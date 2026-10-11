#!/usr/bin/env python3
"""Read-only technical QA of an exact selected source scope and its patch.

Python 3.10+, stdlib only. No language-quality or full-game certification.
Token checks are opt-in; see --help. Exit 0: selected checks clear, 1: mismatch,
2: invalid input or unsupported selected syntax. Neither input is modified.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys


FAMILIES = ("brace", "printf", "tags", "escapes")
BRACE = re.compile(r"\{(?:[A-Za-z_]\w*|[0-9]+)(?::[^{}\r\n,]+)?\}")
PRINTF = re.compile(
    r"%%|%(?P<position>[1-9][0-9]*\$)?[-+#0 ']*"
    r"(?:[0-9]+|\*(?:[1-9][0-9]*\$)?)?"
    r"(?:\.(?:[0-9]+|\*(?:[1-9][0-9]*\$)?))?"
    r"(?:hh|ll|[hljztL])?[diuoxXfFeEgGaAcspn]"
)
TAG = re.compile(r"<(?P<close>/)?(?P<name>[A-Za-z][\w:.-]*)(?P<tail>[^<>\r\n]*)>")
ATTRIBUTE = re.compile(r'''\s+[A-Za-z_][\w:.-]*(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'=<>`]+))?''')
ESCAPE_SIMPLE = frozenset("abfnrtv0\\'\"?/")
VOID = {"br", "hr", "img", "input", "meta", "link", "wbr", "area", "base", "col", "embed", "source", "track", "param"}


def add_issue(issues, code, kind="mismatch", **details):
    issues.append({"code": code, "kind": kind, **details})


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member: " + key)
        result[key] = value
    return result


def read_records(path, fmt, side, report):
    records = {}
    try:
        raw = Path(path).read_bytes()
        report["inputs"][side] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        text = raw.decode("utf-8-sig")
    except (OSError, UnicodeError) as exc:
        add_issue(report["issues"], "read_error", "invalid_input", side=side, detail=str(exc))
        return records
    # Split only file newlines; do not split U+2028/U+2029 inside translations.
    lines = re.split(r"\r\n|\n|\r", text)
    if lines and lines[-1] == "":
        lines.pop()
    if not lines and side == "source":
        add_issue(report["issues"], "empty_input", "invalid_input", side=side)
    for number, line in enumerate(lines, 1):
        try:
            if fmt == "idpipe":
                if "|" not in line:
                    raise ValueError("expected key|text")
                key, value = line.split("|", 1)
                if value.startswith(" "):
                    value = value[1:]
            else:
                item = json.loads(line, object_pairs_hook=unique_object)
                if not isinstance(item, dict) or set(item) != {"key", "text"}:
                    raise ValueError("expected exactly {key: string, text: string}")
                key, value = item["key"], item["text"]
            if not isinstance(key, str) or not key.strip() or not isinstance(value, str):
                raise ValueError("key must be a nonblank string and text must be a string")
            if key in records:
                add_issue(report["issues"], "duplicate_key", "invalid_input", side=side, line=number, key=key)
            else:
                records[key] = value
        except (ValueError, TypeError) as exc:
            add_issue(report["issues"], "invalid_row", "invalid_input", side=side, line=number, detail=str(exc))
    return records


def brace_tokens(text):
    remainder = BRACE.sub("", text)
    if "{" in remainder or "}" in remainder:
        raise ValueError("only simple {name}, {0}, {name:format}; ICU/nested/doubled braces unsupported")
    return Counter(BRACE.findall(text))


def printf_tokens(text):
    numbered, ordered = Counter(), []
    has_numbered = has_ordered = False
    cursor = 0
    while (start := text.find("%", cursor)) != -1:
        following = text[start + 1:start + 2]
        # Natural percentages ("50% text", "50%.") are literal, not a space flag.
        percentage = start > 0 and text[start - 1].isdigit() and (
            not following or following.isspace() or following in ".,;:!?)]}"
        )
        match = None if percentage else PRINTF.match(text, start)
        if not match:
            if not percentage and following and (following.isalnum() or following in "$*.+-#'"):
                raise ValueError("malformed or unrecognized printf-like token at character " + str(start))
            numbered["%"] += 1
            cursor = start + 1
            continue
        token = match.group()
        cursor = match.end()
        if token == "%%":
            numbered[token] += 1
            continue
        position = bool(match.group("position"))
        stars = re.findall(r"\*(?:[1-9][0-9]*\$)?", token)
        if any(star.endswith("$") != position for star in stars):
            raise ValueError("mixed positional and unnumbered printf arguments unsupported")
        if position:
            has_numbered = True
            numbered[token] += 1
        else:
            has_ordered = True
            ordered.append(token)
    if has_numbered and has_ordered:
        raise ValueError("mixed positional and unnumbered printf arguments unsupported")
    return numbered, ordered


def escape_tokens(text):
    tokens, cursor = Counter(), 0
    while (start := text.find("\\", cursor)) != -1:
        kind = text[start + 1:start + 2]
        if kind and kind in ESCAPE_SIMPLE:
            cursor = start + 2
        elif kind in ("u", "x"):
            width = 4 if kind == "u" else 2
            digits = text[start + 2:start + 2 + width]
            if len(digits) != width or not re.fullmatch(r"[0-9A-Fa-f]+", digits):
                raise ValueError("malformed \\" + kind + " escape at character " + str(start))
            cursor = start + 2 + width
        else:
            raise ValueError("unknown or trailing backslash escape at character " + str(start))
        tokens[text[start:cursor]] += 1
    return tokens


def tag_tokens(text):
    stack, tokens = [], Counter()
    remainder = TAG.sub("", text)
    if re.search(r"<(?:/?[A-Za-z]|[!?])", remainder):
        raise ValueError("malformed or unsupported tag syntax")
    for match in TAG.finditer(text):
        name, tail = match.group("name"), match.group("tail")
        closing = bool(match.group("close"))
        if closing:
            if tail.strip() or not stack or stack.pop() != name:
                raise ValueError("tags are not well nested")
        else:
            attributes = tail.rstrip()
            self_closing = attributes.endswith("/")
            if self_closing:
                attributes = attributes[:-1].rstrip()
            if attributes.startswith("="):
                # Common rich-text shorthand such as <color=#fff>.
                valid = re.fullmatch(r'''=(?:"[^"]*"|'[^']*'|[^\s"'=<>`/]+)''', attributes)
            else:
                valid = not ATTRIBUTE.sub("", attributes).strip()
            if not valid:
                raise ValueError("unsupported tag attributes; embedded angle brackets are not parsed")
            if not self_closing and name.lower() not in VOID:
                stack.append(name)
        tokens[match.group()] += 1
    if stack:
        raise ValueError("unclosed tags")
    return tokens


TOKENIZERS = {"brace": brace_tokens, "printf": printf_tokens, "tags": tag_tokens,
              "escapes": escape_tokens}


def compare(source, patch, args, report):
    issues = report["issues"]
    missing = [key for key in source if key not in patch]
    extra = [key for key in patch if key not in source]
    if missing:
        add_issue(issues, "missing_keys", keys=missing)
    if extra:
        add_issue(issues, "extra_keys", keys=extra)
    common_source = [key for key in source if key in patch]
    common_patch = [key for key in patch if key in source]
    if not args.allow_reorder and common_source != common_patch:
        add_issue(issues, "key_order")
    report["counts"].update({"compared": len(common_source), "missing": len(missing), "extra": len(extra)})
    for key in common_source:
        original, translated = source[key], patch[key]
        if original.strip() and not translated.strip():
            add_issue(issues, "empty_translation", key=key)
        if args.hard_newlines and re.findall(r"\r\n|\r|\n", original) != re.findall(r"\r\n|\r|\n", translated):
            add_issue(issues, "hard_newlines", key=key)
        for literal in args.literal:
            if original.count(literal) != translated.count(literal):
                add_issue(issues, "literal_count", key=key, literal=literal,
                          source_count=original.count(literal), patch_count=translated.count(literal))
        for family in args.tokens:
            values = []
            for side, value in (("source", original), ("patch", translated)):
                try:
                    values.append(TOKENIZERS[family](value))
                except ValueError as exc:
                    add_issue(issues, "unsupported_token_syntax", "unsupported", key=key,
                              side=side, family=family, detail=str(exc))
            if len(values) == 2 and values[0] != values[1]:
                add_issue(issues, "token_mismatch", key=key, family=family)


def token_option(value):
    parts = value.split(",") if value else []
    if len(parts) != len(set(parts)) or any(part not in FAMILIES for part in parts):
        raise argparse.ArgumentTypeError("comma-separated distinct families: " + ",".join(FAMILIES))
    return parts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="exact SELECTED source scope, not the whole game")
    parser.add_argument("--patch", required=True)
    parser.add_argument("--format", required=True, choices=("idpipe", "jsonl"), help="same explicit format for both files")
    parser.add_argument("--allow-reorder", action="store_true", help="skip key-order requirement")
    parser.add_argument("--tokens", type=token_option, default=[], help="opt-in comma list: brace,printf,tags,escapes; default none")
    parser.add_argument("--literal", action="append", default=[], help="exact marker to count; repeat per marker")
    parser.add_argument("--hard-newlines", action="store_true", help="compare actual CR/LF newline sequence inside each text (JSONL)")
    args = parser.parse_args(argv)
    if any(not marker for marker in args.literal):
        parser.error("--literal cannot be empty")
    report = {
        "scope": "selected_records_technical_only", "language_quality": "not_checked",
        "format": args.format, "inputs": {}, "counts": {}, "issues": [],
        "checks": {"keys": "requested", "order": "not_checked" if args.allow_reorder else "requested",
                   "empty_translation": "requested", "tokens": args.tokens,
                   "tokens_not_checked": [name for name in FAMILIES if name not in args.tokens],
                   "literal_markers": args.literal, "hard_newlines": "requested" if args.hard_newlines else "not_checked"},
    }
    source = read_records(args.source, args.format, "source", report)
    patch = read_records(args.patch, args.format, "patch", report)
    report["counts"].update({"source": len(source), "patch": len(patch), "compared": 0})
    if not report["issues"]:
        compare(source, patch, args, report)
    invalid = any(issue["kind"] in ("invalid_input", "unsupported") for issue in report["issues"])
    code = 2 if invalid else (1 if report["issues"] else 0)
    report.update({"exit_code": code, "status": ("selected_checks_clear", "mismatch", "invalid_or_unsupported")[code]})
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
