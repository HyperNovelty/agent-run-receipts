# Publish-Safety Reviewer Checklist

Use this checklist before sharing an agent-run receipt outside the trusted workspace where it was created. A valid receipt is not automatically safe to publish.

## 1. Secrets And Credentials

- Confirm the receipt contains no passwords, tokens, API keys, session cookies, recovery codes, private keys, or account identifiers.
- Confirm verification notes do not quote secret-scan output in a way that reveals a secret-like value.
- Confirm links and filenames do not expose private dashboards, account consoles, or credential storage.

## 2. Private Traces And Local Context

- Remove prompts, tool logs, stack traces, chat excerpts, or agent traces unless they are synthetic and approved for public use.
- Replace private workspace paths with repo-relative paths or short public-safe descriptions.
- Avoid names of private clients, customers, students, sources, candidates, vendors, or internal systems.

## 3. Account And Public Actions

- Check `public_action_taken` and make sure it accurately states whether anything was pushed, deployed, published, emailed, submitted, purchased, or posted.
- If any public action happened, confirm a human approval status and approval note are present.
- Do not treat a receipt as authorization for an account action; it is only documentation.

## 4. Human Approval

- Confirm the named human gate is real for the local workflow and not just a placeholder.
- Record what still needs approval before public release.
- If the reviewer cannot verify the approval boundary, keep the receipt private or mark it as not ready to publish.

## 5. Source And Data Boundaries

- Confirm the receipt does not disclose proprietary source material, unpublished work, private datasets, customer data, or paid/private research data.
- Keep examples synthetic unless there is a clear right to share the material.
- Summarize sensitive verification results instead of copying private logs or raw evidence.

## 6. Final Publication Decision

- Open the rendered HTML as well as the JSON; both contain publishable text.
- Read every field as if it were indexed publicly.
- Publish only after the receipt is accurate, minimal, public-safe, and explicitly approved for the intended audience.
