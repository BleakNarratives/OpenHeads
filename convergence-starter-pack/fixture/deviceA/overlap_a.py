"""Overlap candidate, device A."""


def normalize_path(value):
    """Collapse duplicate separators and strip a trailing slash."""
    while "//" in value:
        value = value.replace("//", "/")
    return value.rstrip("/") or "/"


def join_root(root, leaf):
    """Join two path fragments with exactly one separator."""
    return normalize_path(root + "/" + leaf)
