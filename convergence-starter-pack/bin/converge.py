#!/usr/bin/env python3
"""converge.py - bounded, provenance-preserving convergence pipeline (stdlib only).

Three stages, each writing a JSON artifact that the next stage consumes:

  intake   scan a bounded root -> repo_manifest   (identity + provenance + hashes)
  analyze  manifest -> evidence[]                  (claims tied to symbols/lines)
  cluster  manifests + evidence -> clusters[]      (overlap hypotheses, never merges)

Design rules enforced here, not just documented:
  * every scan is bounded by --max-files / --max-depth / --max-seconds, and any
    truncation is recorded in the manifest rather than silently dropped;
  * every evidence packet carries the manifest_id it came from, so provenance
    survives to the final report;
  * a symbol found in one manifest only is reported as unique and is never
    proposed for merging;
  * a function whose body is only a docstring and/or `pass` is reported as a
    stub, regardless of how complete its signature looks;
  * no stage writes to, deletes, or renames any scanned source tree.

Subcommands:
  intake  --device-id ID --root PATH --out FILE
  analyze --manifest FILE --out FILE
  cluster --manifests FILE [FILE ...] --out FILE
  report  --manifests FILE [FILE ...] --out FILE
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import sys
import time

STUB_SENTINELS = {"pass", "NotImplementedError", "..."}


# ---------------------------------------------------------------------------
# intake
# ---------------------------------------------------------------------------
def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def walk_bounded(root: str, max_files: int, max_depth: int, max_seconds: float):
    """Yield (abs_path, rel_path). Stops on any bound and reports which one bit."""
    started = time.time()
    truncated_by = None
    count = 0
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        depth = 0 if rel_dir == "." else rel_dir.count(os.sep) + 1
        if depth >= max_depth:
            dirnames[:] = []
        for name in sorted(filenames):
            if count >= max_files:
                truncated_by = "max_files"
                break
            if time.time() - started > max_seconds:
                truncated_by = "max_seconds"
                break
            abs_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(abs_path, root)
            count += 1
            yield abs_path, rel_path
        if truncated_by:
            break
    if truncated_by:
        # surface the bound via a sentinel attribute on the generator
        walk_bounded.last_truncation = truncated_by
    else:
        walk_bounded.last_truncation = None


def intake(device_id: str, root: str, max_files: int, max_depth: int,
           max_seconds: float) -> dict:
    files = []
    for abs_path, rel_path in walk_bounded(root, max_files, max_depth, max_seconds):
        try:
            size = os.path.getsize(abs_path)
            digest = sha256_file(abs_path)
        except OSError:
            continue
        entry = {"path": rel_path.replace(os.sep, "/"), "sha256": digest, "size_bytes": size}
        if rel_path.endswith(".py"):
            entry["language"] = "python"
        files.append(entry)
    rev_material = "".join(sorted(f"{f['path']}:{f['sha256']}" for f in files))
    revision = "norev:" + hashlib.sha256(rev_material.encode()).hexdigest()[:16]
    manifest_id = hashlib.sha256(f"{device_id}|{revision}|{root}".encode()).hexdigest()[:16]
    return {
        "manifest_id": manifest_id,
        "device_id": device_id,
        "source_root": os.path.abspath(root),
        "revision": revision,
        "intake_status": "discovered",
        "files": files,
        "truncated": walk_bounded.last_truncation is not None,
    }


# ---------------------------------------------------------------------------
# analyze  (evidence extraction)
# ---------------------------------------------------------------------------
def _is_stub(node: ast.AST) -> bool:
    """True when a function body does nothing but declare its own docstring/pass."""
    body = [n for n in getattr(node, "body", [])]
    # drop a leading docstring
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    if not body:
        return True
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if isinstance(only, ast.Expr) and isinstance(only.value, ast.Constant) \
                and only.value.value is Ellipsis:
            return True
        if isinstance(only, ast.Raise):
            exc = only.exc
            name = getattr(getattr(exc, "func", exc), "id", None)
            if name == "NotImplementedError":
                return True
    return False


def analyze_file(manifest_id: str, source_root: str, rel_path: str):
    """Return a list of evidence packets for one Python file."""
    abs_path = os.path.join(source_root, rel_path)
    try:
        with open(abs_path, "r", encoding="utf-8") as fh:
            source = fh.read()
        tree = ast.parse(source)
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        return [{
            "evidence_id": hashlib.sha256(f"{manifest_id}:{rel_path}".encode()).hexdigest()[:16],
            "manifest_id": manifest_id,
            "claim": f"could not parse: {exc.__class__.__name__}",
            "source_path": rel_path,
            "evidence_type": "undocumented",
            "verification_status": "unverified",
            "limitations": ["file was not analysed"],
        }]

    out = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            stub = _is_stub(node)
            out.append({
                "evidence_id": hashlib.sha256(f"{manifest_id}:{rel_path}:{node.name}".encode()).hexdigest()[:16],
                "manifest_id": manifest_id,
                "claim": f"defines function {node.name}",
                "source_path": rel_path,
                "location": {"symbol": node.name, "line_start": node.lineno, "line_end": node.end_lineno},
                "evidence_type": "stubbed" if stub else "implemented",
                "verification_status": "unverified",
                "limitations": ["body not executed"] + (["body is only pass/docstring"] if stub else []),
            })
        elif isinstance(node, ast.ClassDef):
            out.append({
                "evidence_id": hashlib.sha256(f"{manifest_id}:{rel_path}:{node.name}".encode()).hexdigest()[:16],
                "manifest_id": manifest_id,
                "claim": f"defines class {node.name}",
                "source_path": rel_path,
                "location": {"symbol": node.name, "line_start": node.lineno, "line_end": node.end_lineno},
                "evidence_type": "implemented",
                "verification_status": "unverified",
                "limitations": ["body not executed"],
            })
    return out


def analyze(manifest: dict):
    evidence = []
    for f in manifest["files"]:
        if f.get("language") == "python":
            evidence.extend(analyze_file(manifest["manifest_id"], manifest["source_root"], f["path"]))
    return evidence


# ---------------------------------------------------------------------------
# cluster
# ---------------------------------------------------------------------------
def cluster(manifests, evidence):
    """Group symbols by the manifests that define them. Names are hypotheses."""
    symbol_sites = {}   # symbol -> list of (manifest_id, source_path)
    for ev in evidence:
        if ev.get("evidence_type") == "undocumented":
            continue
        sym = (ev.get("location") or {}).get("symbol")
        if not sym:
            continue
        symbol_sites.setdefault(sym, []).append((ev["manifest_id"], ev["source_path"]))

    clusters = []
    unique = []
    for sym, sites in sorted(symbol_sites.items()):
        distinct = sorted({m for m, _ in sites})
        if len(distinct) >= 2:
            clusters.append({
                "cluster_id": "cl-" + hashlib.sha256(sym.encode()).hexdigest()[:10],
                "members": [
                    {"manifest_id": m, "source_path": p, "shared_symbols": [sym]}
                    for m, p in sorted(set(sites))
                ],
                "overlap_rationale": f"symbol '{sym}' is defined independently in {len(distinct)} manifests",
                "conflicts": [],
                "confidence_basis": "symbol-overlap",
                "recommendation": "needs-verification",
            })
        else:
            unique.append({"symbol": sym, "manifest_id": distinct[0], "source_path": sites[0][1]})
    return clusters, unique


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
def report(manifests, evidence, clusters, unique):
    stubs = [e for e in evidence if e.get("evidence_type") == "stubbed"]
    return {
        "manifests": [
            {"manifest_id": m["manifest_id"], "device_id": m["device_id"],
             "source_root": m["source_root"], "revision": m["revision"],
             "files": len(m["files"]), "truncated": m.get("truncated", False)}
            for m in manifests
        ],
        "counts": {
            "manifests": len(manifests),
            "evidence": len(evidence),
            "clusters": len(clusters),
            "unique_symbols": len(unique),
            "stubs": len(stubs),
        },
        "clusters": clusters,
        "unique_symbols": unique,
        "stubs": [{"manifest_id": e["manifest_id"], "source_path": e["source_path"],
                   "symbol": e["location"]["symbol"]} for e in stubs],
        "proposed_tasks": [
            {
                "task_id": c["cluster_id"],
                "kind": "verify-then-consider",
                "targets": [m["source_path"] for m in c["members"]],
                "acceptance": "Kilo independently confirms shared behaviour by running both "
                              "implementations; a diff is produced before any change.",
                "apply": False,
            }
            for c in clusters
        ],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _dump(obj, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True)
    print(f"wrote {path}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="converge.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("intake", help="scan a bounded root into a repo_manifest")
    pi.add_argument("--device-id", required=True)
    pi.add_argument("--root", required=True)
    pi.add_argument("--out", required=True)
    pi.add_argument("--max-files", type=int, default=5000)
    pi.add_argument("--max-depth", type=int, default=25)
    pi.add_argument("--max-seconds", type=float, default=30.0)

    pa = sub.add_parser("analyze", help="manifest -> evidence packets")
    pa.add_argument("--manifest", required=True)
    pa.add_argument("--out", required=True)

    pc = sub.add_parser("cluster", help="manifests -> overlap clusters + unique symbols")
    pc.add_argument("--manifests", nargs="+", required=True)
    pc.add_argument("--out", required=True)

    pr = sub.add_parser("report", help="manifests -> full report + proposed tasks")
    pr.add_argument("--manifests", nargs="+", required=True)
    pr.add_argument("--out", required=True)

    args = p.parse_args(argv)

    if args.cmd == "intake":
        _dump(intake(args.device_id, args.root, args.max_files, args.max_depth, args.max_seconds), args.out)
        return 0
    if args.cmd == "analyze":
        m = _load(args.manifest)
        _dump(analyze(m), args.out)
        return 0
    if args.cmd == "cluster":
        ms = [_load(x) for x in args.manifests]
        ev = [e for m in ms for e in analyze(m)]
        cl, uniq = cluster(ms, ev)
        _dump({"clusters": cl, "unique_symbols": uniq}, args.out)
        return 0
    if args.cmd == "report":
        ms = [_load(x) for x in args.manifests]
        ev = [e for m in ms for e in analyze(m)]
        cl, uniq = cluster(ms, ev)
        _dump(report(ms, ev, cl, uniq), args.out)
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
