import unittest

from scripts.validate_receipt import validate_receipt


def valid_receipt():
    return {
        "receipt_id": "arr-test-001",
        "title": "Synthetic Test",
        "date": "2026-07-06",
        "agent_type": "local coding agent",
        "task_summary": "Synthetic test task.",
        "boundaries": ["local only"],
        "changed_files": ["README.md"],
        "verification": ["python3 -m unittest"],
        "human_gate": {"status": "pending", "approval_note": ""},
        "public_action_taken": False,
        "notes": "Synthetic test receipt.",
    }


class ValidateReceiptTests(unittest.TestCase):
    def test_valid_receipt_passes(self):
        self.assertEqual(validate_receipt(valid_receipt()), [])

    def test_missing_required_field_fails(self):
        receipt = valid_receipt()
        del receipt["title"]
        self.assertIn("missing required field: title", validate_receipt(receipt))

    def test_public_action_requires_approval_note(self):
        receipt = valid_receipt()
        receipt["public_action_taken"] = True
        errors = validate_receipt(receipt)
        self.assertTrue(any("requires human_gate.status approved" in error for error in errors))

    def test_public_action_with_approval_passes(self):
        receipt = valid_receipt()
        receipt["public_action_taken"] = True
        receipt["human_gate"] = {"status": "approved", "approval_note": "Approved by maintainer."}
        self.assertEqual(validate_receipt(receipt), [])

    def test_array_type_required(self):
        receipt = valid_receipt()
        receipt["verification"] = "python3 -m unittest"
        self.assertIn("verification must be an array", validate_receipt(receipt))

    def test_development_delta_extension_passes(self):
        receipt = valid_receipt()
        receipt["development_delta"] = {
            "status": "development_delta",
            "changed_artifacts": ["scripts/validate_receipt.py", "docs/development-delta-receipts.md"],
            "capability_delta": "Validator now checks a concrete development-delta extension when present.",
            "validation_evidence": ["python3 -m unittest discover -s tests exit 0 OK"],
            "next_blocker_or_artifact": "Add more synthetic examples after maintainer review.",
            "non_actions_preserved": ["no deploy", "no account action", "no secrets"],
        }
        self.assertEqual(validate_receipt(receipt), [])

    def test_development_delta_extension_rejects_status_only(self):
        receipt = valid_receipt()
        receipt["development_delta"] = {
            "status": "development_delta",
            "changed_artifacts": ["README.md"],
            "capability_delta": "Status unchanged; validator still ok.",
            "validation_evidence": ["python3 -m unittest discover -s tests exit 0 OK"],
            "next_blocker_or_artifact": "No new artifact remains.",
            "non_actions_preserved": ["no deploy"],
        }
        errors = validate_receipt(receipt)
        self.assertTrue(any("status-only" in error for error in errors))

    def test_development_delta_extension_requires_validation_result(self):
        receipt = valid_receipt()
        receipt["development_delta"] = {
            "status": "development_delta",
            "changed_artifacts": ["README.md"],
            "capability_delta": "A concrete capability changed in a reviewable artifact.",
            "validation_evidence": ["python3 -m unittest discover -s tests"],
            "next_blocker_or_artifact": "Add more examples.",
            "non_actions_preserved": ["no deploy"],
        }
        errors = validate_receipt(receipt)
        self.assertTrue(any("observable result" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

