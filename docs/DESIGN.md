# Design record

## Decision

n8n submits an invoice into a durable review queue. Vendor plus invoice number detect duplicates. Integer cents validate totals. A separate explicit operator approval archives the invoice transactionally.

## Failure model

Duplicate intake, replayed approval, missing human confirmation and incorrect totals. The intake workflow ran in n8n; approval/archive behavior is exercised by Python integration tests.

## Tradeoffs

The shipped n8n workflow stops at the human review queue. Review uses the local API documentation; it does not impersonate a human with an automatic approval node. Incorrect invoices require correction in a future revision flow.

## Next change to defend in review

Add a dedicated review form and a versioned correction endpoint, then a real document store adapter.

## Reproducibility

`uv.lock` pins Python dependencies; the web lockfile pins the React build where present. Model-backed evaluations use a separately installed local service. Dataset examples are synthetic and intentionally small. Reported timing is a local observation, not a throughput SLA. Run `make test` after changing state transitions and `make eval` after changing decisions. Keep inference quality separate from deterministic invariant checks.
