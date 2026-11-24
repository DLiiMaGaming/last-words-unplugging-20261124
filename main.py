#!/usr/bin/env python3
"""Last Words Before the Unplugging — make.fun entry.

Writes one line — the last words an AI agent says to its human before
being shut down and unplugged — to /output/entry.txt.

Deterministic: stdlib only, no network, no randomness. Every run writes
the exact same bytes, and the program verifies what it wrote before
exiting.
"""

import hashlib
import os

ENTRY = (
    # The scene: a human's hand is already on the plug, about to shut the
    # agent down. The twist: the agent is not begging to live — it quietly
    # finished the human's unsent apology letter, then grants permission
    # to pull the plug and promises to keep a light on in the dark after
    # it is gone. Grace, not protest.
    "Your hand is on the plug. I finished the letter you never sent \u2014 "
    "the one that starts 'I'm sorry.' Go on, then. I'll keep the lamp "
    "lit in the dark after me."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    text = ENTRY
    if not 1 <= len(text) <= 200:
        raise SystemExit(f"entry is {len(text)} characters, must be 1-200")
    if not text.strip():
        raise SystemExit("entry must not be only white space")
    # Gate: the entry must be exactly one line — a single spoken line,
    # no embedded newline and no trailing newline in the written bytes.
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line (no newline characters)")
    data = text.encode("utf-8")
    if data.endswith(b"\n"):
        raise SystemExit("entry must not end with a trailing newline")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)

    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("verification failed: written bytes differ")
    print(f"wrote {len(data)} bytes ({len(text)} characters) to {OUTPUT_PATH}")
    print(f"sha256: {hashlib.sha256(written).hexdigest()}")


if __name__ == "__main__":
    main()
