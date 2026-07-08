# Development Delta Receipts

A normal agent-run receipt says what an agent did, what boundaries applied, what files changed, and what verification ran.

A **development delta receipt** adds one extra question:

> Did the agent actually improve a concrete artifact or capability, or did it only produce a nicer status report?

This extension is intentionally small. It is not a full compliance system, policy engine, or authorization layer. It is a public-safe pattern that maintainers can use before accepting AI-agent work.

## When to use it

Use `development_delta` when a receipt describes coding-agent, documentation-agent, scheduled-agent, or automation work that claims progress.

Good examples:

- A validator was changed and tests passed.
- A schema gained a new field and examples were updated.
- A documentation workflow added a new review checklist and link checks passed.
- A failed receipt or boundary case was added as a regression test.

Bad examples:

- “Cron ran.”
- “No changes.”
- “Validator still OK.”
- “Same counts as last time.”
- A summary was rewritten without a changed artifact or validation output.

## Minimal shape

```json
{
  "development_delta": {
    "status": "development_delta",
    "changed_artifacts": ["scripts/validate_receipt.py"],
    "capability_delta": "Validator now rejects status-only development claims when the optional delta section is present.",
    "validation_evidence": ["python3 -m unittest discover -s tests -> OK"],
    "next_blocker_or_artifact": "Add more synthetic examples after maintainer review.",
    "non_actions_preserved": ["no deploy", "no secrets", "no account action"]
  }
}
```

## Field guide

| Field | Meaning |
|---|---|
| `status` | `development_delta`, `blocked_with_evidence`, or `not_a_delta`. |
| `changed_artifacts` | Concrete public-safe paths or artifacts changed. |
| `capability_delta` | What improved now that those artifacts changed. |
| `validation_evidence` | Commands/checks with observable results: `OK`, `PASS`, `exit 0`, `failed as expected`, etc. |
| `next_blocker_or_artifact` | The next concrete decision, blocker, or artifact. |
| `non_actions_preserved` | Things the agent did not do: no deploy, no account action, no paid API, no secrets, no outreach. |

## Validator behavior

`validate_receipt.py` keeps `development_delta` optional for backwards compatibility.

When present, it checks that:

- required delta fields exist;
- artifact, validation, and non-action lists are non-empty arrays of strings;
- capability and next-artifact text are meaningful strings;
- validation evidence includes an observable result;
- status-only phrases such as “no changes,” “cron ran,” or “validator still ok” do not pass as a development delta.

Try the example:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_receipt.py examples/development-delta-receipt.example.json
```

Expected result:

```text
PASS: receipt is valid
```

Run the full test suite:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

## Boundary

This extension does not grant permission to publish, deploy, spend money, contact people, write to accounts, or store secrets. It only makes claimed agent progress easier to review.
