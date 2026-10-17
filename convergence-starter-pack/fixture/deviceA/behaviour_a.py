"""A real, testable behavior so verification has something true to run."""


def checksum_of(text):
    """Return the simple additive checksum of a string's code points."""
    return sum(ord(ch) for ch in text)
