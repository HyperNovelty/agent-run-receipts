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


if __name__ == "__main__":
    unittest.main()

