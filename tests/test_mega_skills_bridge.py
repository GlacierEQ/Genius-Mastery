import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class MegaSkillsBridgeTests(unittest.TestCase):
    def test_bridge_matches_operating_loop_contract(self):
        bridge = json.loads((ROOT / "interfaces" / "mega-skills-bridge.json").read_text())
        schema = json.loads((ROOT / "schemas" / "operating-loop.schema.json").read_text())
        self.assertEqual(bridge["compatibility"]["operating_loop_schema_version"], schema["properties"]["schema_version"]["const"])
        self.assertEqual(bridge["phase_order"], list(schema["properties"]["phases"]["required"]))
        self.assertEqual(bridge["evidence_states"], schema["properties"]["evidence_state"]["enum"])
        self.assertEqual(bridge["outcome_statuses"], schema["properties"]["outcome_status"]["enum"])
        self.assertEqual(bridge["status_map"]["verified"], "verified")
        self.assertEqual(bridge["consumer"]["combo_id"], "mission-aware-operating-loop")

    def test_bridge_pin_is_a_commit_and_blob_hashes(self):
        bridge = json.loads((ROOT / "interfaces" / "mega-skills-bridge.json").read_text())
        provider = bridge["provider"]
        for key in ("ref", "module_blob_sha", "schema_blob_sha"):
            self.assertRegex(provider[key], r"^[0-9a-f]{40}$")

if __name__ == "__main__":
    unittest.main()
