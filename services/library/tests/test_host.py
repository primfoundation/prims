import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from prim_library.library import Library, LibraryError
from prim_library.cli import create
from prim_library.host_catalog import export_host_catalog
from prim_library.pack import read_pack

ROOT = Path(__file__).resolve().parents[3]


class HostInteropTests(unittest.TestCase):
    def test_export_preserves_all_exact_pins_and_cannot_mutate_library(self):
        library = Library()
        catalog = export_host_catalog(library, "fixture-source")
        self.assertEqual(len(catalog["kits"]), 5)
        for kit in catalog["kits"]:
            self.assertEqual(library.kit(kit["profile_id"], kit["version"])["definition_sha256"], kit["definition_sha256"])
        catalog["kits"][0]["template"]["injected"] = True
        self.assertNotIn("injected", export_host_catalog(library)["kits"][0]["template"])

    def test_shared_corpus_is_consistent_with_reference_rules(self):
        library = Library()
        corpus = json.loads((ROOT / "sdk/typescript/tests/fixtures/prim-host-cases.json").read_text())
        for case in corpus["cases"]:
            result = library.validate(case["profile_id"], case["version"], case["record"])
            self.assertEqual(result["status"] == "passed", case["valid"], case["name"])
            self.assertEqual(result["definition_sha256"], case["definition_sha256"])

    def test_python_created_packs_are_read_by_actual_sdk_and_sdk_packs_by_python(self):
        library = Library()
        with tempfile.TemporaryDirectory() as tmp:
            for i, kit in enumerate(export_host_catalog(library)["kits"]):
                target = Path(tmp) / f"python-{i}"
                values = {"external_extension": {"keep": ["漢字", True, False, None, 42]}}
                create(library, kit["profile_id"], kit["version"], target, values)
                result = subprocess.run(["node", "--experimental-strip-types", "sdk/typescript/src/cli.ts", "profile", "check", str(target)], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                other = Path(tmp) / f"sdk-{i}"
                result = subprocess.run(["node", "--experimental-strip-types", "sdk/typescript/src/cli.ts", "profile", "create", kit["profile_id"], "--version", kit["version"], "--output", str(other)], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                read = read_pack(library, other)
                self.assertEqual(read["validation"]["status"], "passed")
                self.assertEqual(read["pin"]["definition_sha256"], kit["definition_sha256"])

    def test_lock_tampering_and_symlinked_record_are_rejected(self):
        library = Library()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "record"
            kit = library.kit("primfoundation/person", "0.1.0-dev.1")
            create(library, kit["profile_id"], kit["version"], target)
            pinfile = target / "prim-definition.lock.json"
            pin = json.loads(pinfile.read_text()); pin["definition_sha256"] = "0" * 64
            pinfile.write_text(json.dumps(pin))
            with self.assertRaises(LibraryError): read_pack(library, target)
            pin["definition_sha256"] = kit["definition_sha256"]; pinfile.write_text(json.dumps(pin))
            authority = target / kit["authority_file"]
            other = Path(tmp) / "outside.json"; authority.rename(other); authority.symlink_to(other)
            with self.assertRaises(LibraryError): read_pack(library, target)
