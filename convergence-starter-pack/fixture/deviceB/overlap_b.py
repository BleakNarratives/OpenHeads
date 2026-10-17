"""Overlap candidate, device B."""


def normalize_path(value):
    """Same contract as device A, independently written."""
    parts = [p for p in value.split("/") if p]
    return "/" + "/".join(parts)


def join_root(root, leaf):
    """Join two path fragments."""
    return normalize_path(root + "/" + leaf)
