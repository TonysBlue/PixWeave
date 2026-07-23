# 织象 PixWeave

Standalone product repository for PixWeave's controlled image generation and editing workflows.

## Boundaries

- Source, tests, product documentation, non-sensitive examples, and deployment templates live here.
- Runtime artifacts, sessions, feedback, and logs live under `/home/tony/product-data/pixweave` and are not committed.
- Company governance, CEO runtime, task scheduling, approvals, and audit state live in `TonysBlue/agent-company`.

## Verify

```bash
python3.11 -m unittest discover -s tests -v
python3.11 -m pixweave --help
```

## Run Local Beta

```bash
python3.11 -m pixweave beta-product --host 127.0.0.1 --port 18112
```

This repository does not authorize external publication, customer outreach, pricing, payment, production deployment, or legal commitments.
