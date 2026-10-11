"""Synthetic technical invariants only; these tests do not measure translation quality."""

from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_patch.py"
SPEC = importlib.util.spec_from_file_location("check_patch", SCRIPT)
QA = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QA)


class PatchTests(unittest.TestCase):
    def run_check(self, source, patch, *options, fmt="idpipe"):
        with tempfile.TemporaryDirectory() as directory:
            files = [Path(directory) / name for name in ("source.txt", "patch.txt")]
            before = [value.encode("utf-8") if isinstance(value, str) else value for value in (source, patch)]
            for path, raw in zip(files, before):
                path.write_bytes(raw)
            output = io.StringIO()
            with redirect_stdout(output):
                code = QA.main(["--source", str(files[0]), "--patch", str(files[1]), "--format", fmt, *options])
            report = json.loads(output.getvalue())
            self.assertEqual([path.read_bytes() for path in files], before, "checker must never mutate inputs")
            self.assertEqual(code, report["exit_code"])
            for side, raw in zip(("source", "patch"), before):
                self.assertEqual(report["inputs"][side]["sha256"], hashlib.sha256(raw).hexdigest())
            return code, report

    def assert_issue(self, report, name):
        self.assertIn(name, [item["code"] for item in report["issues"]])

    @staticmethod
    def rows(items):
        return "\n".join(json.dumps({"key": key, "text": value}, ensure_ascii=False) for key, value in items)

    def test_unicode_bom_and_actual_hash(self):
        code, report = self.run_check(b"\xef\xbb\xbfscene.1| Hi\r\n", "scene.1| Xin chào\r\n")
        self.assertEqual(code, 0)
        self.assertEqual(report["language_quality"], "not_checked")
        self.assertEqual(report["checks"]["tokens"], [])

    def test_missing_and_extra(self):
        code, report = self.run_check("a|A\nb|B", "a|Một\nc|Ba")
        self.assertEqual(code, 1)
        self.assert_issue(report, "missing_keys")
        self.assert_issue(report, "extra_keys")
        code, report = self.run_check("a|A\nb|B", "")
        self.assertEqual(code, 1)
        self.assertEqual(report["issues"], [{"code": "missing_keys", "kind": "mismatch", "keys": ["a", "b"]}])

    def test_duplicate_source_and_patch(self):
        for source, patch in (("a|A\na|B", "a|Một"), ("a|A", "a|Một\na|Hai")):
            code, report = self.run_check(source, patch)
            self.assertEqual(code, 2)
            self.assert_issue(report, "duplicate_key")

    def test_shuffled_keys_and_explicit_opt_out(self):
        source, patch = "a|A\nb|B", "b|Hai\na|Một"
        self.assertEqual(self.run_check(source, patch)[0], 1)
        self.assertEqual(self.run_check(source, patch, "--allow-reorder")[0], 0)

    def test_invalid_rows_and_empty_target(self):
        for source, patch in (("a|A", "invalid"), ("a|A\n\n", "a|Một"), ("|A", "a|Một"), ("", "")):
            self.assertEqual(self.run_check(source, patch)[0], 2)
        code, report = self.run_check("a|A", "a|   ")
        self.assertEqual(code, 1)
        self.assert_issue(report, "empty_translation")

    def test_literal_none_and_json_null(self):
        self.assertEqual(self.run_check("None|None", "None|None")[0], 0)
        source = self.rows([("None", "None")])
        self.assertEqual(self.run_check(source, source, fmt="jsonl")[0], 0)
        for patch in ('{"key":"None","text":null}', '{"key":1,"text":"None"}', '{"key":"None","text":0}'):
            self.assertEqual(self.run_check(source, patch, fmt="jsonl")[0], 2)

    def test_json_duplicate_fields_and_extra_fields(self):
        source = self.rows([("a", "A")])
        for patch in ('{"key":"a","text":"X","text":"Y"}', '{"key":"a","text":"X","other":1}'):
            self.assertEqual(self.run_check(source, patch, fmt="jsonl")[0], 2)

    def test_idpipe_first_separator_and_preserved_whitespace(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scope.txt"
            path.write_text("key|  leading | trailing  \n", encoding="utf-8")
            report = {"inputs": {}, "issues": []}
            self.assertEqual(QA.read_records(path, "idpipe", "source", report), {"key": " leading | trailing  "})
        code, report = self.run_check("a|  x|y  ", "a| x|y ", "--literal", "  ")
        self.assertEqual(code, 1)
        self.assert_issue(report, "literal_count")

    def test_braces_drop_multiplicity_and_reorder(self):
        source = "a|{name} gives {0:02d} to {name}"
        self.assertEqual(self.run_check(source, "a|{name} {0:02d}", "--tokens", "brace")[0], 1)
        self.assertEqual(self.run_check(source, "a|{0:02d} {name} {name}", "--tokens", "brace")[0], 0)

    def test_icu_and_nested_are_explicitly_unsupported(self):
        for text in ("{n, plural, one {item} other {items}}", "{{name}}", "{broken"):
            code, report = self.run_check("a|" + text, "a|" + text, "--tokens", "brace")
            self.assertEqual(code, 2)
            self.assert_issue(report, "unsupported_token_syntax")
        self.assertEqual(self.run_check("a|{n, plural, one {x}}", "a|Xin chào")[0], 0)

    def test_printf_numbered_reorder_and_unnumbered_sequence(self):
        self.assertEqual(self.run_check("a|%1$s %2$d %%", "a|%2$d %1$s %%", "--tokens", "printf")[0], 0)
        self.assertEqual(self.run_check("a|%s %d", "a|%d %s", "--tokens", "printf")[0], 1)
        self.assertEqual(self.run_check("a|%s %s", "a|%s", "--tokens", "printf")[0], 1)
        self.assertEqual(self.run_check("a|%2$*1$s", "a|%2$*1$s", "--tokens", "printf")[0], 0)
        for text in ("%1$s %d", "%1$*s", "%q"):
            self.assertEqual(self.run_check("a|" + text, "a|" + text, "--tokens", "printf")[0], 2)

    def test_printf_malformed_tokens_cannot_report_clear(self):
        for text in ("%1$", "%0", "%*", "%.", "%2$*1$", "%llq", "%1$z"):
            with self.subTest(text=text):
                code, report = self.run_check("a|" + text, "a|" + text, "--tokens", "printf")
                self.assertEqual(code, 2)
                self.assert_issue(report, "unsupported_token_syntax")
                self.assertEqual(self.run_check("a|%s", "a|" + text, "--tokens", "printf")[0], 2)

    def test_printf_literal_percent_and_space_flag(self):
        for source, patch in (("50% text", "50% chữ"), ("50%", "50%"), ("50%.", "50%."), ("Symbol: %", "Dấu: %")):
            self.assertEqual(self.run_check("a|" + source, "a|" + patch, "--tokens", "printf")[0], 0)
        self.assertEqual(self.run_check("a|50% text", "a|50 chữ", "--tokens", "printf")[0], 1)
        self.assertEqual(self.run_check("a|% d", "a|% s", "--tokens", "printf")[0], 1)

    def test_tags_multiset_and_nesting(self):
        source = 'a|<b><i>Hello</i></b><br/><color=#fff>Friend</color>'
        valid = 'a|<color=#fff>Bạn</color><br/><b><i>Xin chào</i></b>'
        self.assertEqual(self.run_check(source, valid, "--tokens", "tags")[0], 0)
        for patch in ('a|<b><i>X</b></i><br/><color=#fff>Y</color>', 'a|<b>X', 'a|<b', 'a|<b foo=\">\">X</b>', 'a|<b /bad>X</b>'):
            self.assertEqual(self.run_check(source, patch, "--tokens", "tags")[0], 2)
        self.assertEqual(self.run_check("a|<b>A</b>", "a|A", "--tokens", "tags")[0], 1)
        self.assertEqual(self.run_check("a|a < 3<br>", "a|b < 3<br>", "--tokens", "tags")[0], 0)

    def test_escapes_literals_and_actual_newlines(self):
        source = self.rows([("a", "Hi\\n{name}\nA\u2028B")])
        patch = self.rows([("a", "Chào\\n{name}\nC\u2028D")])
        self.assertEqual(self.run_check(source, patch, "--tokens", "brace,escapes", "--hard-newlines", fmt="jsonl")[0], 0)
        lost_escape = self.rows([("a", "Chào{name}\nC\u2028D")])
        self.assertEqual(self.run_check(source, lost_escape, "--tokens", "escapes", fmt="jsonl")[0], 1)
        lost_newline = self.rows([("a", "Chào\\n{name} C\u2028D")])
        self.assertEqual(self.run_check(source, lost_newline, "--hard-newlines", fmt="jsonl")[0], 1)
        self.assertEqual(self.run_check("a|<PLAYER> hi", "a|chào", "--literal", "<PLAYER>")[0], 1)

    def test_escape_scanner_covers_every_backslash_and_preserves_pairs(self):
        supported = r"\a\b\f\v\n\r\t\0\'\"\?\/\u00AF\x0a"
        self.assertEqual(self.run_check("a|" + supported, "a|" + supported, "--tokens", "escapes")[0], 0)
        for token in (r"\a", r"\b", r"\f", r"\v"):
            self.assertEqual(self.run_check("a|Hi" + token, "a|Chào", "--tokens", "escapes")[0], 1)
        for text in (r"\q", r"\u123", r"\u12G4", r"\x1", "\\", r"\U00000041"):
            with self.subTest(text=text):
                code, report = self.run_check("a|" + text, "a|" + text, "--tokens", "escapes")
                self.assertEqual(code, 2)
                self.assert_issue(report, "unsupported_token_syntax")
                self.assertEqual(self.run_check(r"a|Hi\n", "a|" + text, "--tokens", "escapes")[0], 2)
        # Two backslashes are one literal-backslash escape; following q is ordinary text.
        self.assertEqual(self.run_check(r"a|\\q", r"a|\\q", "--tokens", "escapes")[0], 0)
        self.assertEqual(self.run_check(r"a|\\n", r"a|\n", "--tokens", "escapes")[0], 1)

    def test_1000_record_technical_smoke_and_final_record_mutation(self):
        source = [(f"scene.{i}", f"Hello {{name}} %1$s <b>{i}</b>\\n") for i in range(1000)]
        patch = [(key, value.replace("Hello", "Xin chào")) for key, value in source]
        options = ("--tokens", "brace,printf,tags,escapes")
        code, report = self.run_check(self.rows(source), self.rows(patch), *options, fmt="jsonl")
        self.assertEqual(code, 0)
        self.assertEqual(report["counts"]["compared"], 1000)
        patch[-1] = (patch[-1][0], patch[-1][1].replace("{name}", ""))
        code, report = self.run_check(self.rows(source), self.rows(patch), *options, fmt="jsonl")
        self.assertEqual(code, 1)
        self.assertEqual(report["issues"], [{"code": "token_mismatch", "kind": "mismatch", "key": "scene.999", "family": "brace"}])


if __name__ == "__main__":
    unittest.main()
