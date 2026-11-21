#!/usr/bin/env python3
"""The joke about the demo.

Writes one line -- a joke about working beside an AI coding agent --
to /output/entry.txt. Deterministic: the same bytes on every run.
Standard library only; no network.
"""

import hashlib
import os
import sys

# Deterministic by construction: the joke is a fixed string constant.
# No clock, randomness, network, or environment input feeds the
# output, so every run writes exactly the same bytes.
JOKE = (
    "The demo crashed on stage, and my agent said, "
    "'Don't panic \u2014 I already blamed you in the commit message.'"
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 280


def main() -> int:
    text = JOKE
    n_chars = len(text)  # Unicode code points
    if not (MIN_CHARS <= n_chars <= MAX_CHARS):
        print(f"gate failed: {n_chars} chars, need {MIN_CHARS}-{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("gate failed: joke is only whitespace", file=sys.stderr)
        return 1
    if "\n" in text:
        print("gate failed: joke must be one line", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    data = text.encode("utf-8")
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)

    # Write-back verification: read the file and compare bytes exactly.
    with open(OUTPUT_PATH, "rb") as f:
        back = f.read()
    if back != data:
        print("verification failed: /output/entry.txt mismatch",
              file=sys.stderr)
        return 1

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {n_chars} chars to {OUTPUT_PATH} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
