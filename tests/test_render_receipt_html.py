import unittest

from scripts.render_receipt_html import render_receipt
from tests.test_validate_receipt import valid_receipt


class RenderReceiptHtmlTests(unittest.TestCase):
    def test_render_includes_visible_boundary_status(self):
        html = render_receipt(valid_receipt())
        self.assertIn("Boundary and Status", html)
        self.assertIn("Human gate:", html)
        self.assertIn("Public action taken:", html)

    def test_render_escapes_text(self):
        receipt = valid_receipt()
        receipt["title"] = "<script>alert(1)</script>"
        receipt["boundaries"] = ["Use <safe> text"]
        html = render_receipt(receipt)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn("Use &lt;safe&gt; text", html)
        self.assertNotIn("<script>alert(1)</script>", html)

    def test_render_includes_development_delta_when_present(self):
        receipt = valid_receipt()
        receipt["development_delta"] = {
            "status": "development_delta",
            "changed_artifacts": ["scripts/validate_receipt.py"],
            "capability_delta": "Validator now checks concrete agent progress evidence.",
            "validation_evidence": ["python3 -m unittest discover -s tests -> OK"],
            "next_blocker_or_artifact": "Add more examples.",
            "non_actions_preserved": ["no deploy", "no secrets"],
        }
        html = render_receipt(receipt)
        self.assertIn("Development Delta", html)
        self.assertIn("scripts/validate_receipt.py", html)
        self.assertIn("Validator now checks concrete agent progress evidence.", html)


if __name__ == "__main__":
    unittest.main()

