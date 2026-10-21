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

# Source deploys build with the project's default compute service account. New projects
# (and organizations that disable automatic grants) give it no build permissions, so grant
# the Cloud Run Builder role, scoped to this project only. Safe to repeat.
NUMBER=$(gcloud projects describe "$PROJECT" --format='value(projectNumber)')
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${NUMBER}-compute@developer.gserviceaccount.com" \
  --role=roles/run.builder --condition=None --quiet >/dev/null
echo "Build service account has roles/run.builder"

# Cost limits: one instance at most, 256 MiB, CPU only during requests, 30 s timeout,
# scale to zero when idle. Public access because the directory calls it without sign-in;
# the server stores and logs no content. --no-invoker-iam-check makes it public without an
# allUsers grant, which organization policies often forbid.
gcloud run deploy "$SERVICE" --source . --region "$REGION" --no-invoker-iam-check \
  --memory 256Mi --cpu 1 --cpu-throttling --max-instances 1 --min-instances 0 \
  --concurrency 10 --timeout 30 --quiet

URL=$(gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)')
echo
echo "Service URL: $URL"
echo "MCP endpoint: $URL/mcp"
echo "Health check:"
curl -fsS "$URL/health" && echo
