#!/usr/bin/env python3
"""Render an Agent Run Receipt JSON file as simple local HTML."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from typing import Any

try:
    from validate_receipt import validate_receipt
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from validate_receipt import validate_receipt


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def render_list(items: Any) -> str:
    if not isinstance(items, list):
        return "<p>Not provided as a list.</p>"
    if not items:
        return "<p>None listed.</p>"
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_receipt(receipt: dict[str, Any]) -> str:
    human_gate = receipt.get("human_gate", {})
    if not isinstance(human_gate, dict):
        human_gate = {}
    status = human_gate.get("status", "unknown")
    approval_note = human_gate.get("approval_note", "")
    public_action = "yes" if receipt.get("public_action_taken") is True else "no"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(receipt.get("title", "Agent Run Receipt"))}</title>
  <style>
    body {{ font-family: Arial, sans-serif; line-height: 1.5; margin: 2rem; color: #1f2933; }}
    main {{ max-width: 860px; }}
    section {{ border-top: 1px solid #d9e2ec; padding-top: 1rem; margin-top: 1rem; }}
    .boundary-status {{ border: 2px solid #52606d; border-left-width: 8px; padding: 1rem; background: #f5f7fa; }}
    .label {{ font-weight: bold; }}
  </style>
</head>
<body>
  <main>
    <h1>{esc(receipt.get("title", ""))}</h1>
    <p><span class="label">Receipt ID:</span> {esc(receipt.get("receipt_id", ""))}</p>
    <p><span class="label">Date:</span> {esc(receipt.get("date", ""))}</p>
    <p><span class="label">Agent type:</span> {esc(receipt.get("agent_type", ""))}</p>

    <section class="boundary-status">
      <h2>Boundary and Status</h2>
      <p><span class="label">Human gate:</span> {esc(status)}</p>
      <p><span class="label">Approval note:</span> {esc(approval_note)}</p>
      <p><span class="label">Public action taken:</span> {esc(public_action)}</p>
      <h3>Boundaries</h3>
      {render_list(receipt.get("boundaries", []))}
    </section>

    <section>
      <h2>Task Summary</h2>
      <p>{esc(receipt.get("task_summary", ""))}</p>
    </section>

    <section>
      <h2>Changed Files</h2>
      {render_list(receipt.get("changed_files", []))}
    </section>

    <section>
      <h2>Verification</h2>
      {render_list(receipt.get("verification", []))}
    </section>

    <section>
      <h2>Notes</h2>
      <p>{esc(receipt.get("notes", ""))}</p>
    </section>
  </main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("FAIL: usage: render_receipt_html.py input.json output.html")
        return 2

    input_path = Path(argv[1])
    output_path = Path(argv[2])

    try:
        with input_path.open("r", encoding="utf-8") as handle:
            receipt = json.load(handle)
    except OSError as exc:
        print(f"FAIL: could not read {input_path}: {exc}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid JSON: {exc}")
        return 1

    errors = validate_receipt(receipt)
    if errors:
        print("FAIL: " + "; ".join(errors))
        return 1

    output_path.write_text(render_receipt(receipt), encoding="utf-8")
    print(f"PASS: wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

