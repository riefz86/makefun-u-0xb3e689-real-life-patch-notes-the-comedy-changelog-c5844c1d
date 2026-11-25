#!/usr/bin/env python3
"""
Real-Life Patch Notes: The Comedy Changelog (make.fun, u-0xb3e689).

Why this joke, and why it works as a patch note
------------------------------------------------
The best real-life patch notes take a bug everyone has personally
shipped into production -- in their own body -- and describe it in
the flat, apologetic voice of a release engineer who has seen this
crash report a thousand times and still cannot reproduce it on
demand.

The bug picked here is the doorway effect: you walk into a room
with a perfectly clear intention, cross the threshold, and the
intention evaporates. Psychologists really have measured this --
walking through a doorway makes people forget what they went to
fetch, as if the brain treated the room boundary like a context
switch and dropped the previous process's working memory. It is a
bug report the reader has filed themselves, probably this week,
standing in a kitchen holding a fridge door open and staring at
nothing.

That is why the changelog register fits it so well. A real release
note never says "we are sorry you forgot"; it says the state is now
persisted across a boundary, as if memory were a database row that
used to be lost on every room transition. The comedy lands on the
collision between two vocabularies: the solemn, versioned,
"Fixed a bug where..." engineering voice, and a failure so small
and so human that no engineer would ever be assigned to it. The
reader winces because they recognise the bug instantly, then laughs
because the fix is stated as if it shipped in v4.1.2 and they can
now upgrade their brain.

The note is kept deliberately short and single-line: one version,
one bug, one fix, no setup the punchline does not need. The second
sentence ("Memory now persists across thresholds.") is the actual
punchline -- it restates the bug as a shipped feature, which is
exactly how a changelog closes a ticket. "Thresholds" is doing
double duty: it is the engineering word for a doorway and the
ordinary word for a limit, so the line reads as a real fix and a
joke at the same time.

Design of this program
----------------------
The entry text is a single constant, ENTRY, so the program is
deterministic: every run writes exactly the same bytes. A small
validation helper checks the gate the competition seals -- the
file must be UTF-8 text of 1 to 160 characters, not only white
space, and a single line -- and refuses to write an entry that
fails it, so a typo in the text can never silently ship a broken
entry. The output directory is created with os.makedirs only;
no directory permission is ever changed, because the grader runs
as an unprivileged user and a chmod on a directory it does not own
kills the run. Only the result file itself gets a mode set, and
only after it has been written.
"""

import os

# The entry: one line, a software patch note for a bug in human
# biology / daily life. The doorway effect, fixed in v4.1.2.
# "Wiped" was chosen over "deleted": it is the engineer's word for
# data loss, so the bug reads like a cache being cleared on every
# room transition -- which, for the brain, it is.
ENTRY = (
    "v4.1.2: Fixed a bug where walking through a doorway wiped "
    "the reason you entered the room. Memory now persists across "
    "thresholds."
)

MAX_CHARS = 160
OUTPUT_PATH = "/output/entry.txt"


def validate_entry(text):
    """Check the sealed gate: 1-160 chars, non-blank, single line."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    # UTF-8 round-trip: the gate reads the file as UTF-8 text.
    text.encode("utf-8")
    return True


def main():
    validate_entry(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    os.chmod(OUTPUT_PATH, 0o644)
    print("Wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH))


if __name__ == "__main__":
    main()
