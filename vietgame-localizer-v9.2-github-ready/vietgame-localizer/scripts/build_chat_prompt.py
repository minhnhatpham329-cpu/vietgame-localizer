"""Build the portable chat prompt from maintained references (Python stdlib)."""
import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PARTS = (
    "references/chat-workflow.md",
    "references/context-and-state.md",
    "references/language-review.md",
    "references/learning-from-edits.md",
    "references/technical-checks.md",
    "assets/chat-state.md",
)
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def build(root=ROOT):
    sections = []
    for relative in PARTS:
        source = (root / relative).read_text(encoding="utf-8-sig")
        # Local files are embedded below; keep web URLs intact.
        source = LINK.sub(lambda m: m[0] if "://" in m[2] else m[1], source)
        sections.append(source.strip())
    version = re.search(r"\bv[0-9]+(?:\.[0-9]+)*\b", sections[0].splitlines()[0])
    if not version:
        raise ValueError("Workflow title must include its version.")
    return (
        f"HƯỚNG DẪN DỊCH GAME TRONG CHAT — {version.group()}\n"
        "Bản tự chứa, sinh từ tài liệu nguồn của skill; không sửa tay file này.\n"
        "Áp dụng các mục dưới đây mỗi lượt, kể cả khi tôi chỉ nói 'tiếp'.\n"
        "Mẫu STATE ở cuối là mẫu đầu ra để điền, không phải trạng thái dự án có sẵn.\n\n"
        "Các script được nhắc là tùy chọn khi có sẵn; bản TXT này không kèm script.\n\n"
        + "\n\n---\n\n".join(sections) + "\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the export is missing or stale.")
    args = parser.parse_args()
    output = ROOT / "assets/chat-instructions.txt"
    expected = build()
    if args.check:
        if not output.is_file() or output.read_bytes() != expected.encode("utf-8"):
            print("Portable prompt missing or stale; run scripts/build_chat_prompt.py", file=sys.stderr)
            return 1
        print("Portable prompt matches maintained sources.")
    else:
        output.write_bytes(expected.encode("utf-8"))
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
