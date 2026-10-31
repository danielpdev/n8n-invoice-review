# Demo walkthrough

## Start

```bash
make setup
make demo
make test
make eval
```

## What to show

n8n submits an invoice into a durable review queue. Vendor plus invoice number detect duplicates. Integer cents validate totals. A separate explicit operator approval archives the invoice transactionally.

## Failure case to discuss

Duplicate intake, replayed approval, missing human confirmation and incorrect totals. The intake workflow ran in n8n; approval/archive behavior is exercised by Python integration tests.

## Evidence

Open the JSON evaluation report alongside the implementation. Distinguish synthetic fixture outputs, synthetic trace timing, actual elapsed evaluation time, and local model inference. Do not present a tiny test set as a production benchmark.

## Closing tradeoff

The shipped n8n workflow stops at the human review queue. Review uses the local API documentation; it does not impersonate a human with an automatic approval node. Incorrect invoices require correction in a future revision flow.

The repository's `docs/demo.webm` or `docs/demo.mp4`, when present, records the demonstration. A terminal replay is also available for focused projects as `docs/demo.cast`.
