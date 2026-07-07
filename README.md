# Agent Run Receipts

Agent Run Receipts is a local-only starter repo for documenting a bounded AI or coding-agent run without publishing private traces. A receipt records what the agent was asked to do, what boundaries applied, which files changed, what verification ran, whether a human gate is still needed, and whether any public action was taken.

The goal is practical accountability for public-good work. Receipts help maintainers, reviewers, grant teams, community labs, and operators understand the shape of an agent-assisted change without requiring access to chat logs, credentials, proprietary systems, or internal workspaces.

## Why Receipts Matter

Agent work can move quickly. A short receipt gives humans a durable checkpoint:

- the task and boundaries are visible
- changed files are listed in a compact form
- verification is separated from claims
- public action is explicitly gated
- remaining approval needs are documented

This repo is intentionally small so it can be copied into local workflows, adapted, or used as a teaching artifact.

## Quick Start

Validate the synthetic example:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_receipt.py examples/agent-run-receipt.example.json
```

Render it to a checked-in demo HTML file:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/render_receipt_html.py examples/agent-run-receipt.example.json examples/rendered/agent-run-receipt.example.html
```

Run tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

Open `START_HERE.html` for a simple local overview.

Before sharing a receipt outside the trusted workspace, use `docs/publish-safety-reviewer-checklist.md`.

## Receipt Shape

Receipts are JSON objects with these required fields:

- `receipt_id`
- `title`
- `date`
- `agent_type`
- `task_summary`
- `boundaries`
- `changed_files`
- `verification`
- `human_gate`
- `public_action_taken`
- `notes`

The `boundaries`, `changed_files`, and `verification` fields are arrays. `public_action_taken` is a boolean. If `public_action_taken` is `true`, validation fails unless `human_gate.status` is exactly `approved` and `human_gate.approval_note` is non-empty.

## What This Repo Does Not Do

This is not a compliance product, legal advice, a policy engine, or an authorization mechanism by itself. It does not prove that a task was safe, complete, lawful, or approved. It does not collect secrets, private traces, prompts, account data, or credentials.

Use synthetic examples in public materials. Keep private workspace paths, internal customer data, proprietary traces, and security-sensitive details out of receipts intended for sharing.

For a practical publication review pass, see `docs/publish-safety-reviewer-checklist.md`.

## Local-Only Boundary

The scripts use Python standard library only. They do not call external APIs, create accounts, publish files, deploy services, or transmit receipt contents. Any sharing decision must happen outside this repo and should require explicit human review.

## Open Lab Fit

This repo is part of the Hypernovelty Open Lab public proof footprint. See `docs/open-lab-positioning.md` for how receipts relate to the umbrella kit, workflow screens, source cards, verification literacy labs, and school readiness review.
