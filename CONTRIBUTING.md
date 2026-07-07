# Contributing

Contributions should keep the project small, sober, and usable without third-party dependencies.

Guidelines:

- use Python standard library only for scripts and tests
- keep examples synthetic
- do not add network calls, account integrations, deployment logic, or telemetry
- do not include secrets, private traces, or private machine paths
- prefer plain language over policy theater
- add focused tests for validator and renderer behavior

Before proposing a change, run:

```bash
python3 scripts/validate_receipt.py examples/agent-run-receipt.example.json
python3 scripts/render_receipt_html.py examples/agent-run-receipt.example.json /tmp/agent-run-receipt-example.html
python3 -m unittest discover -s tests
git diff --check
```

