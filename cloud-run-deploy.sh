#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# cloud-run-deploy.sh
# Deploy the Ridhi Command Center to Google Cloud Run
#
# Usage:
#   export PROJECT_ID=my-gcp-project
#   export GEMINI_API_KEY=AIza...
#   ./cloud-run-deploy.sh
#
# Optional overrides (all have sensible defaults):
#   REGION          GCP region            (default: us-central1)
#   SERVICE_NAME    Cloud Run service      (default: ridhi-command-center)
#   IMAGE_NAME      Image name            (default: ridhi-command-center)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── Required variables ───────────────────────────────────────────────────────
: "${PROJECT_ID:?PROJECT_ID must be set}"
: "${GEMINI_API_KEY:?GEMINI_API_KEY must be set}"

# ── Optional variables with defaults ────────────────────────────────────────
REGION="${REGION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-ridhi-command-center}"
IMAGE_NAME="${IMAGE_NAME:-ridhi-command-center}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

IMAGE_URI="gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "╔══════════════════════════════════════════════════════╗"
echo "║      Ridhi Command Center – Cloud Run Deploy         ║"
echo "╚══════════════════════════════════════════════════════╝"
echo "  Project  : ${PROJECT_ID}"
echo "  Region   : ${REGION}"
echo "  Service  : ${SERVICE_NAME}"
echo "  Image    : ${IMAGE_URI}"
echo ""

# ── 1. Authenticate & configure project ─────────────────────────────────────
echo "▶ Configuring gcloud project..."
gcloud config set project "${PROJECT_ID}"

# ── 2. Enable required APIs ──────────────────────────────────────────────────
echo "▶ Enabling required GCP APIs..."
gcloud services enable \
    run.googleapis.com \
    containerregistry.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com \
    --project="${PROJECT_ID}"

# ── 3. Store the Gemini API key in Secret Manager ────────────────────────────
echo "▶ Storing GEMINI_API_KEY in Secret Manager..."
if gcloud secrets describe gemini-api-key --project="${PROJECT_ID}" &>/dev/null; then
    echo "   Secret already exists – adding a new version."
    echo -n "${GEMINI_API_KEY}" | gcloud secrets versions add gemini-api-key \
        --data-file=- --project="${PROJECT_ID}"
else
    echo "   Creating new secret."
    echo -n "${GEMINI_API_KEY}" | gcloud secrets create gemini-api-key \
        --data-file=- \
        --replication-policy=automatic \
        --project="${PROJECT_ID}"
fi

# ── 4. Build the Docker image with Cloud Build ───────────────────────────────
echo "▶ Building Docker image with Cloud Build..."
gcloud builds submit \
    --tag="${IMAGE_URI}" \
    --project="${PROJECT_ID}" \
    .

# ── 5. Deploy to Cloud Run ───────────────────────────────────────────────────
echo "▶ Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
    --image="${IMAGE_URI}" \
    --platform=managed \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --allow-unauthenticated \
    --port=3000 \
    --memory=512Mi \
    --cpu=1 \
    --min-instances=0 \
    --max-instances=10 \
    --timeout=300 \
    --set-env-vars="NODE_ENV=production,BACKEND_PORT=8000" \
    --set-secrets="GEMINI_API_KEY=gemini-api-key:latest"

# ── 6. Print the service URL ─────────────────────────────────────────────────
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
    --platform=managed \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --format="value(status.url)")

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  Deployment complete!                                ║"
echo "╚══════════════════════════════════════════════════════╝"
echo "  Service URL : ${SERVICE_URL}"
echo "  Health check: ${SERVICE_URL}/api/health"
