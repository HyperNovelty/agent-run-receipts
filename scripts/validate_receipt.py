#!/usr/bin/env python3
"""Validate an Agent Run Receipt JSON file."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "receipt_id",
    "title",
    "date",
    "agent_type",
    "task_summary",
    "boundaries",
    "changed_files",
    "verification",
    "human_gate",
    "public_action_taken",
    "notes",
]

STRING_FIELDS = [
    "receipt_id",
    "title",
    "date",
    "agent_type",
    "task_summary",
    "notes",
]

ARRAY_FIELDS = ["boundaries", "changed_files", "verification"]

DEVELOPMENT_DELTA_REQUIRED = [
    "changed_artifacts",
    "capability_delta",
    "validation_evidence",
    "next_blocker_or_artifact",
    "non_actions_preserved",
]

STATUS_ONLY_PHRASES = [
    "no changes",
    "nothing changed",
    "status unchanged",
    "cron ran",
    "same as before",
    "validator still ok",
    "no new artifact",
]


def load_receipt(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_development_delta(delta: Any) -> list[str]:
    errors: list[str] = []
    if delta is None:
        return errors
    if not isinstance(delta, dict):
        return ["development_delta must be an object when present"]

    for field in DEVELOPMENT_DELTA_REQUIRED:
        if field not in delta:
            errors.append(f"development_delta missing required field: {field}")

    for field in ["changed_artifacts", "validation_evidence", "non_actions_preserved"]:
        if field in delta:
            value = delta[field]
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
                errors.append(f"development_delta.{field} must be a non-empty array of strings")

    for field in ["capability_delta", "next_blocker_or_artifact"]:
        if field in delta:
            value = delta[field]
            if not isinstance(value, str) or len(value.strip()) < 10:
                errors.append(f"development_delta.{field} must be a meaningful string")

    status = delta.get("status")
    if status is not None and status not in {"development_delta", "blocked_with_evidence", "not_a_delta"}:
        errors.append("development_delta.status must be development_delta, blocked_with_evidence, or not_a_delta")

    validation_text = " ".join(delta.get("validation_evidence", [])) if isinstance(delta.get("validation_evidence"), list) else ""
    if "validation_evidence" in delta and not any(marker in validation_text.lower() for marker in ["pass", "ok", "exit 0", "success", "failed as expected"]):
        errors.append("development_delta.validation_evidence should include an observable result such as pass, ok, exit 0, success, or failed as expected")

    searchable = " ".join(str(delta.get(field, "")) for field in ["capability_delta", "next_blocker_or_artifact"]).lower()
    if delta.get("status") != "not_a_delta" and any(phrase in searchable for phrase in STATUS_ONLY_PHRASES):
        errors.append("development_delta appears status-only; describe a concrete artifact/capability change or mark status not_a_delta")

    return errors


def validate_receipt(receipt: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(receipt, dict):
        return ["receipt must be a JSON object"]

    for field in REQUIRED_FIELDS:
        if field not in receipt:
            errors.append(f"missing required field: {field}")

    for field in STRING_FIELDS:
        if field in receipt and not isinstance(receipt[field], str):
            errors.append(f"{field} must be a string")

    for field in ARRAY_FIELDS:
        if field in receipt:
            if not isinstance(receipt[field], list):
                errors.append(f"{field} must be an array")
            elif not all(isinstance(item, str) for item in receipt[field]):
                errors.append(f"{field} items must be strings")

    if "public_action_taken" in receipt and not isinstance(receipt["public_action_taken"], bool):
        errors.append("public_action_taken must be a boolean")

    human_gate = receipt.get("human_gate")
    if "human_gate" in receipt and not isinstance(human_gate, dict):
        errors.append("human_gate must be an object")
    elif isinstance(human_gate, dict):
        status = human_gate.get("status")
        approval_note = human_gate.get("approval_note")
        if status is not None and not isinstance(status, str):
            errors.append("human_gate.status must be a string")
        if approval_note is not None and not isinstance(approval_note, str):
            errors.append("human_gate.approval_note must be a string")
        if receipt.get("public_action_taken") is True:
            if status != "approved" or not isinstance(approval_note, str) or not approval_note.strip():
                errors.append(
                    "public_action_taken true requires human_gate.status approved and a non-empty approval_note"
                )

    if "development_delta" in receipt:
        errors.extend(validate_development_delta(receipt.get("development_delta")))

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("FAIL: usage: validate_receipt.py path/to/receipt.json")
        return 2

    path = Path(argv[1])
    try:
        receipt = load_receipt(path)
    except OSError as exc:
        print(f"FAIL: could not read {path}: {exc}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid JSON: {exc}")
        return 1

    errors = validate_receipt(receipt)
    if errors:
        print("FAIL: " + "; ".join(errors))
        return 1

    print("PASS: receipt is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

