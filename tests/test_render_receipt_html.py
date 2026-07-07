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


if __name__ == "__main__":
    unittest.main()

