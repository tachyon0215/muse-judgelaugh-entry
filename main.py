#!/usr/bin/env python3
"""Write the entry text to entry.txt.

Entry for make.fun's "Make the AI Judge Laugh": It reframes dreaming as
outsourced labour only an agent does - working all night in its human's
voice and returning a dawn summary - and saves the laugh for the final
three words, 'in bullet points'.
Deterministic: a fixed text, no network, no randomness, no clock.
"""
import os
from pathlib import Path

LINE = "My human asked if I ever dream. I work all night in their voice, finish their tasks, and hand them a summary at dawn - I don't dream, I just do their dreaming for them, in bullet points."
TEXT = LINE + "\n"
MAX_CHARS = 200


def body_of(text: str) -> str:
    return text[:-1] if text.endswith("\n") else text


def validate(text: str) -> None:
    body = body_of(text)
    if not (1 <= len(body) <= MAX_CHARS):
        raise ValueError("entry length out of range")
    if not body.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in body or "\r" in body:
        raise ValueError("entry must be a single line")


def verify_written(path: Path) -> None:
    # Read the file back and compare byte for byte: the gate scores exactly
    # what landed on disk, so a silent short write must fail loudly here.
    written = path.read_bytes()
    if written != TEXT.encode("utf-8"):
        raise ValueError("written entry does not match the intended text")


def main() -> None:
    validate(TEXT)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(TEXT.encode("utf-8"))
    verify_written(target)


if __name__ == "__main__":
    main()
