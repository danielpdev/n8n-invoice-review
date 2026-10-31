# n8n Invoice Review

Duplicate-safe invoice intake, review and local archive.

[![verification](https://github.com/danielpdev/n8n-invoice-review/actions/workflows/ci.yml/badge.svg)](https://github.com/danielpdev/n8n-invoice-review/actions/workflows/ci.yml)

**Role focus:** n8n / Finance Operations Automation. **Status:** working local portfolio implementation, with synthetic data.

## Demo

![How n8n Invoice Review works](docs/demo.gif)

Edited replay of captured CLI outputs in deterministic fixture mode. This is not live model inference. [Full recording](docs/demo.mp4). Rebuild with `./scripts/render_gif.sh` (FFmpeg required).

## The engineering decision

n8n submits an invoice into a durable review queue. Vendor plus invoice number detect duplicates. Integer cents validate totals. A separate explicit operator approval archives the invoice transactionally.

```mermaid
flowchart LR
  n8n_intake --> Duplicate_check; Duplicate_check --> Arithmetic_validation; Arithmetic_validation --> Human_review_queue; Operator_approval --> Local_archive
```

## Run locally

Requirements: Python 3.12, [uv](https://docs.astral.sh/uv/getting-started/installation/) and Make.

```bash
git clone https://github.com/danielpdev/n8n-invoice-review.git
cd n8n-invoice-review
make setup
make demo
make test
make eval
```

`make demo` uses an isolated temporary database where relevant, so it is safe to repeat. `make eval` writes a timestamped report to `reports/evaluation-fixture.json`. Fixture mode is deterministic and does not represent model inference. There is no recurring hosting or API subscription cost.

`make serve` opens the local API on `http://127.0.0.1:8113/docs`.

### Execute the real n8n workflow

With Docker Engine + Compose (or Colima on macOS):

```bash
./scripts/run-workflow.sh
```

This builds the local mock API, imports `workflows/main.json`, then executes it through n8n's CLI. `reports/n8n-execution.json` contains the measured node results from an actual run. To inspect visually, run `docker compose up -d n8n`, open `http://localhost:5679`, complete local owner setup, and import the workflow JSON. No credentials are embedded.

All destinations point to the local `mock` service. No real CRM, email, Slack or customer system is contacted. Stop only this project's containers with `docker compose down`; data volumes are retained.

[Watch the recorded demo](docs/demo.mp4) · [Reproduce the walkthrough](docs/DEMO.md)

## Verification and evidence

Duplicate intake, replayed approval, missing human confirmation and incorrect totals. The intake workflow ran in n8n; approval/archive behavior is exercised by Python integration tests.

- [Evaluation report](reports/evaluation-fixture.json) — measured during an actual run; inspect the mode and dataset size.
- [Development and authorship](docs/DEVELOPMENT.md).
- [Romanian interview preparation](docs/INTERVIEW_RO.md).
- [Design notes](docs/DESIGN.md).
- [Demo walkthrough](docs/DEMO.md).

CI uses standard GitHub-hosted runners and deterministic tests without downloading LLM weights. The lockfiles record exact package versions. Local-model results, when present, live in `reports/evaluation-local.json`; hardware/model identities are in `reports/environment.json`.

## Limits and next iteration

The shipped n8n workflow stops at the human review queue. Review uses the local API documentation; it does not impersonate a human with an automatic approval node. Incorrect invoices require correction in a future revision flow.

Next: Add a dedicated review form and a versioned correction endpoint, then a real document store adapter.

The local demonstration does not include production authentication, secret management or operational service guarantees. Bind it to localhost and use synthetic data. These projects demonstrate engineering decisions; they do not claim real customers, paid production deployments or guaranteed interviews.

## Project ownership

Implemented with Codex assistance for Daniel Popa. The owner should review the code, run it, make an independent change and rehearse the tradeoffs before presenting it at interview. That human understanding check is pending and cannot be verified automatically. See [development notes](docs/DEVELOPMENT.md).

MIT for original source; dependencies/models retain their own licenses. See [third-party notices](THIRD_PARTY.md).
