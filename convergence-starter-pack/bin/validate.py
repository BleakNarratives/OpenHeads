#!/usr/bin/env python3
"""validate.py - minimal JSON Schema subset validator (stdlib only).

Supports the subset used by the schemas in ../schemas: type, required,
properties, additionalProperties (false), enum, pattern, items, minItems,
minimum. That is enough to prove the generated artifacts actually conform,
without pulling in a dependency the target devices may not have.

Usage:
    python3 bin/validate.py --schema schemas/evidence.schema.json --data reports/ev.json
    python3 bin/validate.py --schema schemas/cluster.schema.json --data '[...]'
"""
from __future__ import annotations

import argparse
import json
import re
import sys

TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
}


def _type_ok(value, expected):
    py = TYPES.get(expected)
    if py is None:
        return True
    if expected in ("integer", "number") and isinstance(value, bool):
        return False
    return isinstance(value, py)


def validate(value, schema, path="$", errors=None):
    """Return a list of human-readable error strings (empty means valid)."""
    if errors is None:
        errors = []

    if "type" in schema and not _type_ok(value, schema["type"]):
        errors.append(f"{path}: expected {schema['type']}, got {type(value).__name__}")
        return errors

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in {schema['enum']}")

    if "pattern" in schema and isinstance(value, str):
        if not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")

    if "minimum" in schema and isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema["minimum"]:
            errors.append(f"{path}: {value} < minimum {schema['minimum']}")

    if isinstance(value, dict):
        for req in schema.get("required", []):
            if req not in value:
                errors.append(f"{path}: missing required property '{req}'")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append(f"{path}: unexpected property '{key}'")
        for key, sub in props.items():
            if key in value:
                validate(value[key], sub, f"{path}.{key}", errors)

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: {len(value)} items < minItems {schema['minItems']}")
        if "items" in schema:
            for i, item in enumerate(value):
                validate(item, schema["items"], f"{path}[{i}]", errors)

    return errors


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="validate.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--schema", required=True)
    p.add_argument("--data", required=True, help="path to a JSON file, or inline JSON")
    args = p.parse_args(argv)

    with open(args.schema, "r", encoding="utf-8") as fh:
        schema = json.load(fh)
    try:
        with open(args.data, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        data = json.loads(args.data)

    errors = validate(data, schema)
    if errors:
        for e in errors:
            print("FAIL", e, file=sys.stderr)
        return 1
    print("OK", args.data, "conforms to", args.schema)
    return 0


if __name__ == "__main__":
    sys.exit(main())
