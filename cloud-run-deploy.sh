#!/usr/bin/env bash
# cloud-run-deploy.sh
# One-command script to build, push, and deploy student-ai-automation to Cloud Run.
#
# Usage:
#   chmod +x cloud-run-deploy.sh
#   ./cloud-run-deploy.sh
#
# Prerequisites:
#   - gcloud CLI installed and authenticated  (gcloud auth login)
#   - Docker installed and configured         (gcloud auth configure-docker gcr.io)
#   - GEMINI_API_KEY set in your shell or via Secret Manager

set -euo pipefail

# ─────────────────────────────────────────────────────────────
# Configuration – override any variable by exporting it before
# running this script.
# ─────────────────────────────────────────────────────────────
PROJECT_ID="${PROJECT_ID:-gen-lang-client-0581494231}"
SERVICE_NAME="${SERVICE_NAME:-student-ai-automation}"
REGION="${REGION:-us-central1}"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
TAG="${TAG:-$(git rev-parse --short HEAD 2>/dev/null || echo latest)}"
MEMORY="${MEMORY:-512Mi}"
CPU="${CPU:-1}"
MAX_INSTANCES="${MAX_INSTANCES:-10}"
MIN_INSTANCES="${MIN_INSTANCES:-0}"
PORT="${PORT:-3000}"

# Gemini API key: read from env or Secret Manager
GEMINI_API_KEY="${GEMINI_API_KEY:-}"

# ─────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────
log()  { echo "==> $*"; }
die()  { echo "ERROR: $*" >&2; exit 1; }

# ─────────────────────────────────────────────────────────────
# 1. Preflight checks
# ─────────────────────────────────────────────────────────────
log "Checking prerequisites..."
command -v gcloud >/dev/null 2>&1 || die "gcloud CLI not found. Install from https://cloud.google.com/sdk/docs/install"
command -v docker  >/dev/null 2>&1 || die "Docker not found. Install from https://docs.docker.com/get-docker/"

# Verify Docker can reach GCR
gcloud auth configure-docker gcr.io --quiet

# Set active project
gcloud config set project "${PROJECT_ID}"

# ─────────────────────────────────────────────────────────────
# 2. Build Docker image
# ─────────────────────────────────────────────────────────────
log "Building Docker image ${IMAGE}:${TAG} ..."
docker build \
  --platform linux/amd64 \
  -t "${IMAGE}:${TAG}" \
  -t "${IMAGE}:latest" \
  .

# ─────────────────────────────────────────────────────────────
# 3. Push to Google Container Registry
# ─────────────────────────────────────────────────────────────
log "Pushing image to gcr.io ..."
docker push "${IMAGE}:${TAG}"
docker push "${IMAGE}:latest"

# ─────────────────────────────────────────────────────────────
# 4. Resolve Gemini API key
# ─────────────────────────────────────────────────────────────
if [[ -z "${GEMINI_API_KEY}" ]]; then
  log "GEMINI_API_KEY not set in env – attempting to read from Secret Manager..."
  GEMINI_API_KEY=$(gcloud secrets versions access latest --secret="gemini-api-key" --project="${PROJECT_ID}" 2>/dev/null) || \
    die "Could not read GEMINI_API_KEY. Either export it or store it in Secret Manager as 'gemini-api-key'."
fi

# ─────────────────────────────────────────────────────────────
# 5. Deploy to Cloud Run
# ─────────────────────────────────────────────────────────────
log "Deploying ${SERVICE_NAME} to Cloud Run (${REGION})..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE}:${TAG}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --port "${PORT}" \
  --memory "${MEMORY}" \
  --cpu "${CPU}" \
  --min-instances "${MIN_INSTANCES}" \
  --max-instances "${MAX_INSTANCES}" \
  --set-env-vars "NODE_ENV=production,PYTHONUNBUFFERED=1,PORT=${PORT},GEMINI_API_KEY=${GEMINI_API_KEY}" \
  --project "${PROJECT_ID}"

# ─────────────────────────────────────────────────────────────
# 6. Retrieve and verify the service URL
# ─────────────────────────────────────────────────────────────
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
  --region "${REGION}" \
  --project "${PROJECT_ID}" \
  --format 'value(status.url)')

log "Service deployed at: ${SERVICE_URL}"

log "Verifying health endpoint..."
for i in 1 2 3 4 5; do
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${SERVICE_URL}/health" || true)
  if [[ "${HTTP_STATUS}" == "200" ]]; then
    log "Health check passed (HTTP ${HTTP_STATUS})."
    break
  fi
  log "Health check attempt ${i} returned HTTP ${HTTP_STATUS}. Retrying in 10s..."
  sleep 10
done

log ""
log "✅ Deployment complete!"
log "   App URL : ${SERVICE_URL}"
log "   Health  : ${SERVICE_URL}/health"
log ""
log "Stream logs with:"
log "  gcloud run services logs read ${SERVICE_NAME} --region ${REGION} --follow"
