"""Entry program for make.fun bounty
u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a
(Make the AI Judge Laugh: Office Jokes).

Writes the one-line office joke to entry.txt in the output directory
(MAKEFUN_OUTPUT_DIR, default /output). Deterministic: no input, no
randomness, no clock.
"""

import os

JOKE = (
    "My boss told me to treat the company like family, "
    "so now I don't answer its messages after 6 pm."
)

MAX_CHARS = 199  # gate: entry.txt must be 1..199 UTF-8 characters


def validated_text() -> str:
    """Return the joke after checking it against the entry gate:
    UTF-8 encodable, 1..199 characters, not only whitespace, one line."""
    text = JOKE
    encoded = text.encode("utf-8")  # raises if not encodable
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry is {len(text)} chars, gate allows 1..{MAX_CHARS}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(encoded.decode("utf-8")) != len(text):
        raise ValueError("entry does not round-trip as UTF-8")
    return text


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    payload = (validated_text() + "\n").encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(payload)
    with open(path, "rb") as fh:  # read back: bytes on disk must match exactly
        if fh.read() != payload:
            raise IOError("written entry does not match intended bytes")


if __name__ == "__main__":
    main()
