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
        return '<p class="empty">Not provided as a list.</p>'
    if not items:
        return '<p class="empty">None listed.</p>'
    return '<ul class="check-list">' + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_development_delta(delta: Any) -> str:
    if not isinstance(delta, dict):
        return ""
    status = delta.get("status", "not provided")
    return f"""
    <section class="wide development-delta">
      <h2>Development Delta</h2>
      <p><span class="label">Status:</span> {esc(status)}</p>
      <h3>Changed Artifacts</h3>
      {render_list(delta.get("changed_artifacts", []))}
      <h3>Capability Delta</h3>
      <p>{esc(delta.get("capability_delta", ""))}</p>
      <h3>Validation Evidence</h3>
      {render_list(delta.get("validation_evidence", []))}
      <h3>Next Blocker or Artifact</h3>
      <p>{esc(delta.get("next_blocker_or_artifact", ""))}</p>
      <h3>Non-actions Preserved</h3>
      {render_list(delta.get("non_actions_preserved", []))}
    </section>
"""


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
    :root {{ color-scheme: dark; --ink: #f7ead7; --muted: #d7c2a2; --paper: #fff7e8; --paper-ink: #261b12; --line: #6f5840; --accent: #f2b66d; --warn: #ffd08a; --panel: #352417; }}
    * {{ box-sizing: border-box; }}
    body {{ color: var(--ink); font-family: Georgia, "Times New Roman", serif; line-height: 1.6; margin: 0; background: #20150f; }}
    body::before {{ content: ""; position: fixed; inset: 0; pointer-events: none; background: radial-gradient(circle at top left, rgba(242, 182, 109, 0.16), transparent 34rem); }}
    main {{ max-width: 1080px; margin: 0 auto; padding: 32px 18px 44px; position: relative; }}
    header {{ border: 1px solid var(--line); border-radius: 8px; margin-bottom: 18px; padding: 24px; background: linear-gradient(135deg, #3a2617, #251810); box-shadow: 0 18px 50px rgba(0,0,0,0.25); }}
    h1 {{ color: var(--ink); font-size: clamp(2rem, 5vw, 4rem); line-height: 0.98; margin: 10px 0 14px; letter-spacing: 0; }}
    h2 {{ color: var(--paper-ink); font-size: 1.02rem; line-height: 1.2; margin: 0 0 10px; }}
    h3 {{ color: var(--paper-ink); font-family: Arial, Helvetica, sans-serif; font-size: 0.82rem; margin: 16px 0 8px; text-transform: uppercase; }}
    p {{ margin: 0; }}
    section, .meta-card {{ background: var(--paper); border: 1px solid #dfcaa8; border-radius: 8px; color: var(--paper-ink); padding: 18px; }}
    .eyebrow {{ color: var(--accent); font-family: Arial, Helvetica, sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip {{ border: 1px solid rgba(255,255,255,0.28); border-radius: 999px; color: var(--ink); display: inline-flex; font-family: Arial, Helvetica, sans-serif; font-size: 0.78rem; font-weight: 700; padding: 6px 10px; }}
    .chip.warn {{ background: rgba(255, 208, 138, 0.18); color: #ffe2ac; }}
    .chip.neutral {{ background: rgba(255,255,255,0.08); }}
    .meta-grid {{ display: grid; gap: 12px; grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 18px 0; }}
    .meta-card dt {{ color: #735230; font-family: Arial, Helvetica, sans-serif; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }}
    .meta-card dd {{ margin: 4px 0 0; font-weight: 700; }}
    .section-grid {{ display: grid; gap: 14px; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .section-grid section.wide {{ grid-column: 1 / -1; }}
    .boundary-status {{ border-color: #d99745; background: #fff1d6; }}
    .label {{ color: #735230; font-family: Arial, Helvetica, sans-serif; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }}
    .status-line {{ display: grid; gap: 8px; margin: 10px 0; }}
    .check-list {{ margin: 0; padding-left: 1.2rem; }}
    .check-list li {{ margin: 0.45rem 0; padding-left: 0.15rem; }}
    .empty {{ color: #7a6a55; font-style: italic; }}
    footer {{ color: var(--muted); font-family: Arial, Helvetica, sans-serif; font-size: 0.9rem; margin-top: 18px; }}
    @media (max-width: 760px) {{ .meta-grid, .section-grid {{ grid-template-columns: 1fr; }} header {{ padding: 20px; }} }}
    @media print {{ body {{ background: #fff; color: #000; }} body::before {{ display: none; }} main {{ max-width: none; padding: 0; }} header, section, .meta-card {{ box-shadow: none; break-inside: avoid; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Hypernovelty Open Lab / Agent Run Receipt</p>
      <h1>{esc(receipt.get("title", ""))}</h1>
      <div class="chips" aria-label="Receipt status">
        <span class="chip warn">Human gate: {esc(status)}</span>
        <span class="chip neutral">Public action: {esc(public_action)}</span>
        <span class="chip neutral">Synthetic example</span>
      </div>
    </header>

    <dl class="meta-grid" aria-label="Receipt metadata">
      <div class="meta-card"><dt>Receipt ID</dt><dd>{esc(receipt.get("receipt_id", ""))}</dd></div>
      <div class="meta-card"><dt>Date</dt><dd>{esc(receipt.get("date", ""))}</dd></div>
      <div class="meta-card"><dt>Agent type</dt><dd>{esc(receipt.get("agent_type", ""))}</dd></div>
    </dl>

    <div class="section-grid">
    <section class="boundary-status wide">
      <h2>Boundary and Status</h2>
      <div class="status-line">
        <p><span class="label">Human gate:</span> {esc(status)}</p>
        <p><span class="label">Approval note:</span> {esc(approval_note) if approval_note else "None recorded"}</p>
        <p><span class="label">Public action taken:</span> {esc(public_action)}</p>
      </div>
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

    <section class="wide">
      <h2>Notes</h2>
      <p>{esc(receipt.get("notes", ""))}</p>
    </section>
{render_development_delta(receipt.get("development_delta"))}
    </div>
    <footer>This receipt is a local synthetic review aid. It is not an approval, deployment record, audit attestation, or permission to publish.</footer>
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
