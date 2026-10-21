#!/usr/bin/env bash
# Deploy Fievel's hosted MCP server to Google Cloud Run with cost limits.
# Run from Cloud Shell inside a clone of the repository:  bash deploy/cloud-run.sh
set -euo pipefail

SERVICE=fievel-mcp
REGION=${REGION:-us-central1}
PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT" ]; then
  echo "No project selected. Run: gcloud config set project YOUR-PROJECT-ID" >&2
  exit 1
fi
cd "$(dirname "$0")/.."
echo "Deploying $SERVICE to project $PROJECT in $REGION"

gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# Cost limits: one instance at most, 256 MiB, CPU only during requests, 30 s timeout,
# scale to zero when idle. Public access because the directory calls it without sign-in;
# the server stores and logs no content.
gcloud run deploy "$SERVICE" --source . --region "$REGION" --allow-unauthenticated \
  --memory 256Mi --cpu 1 --cpu-throttling --max-instances 1 --min-instances 0 \
  --concurrency 10 --timeout 30 --quiet

URL=$(gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)')
echo
echo "Service URL: $URL"
echo "MCP endpoint: $URL/mcp"
echo "Health check:"
curl -fsS "$URL/healthz" && echo
