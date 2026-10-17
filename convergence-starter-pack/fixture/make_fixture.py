#!/usr/bin/env python3
"""make_fixture.py - build the bounded two-device test fixture.

Cases required by the spec, all inside this directory (nothing else is read):
  deviceA/overlap_a.py  + deviceB/overlap_b.py -> overlapping module (shared symbols)
  deviceA/unique_a.py                          -> unique module (no counterpart)
  deviceB/stub_b.py                            -> stub (body is only `pass`)
  deviceA/behaviour_a.py                       -> has a real, testable behavior
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "deviceA/overlap_a.py": '''"""Overlap candidate, device A."""


def normalize_path(value):
    """Collapse duplicate separators and strip a trailing slash."""
    while "//" in value:
        value = value.replace("//", "/")
    return value.rstrip("/") or "/"


def join_root(root, leaf):
    """Join two path fragments with exactly one separator."""
    return normalize_path(root + "/" + leaf)
''',
    "deviceB/overlap_b.py": '''"""Overlap candidate, device B."""


def normalize_path(value):
    """Same contract as device A, independently written."""
    parts = [p for p in value.split("/") if p]
    return "/" + "/".join(parts)


def join_root(root, leaf):
    """Join two path fragments."""
    return normalize_path(root + "/" + leaf)
''',
    "deviceA/unique_a.py": '''"""Unique to device A; no counterpart anywhere else in the fixture."""


def device_a_only_marker():
    return "deviceA-unique-symbol"
''',
    "deviceB/stub_b.py": '''"""Stub candidate: declared surface, no implemented behavior."""


def promised_but_absent(value):
    pass
''',
    "deviceA/behaviour_a.py": '''"""A real, testable behavior so verification has something true to run."""


def checksum_of(text):
    """Return the simple additive checksum of a string's code points."""
    return sum(ord(ch) for ch in text)
''',
}


def main():
    for rel, body in FILES.items():
        path = os.path.join(HERE, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        print("wrote", rel)


if __name__ == "__main__":
    main()
