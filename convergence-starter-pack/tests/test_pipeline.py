#!/usr/bin/env python3
"""End-to-end tests for the convergence starter pack.

Runs against the real fixture in ../fixture and the real pipeline in ../bin.
Uses only the standard library, so `python3 -m unittest` works with no install.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.dirname(HERE)
FIXTURE = os.path.join(PACK, "fixture")
BIN = os.path.join(PACK, "bin", "converge.py")


def run(*args):
    """Run the pipeline CLI and return (exit_code, parsed_json_or_stdout)."""
    proc = subprocess.run([sys.executable, BIN, *args], capture_output=True, text=True)
    return proc


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def tree_hashes(root):
    """sha256 of every file under root, keyed by relative path."""
    out = {}
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            ap = os.path.join(dirpath, name)
            rel = os.path.relpath(ap, root)
            with open(ap, "rb") as fh:
                out[rel] = hashlib.sha256(fh.read()).hexdigest()
    return out


class ConvergenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="converge-test-")
        cls.man_a = os.path.join(cls.tmp, "a.json")
        cls.man_b = os.path.join(cls.tmp, "b.json")
        r1 = run("intake", "--device-id", "deviceA", "--root", os.path.join(FIXTURE, "deviceA"), "--out", cls.man_a)
        r2 = run("intake", "--device-id", "deviceB", "--root", os.path.join(FIXTURE, "deviceB"), "--out", cls.man_b)
        assert r1.returncode == 0, r1.stderr
        assert r2.returncode == 0, r2.stderr
        cls.report_path = os.path.join(cls.tmp, "report.json")
        r3 = run("report", "--manifests", cls.man_a, cls.man_b, "--out", cls.report_path)
        assert r3.returncode == 0, r3.stderr
        cls.report = load(cls.report_path)

    # 1. discovery + provenance -------------------------------------------------
    def test_intake_records_device_provenance(self):
        a = load(self.man_a)
        self.assertEqual(a["device_id"], "deviceA")
        self.assertTrue(a["source_root"].endswith("deviceA"))
        self.assertTrue(a["revision"].startswith("norev:"))
        self.assertTrue(all(len(f["sha256"]) == 64 for f in a["files"]))

    def test_evidence_preserves_manifest_id(self):
        ev_path = os.path.join(self.tmp, "ev.json")
        r = run("analyze", "--manifest", self.man_a, "--out", ev_path)
        self.assertEqual(r.returncode, 0, r.stderr)
        ev = load(ev_path)
        self.assertTrue(ev)
        a_id = load(self.man_a)["manifest_id"]
        self.assertTrue(all(e["manifest_id"] == a_id for e in ev))

    # 2. overlapping candidates -------------------------------------------------
    def test_overlap_symbol_clustered(self):
        symbols = [s for c in self.report["clusters"] for m in c["members"] for s in m["shared_symbols"]]
        self.assertIn("normalize_path", symbols)
        self.assertIn("join_root", symbols)
        for c in self.report["clusters"]:
            self.assertEqual(c["confidence_basis"], "symbol-overlap")
            self.assertEqual(c["recommendation"], "needs-verification")

    # 3. unique module ----------------------------------------------------------
    def test_unique_symbol_not_clustered(self):
        uniq = [u["symbol"] for u in self.report["unique_symbols"]]
        self.assertIn("device_a_only_marker", uniq)
        clustered = {s for c in self.report["clusters"] for m in c["members"] for s in m["shared_symbols"]}
        self.assertNotIn("device_a_only_marker", clustered)

    # 4. stub detection ---------------------------------------------------------
    def test_stub_flagged(self):
        stubs = {(s["manifest_id"], s["symbol"]) for s in self.report["stubs"]}
        b_id = load(self.man_b)["manifest_id"]
        self.assertIn((b_id, "promised_but_absent"), stubs)

    def test_implemented_function_not_flagged_as_stub(self):
        stubs = {s["symbol"] for s in self.report["stubs"]}
        self.assertNotIn("normalize_path", stubs)
        self.assertNotIn("checksum_of", stubs)

    # 5. real behaviour test ----------------------------------------------------
    def test_real_behaviour_runs(self):
        path = os.path.join(FIXTURE, "deviceA", "behaviour_a.py")
        spec = importlib.util.spec_from_file_location("behaviour_a", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.checksum_of("AB"), ord("A") + ord("B"))

    # 6. reviewability: no task is auto-applied ---------------------------------
    def test_no_task_is_auto_applied(self):
        self.assertTrue(self.report["proposed_tasks"])
        self.assertTrue(all(t["apply"] is False for t in self.report["proposed_tasks"]))

    # 7. safety: pipeline never modifies the source fixture ---------------------
    def test_source_tree_untouched(self):
        before = tree_hashes(FIXTURE)
        tmp2 = tempfile.mkdtemp(prefix="converge-recheck-")
        m = os.path.join(tmp2, "a.json")
        run("intake", "--device-id", "deviceA", "--root", os.path.join(FIXTURE, "deviceA"), "--out", m)
        run("report", "--manifests", m, "--out", os.path.join(tmp2, "r.json"))
        self.assertEqual(before, tree_hashes(FIXTURE))

    # 8. bounds are honoured and truncation is reported -------------------------
    def test_scan_bound_reports_truncation(self):
        tmp3 = tempfile.mkdtemp(prefix="converge-bound-")
        m = os.path.join(tmp3, "a.json")
        r = run("intake", "--device-id", "deviceA", "--root", os.path.join(FIXTURE, "deviceA"),
                "--out", m, "--max-files", "1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(load(m)["truncated"])
        self.assertEqual(len(load(m)["files"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
