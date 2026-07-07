# Public-Safety Boundary

Agent Run Receipts are documentation artifacts. They help people see what was requested, what constraints were named, what changed, what verification ran, and whether human approval is still needed.

They are not:

- a compliance product
- legal advice
- a substitute for security review
- an authorization mechanism by themselves
- a private trace archive
- a place to store secrets, credentials, customer data, or proprietary internals

For public-facing receipts, use synthetic examples or carefully reviewed summaries. Do not include private workspace paths, unpublished traces, access tokens, account identifiers, or sensitive operational detail.

If a receipt says public action was taken, the validator requires explicit human approval status and a non-empty approval note. That requirement is a minimal guardrail, not proof that the action was appropriate.

