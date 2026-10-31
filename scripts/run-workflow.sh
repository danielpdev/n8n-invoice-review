#!/bin/sh
set -eu
docker compose up -d --build mock
docker compose run --rm n8n import:workflow --input=/workflows/main.json
docker compose run --rm n8n execute --id=n8ninvoicereview --rawOutput
