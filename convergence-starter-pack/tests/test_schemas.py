#!/usr/bin/env python3
"""Schema conformance tests: prove the generated artifacts match the schemas.

Uses the stdlib-only validator in ../bin/validate.py, so no dependency install
is needed. If these pass, the schemas are load-bearing, not decorative.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.dirname(HERE)
FIXTURE = os.path.join(PACK, "fixture")
CONVERGE = os.path.join(PACK, "bin", "converge.py")
VALIDATE = os.path.join(PACK, "bin", "validate.py")
SCHEMAS = os.path.join(PACK, "schemas")


def validate(schema_name, data_path):
    proc = subprocess.run(
        [sys.executable, VALIDATE,
         "--schema", os.path.join(SCHEMAS, schema_name),
         "--data", data_path],
        capture_output=True, text=True)
    return proc


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="converge-schema-")
        cls.man_a = os.path.join(cls.tmp, "a.json")
        cls.man_b = os.path.join(cls.tmp, "b.json")
        cls.ev_a = os.path.join(cls.tmp, "ev_a.json")
        cls.clusters = os.path.join(cls.tmp, "clusters.json")
        cls.report = os.path.join(cls.tmp, "report.json")
        subprocess.run([sys.executable, CONVERGE, "intake", "--device-id", "deviceA",
                        "--root", os.path.join(FIXTURE, "deviceA"), "--out", cls.man_a], check=True)
        subprocess.run([sys.executable, CONVERGE, "intake", "--device-id", "deviceB",
                        "--root", os.path.join(FIXTURE, "deviceB"), "--out", cls.man_b], check=True)
        subprocess.run([sys.executable, CONVERGE, "analyze", "--manifest", cls.man_a,
                        "--out", cls.ev_a], check=True)
        subprocess.run([sys.executable, CONVERGE, "cluster", "--manifests", cls.man_a, cls.man_b,
                        "--out", cls.clusters], check=True)
        subprocess.run([sys.executable, CONVERGE, "report", "--manifests", cls.man_a, cls.man_b,
                        "--out", cls.report], check=True)

    def test_manifest_conforms(self):
        r = validate("repo_manifest.schema.json", self.man_a)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_evidence_conforms(self):
        # analyze emits a JSON array; the schema describes one packet, so wrap it.
        evidence = load(self.ev_a)
        self.assertTrue(evidence)
        for i, packet in enumerate(evidence):
            p = os.path.join(self.tmp, f"packet_{i}.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(packet, fh)
            r = validate("evidence.schema.json", p)
            self.assertEqual(r.returncode, 0, f"packet {i}: {r.stderr}")

    def test_clusters_conform(self):
        clusters = load(self.clusters)["clusters"]
        self.assertTrue(clusters)
        for i, c in enumerate(clusters):
            p = os.path.join(self.tmp, f"cluster_{i}.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(c, fh)
            r = validate("cluster.schema.json", p)
            self.assertEqual(r.returncode, 0, f"cluster {i}: {r.stderr}")

    def test_validator_rejects_bad_data(self):
        """Negative control: the validator must actually fail on bad input."""
        bad = os.path.join(self.tmp, "bad.json")
        with open(bad, "w", encoding="utf-8") as fh:
            json.dump({"manifest_id": "x"}, fh)  # missing required fields
        r = validate("repo_manifest.schema.json", bad)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("missing required", r.stderr)

    def test_validator_rejects_bad_enum(self):
        bad = os.path.join(self.tmp, "bad_enum.json")
        with open(bad, "w", encoding="utf-8") as fh:
            json.dump({"manifest_id": "m", "device_id": "d", "source_root": "/r",
                       "revision": "norev:1", "files": [
                           {"path": "a.py", "sha256": "0" * 64, "size_bytes": 1}],
                       "intake_status": "definitely-not-valid"}, fh)
        r = validate("repo_manifest.schema.json", bad)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not in", r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
