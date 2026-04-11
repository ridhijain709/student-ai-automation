# 🚀 Deployment Guide - Ridhi Command Center

Complete guide for deploying the student-ai-automation application to Google Cloud Run.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Testing](#local-testing)
3. [Cloud Setup](#cloud-setup)
4. [Deployment Methods](#deployment-methods)
5. [Monitoring & Logs](#monitoring--logs)
6. [Troubleshooting](#troubleshooting)
7. [Scaling & Performance](#scaling--performance)

---

## Prerequisites

### Required Tools
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Google Cloud SDK**: [Install gcloud CLI](https://cloud.google.com/sdk/docs/install)
- **Git**: [Install Git](https://git-scm.com/)

### Required Accounts
- **Google Cloud Account** with billing enabled
- **Google Gemini API Key**: Get from [AI Studio](https://aistudio.google.com/apikey)

### Required APIs (Enable in Google Cloud Console)
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable compute.googleapis.com
```

---

## Local Testing

### Build Docker Image Locally

```bash
# Build the Docker image
docker build -t student-ai-automation:latest .

# Run the container
docker run -p 3000:3000 \
  -e GEMINI_API_KEY=AIzaSyAiKRvzZVI4zT30It595L7vzECg47y3MKM \
  -e NODE_ENV=production \
  student-ai-automation:latest

# Test the application
curl http://localhost:3000/health
curl http://localhost:3000/
```

### Verify Build Contents

```bash
# Check image size
docker images student-ai-automation:latest

# Run container and inspect
docker run -it student-ai-automation:latest sh

# View logs
docker logs -f <container-id>
```

---

## Cloud Setup

### 1. Authenticate with Google Cloud

```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project gen-lang-client-0581494231

# Verify authentication
gcloud auth list
```

### 2. Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com
```

### 3. Create Secret for Gemini API Key

```bash
# Create secret in Secret Manager
gcloud secrets create gemini-api-key \
  --replication-policy="automatic" \
  --data-file=- <<< "AIzaSyAiKRvzZVI4zT30It595L7vzECg47y3MKM"

# Grant access to Cloud Run service account
PROJECT_NUMBER=$(gcloud projects describe gen-lang-client-0581494231 --format='value(projectNumber)')

gcloud secrets add-iam-policy-binding gemini-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 4. Configure Docker Authentication

```bash
# Configure Docker to use gcloud as credential helper
gcloud auth configure-docker gcr.io
```

---

## Deployment Methods

### Method 1: Automatic Deployment (GitHub Actions)

**Easiest option - automatic deployment on every push to main branch**

```bash
# Push to main branch
git add .
git commit -m "Add deployment configuration"
git push origin main

# GitHub Actions will automatically:
# - Build Docker image
# - Push to gcr.io
# - Deploy to Cloud Run
```

**Setup GitHub Secrets** (if using GitHub Actions):
1. Go to Settings → Secrets and Variables → Actions
2. Add: `GEMINI_API_KEY` = `AIzaSyAiKRvzZVI4zT30It595L7vzECg47y3MKM`

### Method 2: Cloud Build (Recommended)

**Automatic deployment via Google Cloud Build**

```bash
# Enable Cloud Build GitHub integration
gcloud builds connect --name=student-ai-automation \
  --repository=ridhijain709/student-ai-automation \
  --branch-pattern=main

# Cloud Build will automatically deploy on every push to main
```

### Method 3: Manual Deployment Script

**Full control over deployment process**

```bash
# Make script executable
chmod +x cloud-run-deploy.sh

# Run deployment
./cloud-run-deploy.sh

# Output:
# - Docker image built
# - Image pushed to gcr.io
# - Service deployed to Cloud Run
# - Service URL displayed
```

### Method 4: Manual gcloud Command

**Direct deployment using gcloud CLI**

```bash
# Build and push Docker image
docker build -t gcr.io/gen-lang-client-0581494231/student-ai-automation:latest .
docker push gcr.io/gen-lang-client-0581494231/student-ai-automation:latest

# Deploy to Cloud Run
gcloud run deploy student-ai-automation \
  --image gcr.io/gen-lang-client-0581494231/student-ai-automation:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_API_KEY=AIzaSyAiKRvzZVI4zT30It595L7vzECg47y3MKM,NODE_ENV=production" \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

---

## Get Your Service URL

```bash
# Get the URL after deployment
gcloud run services describe student-ai-automation \
  --region us-central1 \
  --format 'value(status.url)'

# Output: https://student-ai-automation-xxxxx.run.app
```

---

## Monitoring & Logs

### View Live Logs

```bash
# Stream logs in real-time
gcloud run services logs read student-ai-automation \
  --region us-central1 \
  --follow

# View last 100 logs
gcloud run services logs read student-ai-automation \
  --region us-central1 \
  --limit 100
```

### Monitor Service Health

```bash
# View service details
gcloud run services describe student-ai-automation \
  --region us-central1

# Check service status
gcloud run services describe student-ai-automation \
  --region us-central1 \
  --format 'value(status.conditions[0].message)'

# View metrics in Google Cloud Console
# https://console.cloud.google.com/run/detail/us-central1/student-ai-automation/metrics
```

### Health Check

```bash
# Test health endpoint
curl https://student-ai-automation-xxxxx.run.app/health

# Expected response:
# {"status":"ok"}
```

---

## Troubleshooting

### Common Issues

#### 1. Deployment Fails: "Insufficient permission"

```bash
# Grant required permissions to Cloud Build service account
PROJECT_NUMBER=$(gcloud projects describe gen-lang-client-0581494231 --format='value(projectNumber)')

gcloud projects add-iam-policy-binding gen-lang-client-0581494231 \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding gen-lang-client-0581494231 \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

#### 2. Container Fails to Start

```bash
# View detailed logs
gcloud run services logs read student-ai-automation \
  --region us-central1 \
  --limit 50

# Test Docker image locally
docker run -e GEMINI_API_KEY=test student-ai-automation:latest

# Check Dockerfile syntax
docker build --progress=plain -t test:latest .
```

#### 3. API Key Not Working

```bash
# Verify secret is created
gcloud secrets list

# View secret value (be careful!)
gcloud secrets versions access latest --secret gemini-api-key

# Update secret if needed
echo "NEW_API_KEY" | gcloud secrets versions add gemini-api-key --data-file=-

# Redeploy after updating secret
gcloud run deploy student-ai-automation \
  --image gcr.io/gen-lang-client-0581494231/student-ai-automation:latest \
  --region us-central1 \
  --update-env-vars GEMINI_API_KEY=AIzaSyAiKRvzZVI4zT30It595L7vzECg47y3MKM
```

#### 4. Port Conflicts

```bash
# Ensure service uses port 3000
gcloud run services describe student-ai-automation \
  --region us-central1 \
  --format 'value(spec.template.spec.containers[0].ports[0].containerPort)'

# Update if needed
gcloud run services update student-ai-automation \
  --region us-central1 \
  --set-env-vars PORT=3000
```

---

## Scaling & Performance

### Adjust Auto-Scaling

```bash
# Set minimum instances (for faster cold start)
gcloud run services update student-ai-automation \
  --region us-central1 \
  --min-instances 1

# Set maximum instances
gcloud run services update student-ai-automation \
  --region us-central1 \
  --max-instances 20

# Adjust concurrency per instance
gcloud run services update student-ai-automation \
  --region us-central1 \
  --concurrency 100
```

### Update Memory & CPU

```bash
# Increase memory for faster processing
gcloud run services update student-ai-automation \
  --region us-central1 \
  --memory 1Gi \
  --cpu 2

# View current resources
gcloud run services describe student-ai-automation \
  --region us-central1 \
  --format 'value(spec.template.spec.resources)'
```

### View Metrics

```bash
# View CPU usage
gcloud monitoring time-series list \
  --filter='resource.service_name=student-ai-automation'

# View in Google Cloud Console
# https://console.cloud.google.com/run/detail/us-central1/student-ai-automation/metrics
```

---

## Managing Deployments

### Update Service

```bash
# Redeploy with new code
git push origin main

# Or manually redeploy
gcloud run deploy student-ai-automation \
  --image gcr.io/gen-lang-client-0581494231/student-ai-automation:latest \
  --region us-central1
```

### View Deployment History

```bash
# List all revisions
gcloud run revisions list --service student-ai-automation --region us-central1

# View revision details
gcloud run revisions describe student-ai-automation@REVISION_NAME --region us-central1
```

### Rollback to Previous Version

```bash
# Get revision name
gcloud run revisions list --service student-ai-automation --region us-central1

# Rollback
gcloud run services update-traffic student-ai-automation \
  --to-revisions REVISION_NAME=100 \
  --region us-central1
```

### Delete Service

```bash
# Delete the service
gcloud run services delete student-ai-automation \
  --region us-central1 \
  --quiet
```

---

## Cost Optimization

### Reduce Costs

```bash
# Set minimum instances to 0 for lower costs
gcloud run services update student-ai-automation \
  --region us-central1 \
  --min-instances 0

# Reduce memory usage
gcloud run services update student-ai-automation \
  --region us-central1 \
  --memory 256Mi

# Use us-central1 region (usually cheapest)
```

### Monitor Costs

```bash
# View Cloud Run costs in Google Cloud Console
# https://console.cloud.google.com/run?project=gen-lang-client-0581494231

# Export billing data
gcloud beta billing export-data --dataset=billing_dataset
```

---

## Environment Variables Reference

### Production Environment (.env.production)

```env
# Application
NODE_ENV=production
PYTHONUNBUFFERED=1
PORT=3000

# API Keys
GEMINI_API_KEY=AIzaSyAiKRvzZVI4zT30It595L7vzECg47y3MKM

# Database
DATABASE_URL=sqlite:///./data/ridhi.db

# URLs
APP_URL=https://student-ai-automation-xxxxx.run.app

# Features (all enabled by default)
ENABLE_GMAIL_INTEGRATION=true
ENABLE_TELEGRAM_INTEGRATION=true
ENABLE_LINKEDIN_ASSIST=true
ENABLE_WHATSAPP_SIMULATION=true
ENABLE_RESUME_AUTOMATION=true
ENABLE_TRUTHGRID=true
ENABLE_DASHBOARD=true
```

---

## Support

For issues or questions:
- Check Google Cloud Run documentation: https://cloud.google.com/run/docs
- View service logs: `gcloud run services logs read student-ai-automation --region us-central1 --follow`
- Google Cloud Support: https://cloud.google.com/support

---

## Next Steps

1. ✅ Verify local build works: `docker build -t test:latest .`
2. ✅ Deploy to Cloud Run using one of the methods above
3. ✅ Test health endpoint: `curl https://your-service-url/health`
4. ✅ Monitor logs: `gcloud run services logs read student-ai-automation --region us-central1 --follow`
5. ✅ Configure custom domain (optional)
6. ✅ Set up monitoring alerts (optional)

🎉 **Your application is now deployed to Google Cloud Run!**