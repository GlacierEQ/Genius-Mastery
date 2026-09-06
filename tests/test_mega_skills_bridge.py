import copy
import json
from pathlib import Path
import subprocess
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = ROOT / "interfaces" / "mega-skills-bridge.json"
BRIDGE_SCHEMA_PATH = ROOT / "schemas" / "mega-skills-bridge.schema.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class MegaSkillsBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bridge = load_json(BRIDGE_PATH)
        cls.bridge_schema = load_json(BRIDGE_SCHEMA_PATH)
        Draft202012Validator.check_schema(cls.bridge_schema)
        cls.validator = Draft202012Validator(cls.bridge_schema)

    def assert_bridge_valid(self, bridge):
        errors = sorted(self.validator.iter_errors(bridge), key=lambda error: list(error.path))
        self.assertFalse(
            errors,
            "bridge schema errors:\n" + "\n".join(error.message for error in errors),
        )

    def assert_bridge_invalid(self, bridge):
        self.assertTrue(list(self.validator.iter_errors(bridge)))

    def test_bridge_matches_operating_loop_contract(self):
        bridge = self.bridge
        schema = load_json(ROOT / "schemas" / "operating-loop.schema.json")
        self.assertEqual(
            bridge["compatibility"]["operating_loop_schema_version"],
            schema["properties"]["schema_version"]["const"],
        )
        self.assertEqual(bridge["phase_order"], list(schema["properties"]["phases"]["required"]))
        self.assertEqual(bridge["evidence_states"], schema["properties"]["evidence_state"]["enum"])
        self.assertEqual(bridge["outcome_statuses"], schema["properties"]["outcome_status"]["enum"])
        self.assertEqual(bridge["status_map"]["verified"], "verified")
        self.assertEqual(bridge["consumer"]["combo_id"], "mission-aware-operating-loop")
        self.assert_bridge_valid(bridge)

    def test_bridge_schema_reference_resolves(self):
        declared = self.bridge["$schema"]
        self.assertFalse(declared.startswith("http://"))
        resolved = (BRIDGE_PATH.parent / declared).resolve()
        self.assertEqual(resolved, BRIDGE_SCHEMA_PATH.resolve())
        self.assertTrue(resolved.is_file())

    def test_bridge_schema_rejects_compatibility_drift(self):
        mutations = {
            "duplicate route": lambda bridge: bridge["consumer"].update(
                mega_routes=["apex-adaptive-operations", "apex-adaptive-operations"]
            ),
            "invalid phase": lambda bridge: bridge["phase_order"].__setitem__(0, "decide"),
            "missing status mapping": lambda bridge: bridge["status_map"].pop("verified"),
            "extra status mapping": lambda bridge: bridge["status_map"].update(extra="verified"),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                candidate = copy.deepcopy(self.bridge)
                mutate(candidate)
                self.assert_bridge_invalid(candidate)

    def test_bridge_pin_is_a_commit_and_blob_identity(self):
        provider = self.bridge["provider"]
        for key in ("ref", "module_blob_sha", "schema_blob_sha"):
            self.assertRegex(provider[key], r"^[0-9a-f]{40}$")

        commit = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "--verify", f"{provider['ref']}^{{commit}}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(commit, provider["ref"])

        for key, path in (
            ("module_blob_sha", provider["module"]),
            ("schema_blob_sha", provider["schema"]),
        ):
            actual = subprocess.run(
                ["git", "-C", str(ROOT), "rev-parse", f"{provider['ref']}:{path}"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            self.assertEqual(actual, provider[key])


if __name__ == "__main__":
    unittest.main()
