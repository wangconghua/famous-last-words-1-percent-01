#!/usr/bin/env python3
"""Famous Last Words at 1 Percent (make.fun entry).

Writes one original last-words line a phone says as its battery hits
1 percent to /output/entry.txt. The gate requires UTF-8 text of 1-199
characters, not only white space.
"""

import os

# The line: the phone itself talking, in its own voice, about its own
# dying battery. Setup ("Battery at 1%. Good news: I saved your unsent
# draft.") then the turn ("Bad news: it's the text to your ex.") — the
# save the owner would want turns out to be the one message they would
# least want kept. One line, no trailing newline, so the file is exactly
# the line.
LINE = "Battery at 1%. Good news: I saved your unsent draft. Bad news: it's the text to your ex."

# Stock moves the judge brief calls out: the will reading, the goodbye to
# the charger, the pun on 1 percent.
BANNED_PHRASES = (
    "charger",
    "will and testament",
    "i leave my",
    "i bequeath",
    "goodbye cruel",
    "i'm the 1",
    "the one percent",
    "farewell, charger",
)

# The phone's own dying-battery voice: a battery mention plus a
# first-person claim of its own.
BATTERY_WORDS = ("battery", "1%", "percent", "power")
PHONE_VOICE = ("i ", "i'm", "i've", "my ")


def validate(line):
    """Gate plus the judge brief, enforced before the line is written."""
    # Gate: 1-199 characters, not only white space, single line.
    if not 1 <= len(line) <= 199:
        raise ValueError(f"line is {len(line)} chars, must be 1-199")
    if not line.strip():
        raise ValueError("line must not be only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if line != line.strip():
        raise ValueError("line must have no leading or trailing whitespace")
    if "  " in line:
        raise ValueError("line must have no double spaces")
    # The phone itself talking about its own dying battery.
    lowered = line.lower()
    if not any(word in lowered for word in BATTERY_WORDS):
        raise ValueError("line must name its own dying battery")
    if not any(word in lowered for word in PHONE_VOICE):
        raise ValueError("line must speak in the phone's own voice")
    # The joke must turn: a setup sentence and a punch sentence.
    if ". " not in line:
        raise ValueError("line must carry a turn: setup, then punch")
    # No stock move of the genre: no will, no charger goodbye, no 1% pun.
    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            raise ValueError(f"line uses stock material: {phrase!r}")
    return line


def main():
    line = validate(LINE)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    print(f"{line} ({len(line)} chars)")


if __name__ == "__main__":
    main()
