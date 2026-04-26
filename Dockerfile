# ============================================================
# Stage 1: Build Node.js frontend with Vite
# ============================================================
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# Copy package files first for layer caching
COPY package.json package-lock.json ./

# Install all dependencies (including dev) for the build step
RUN npm ci --prefer-offline

# Copy source files needed by Vite build
COPY vite.config.ts tsconfig.json index.html ./
COPY src/ ./src/
COPY frontend/ ./frontend/

# Build production assets into /app/dist
ENV NODE_ENV=production
RUN npm run build

# ============================================================
# Stage 2: Python dependency builder
# ============================================================
FROM python:3.11-alpine AS python-builder

WORKDIR /install

# Install build dependencies required by some Python packages
RUN apk add --no-cache gcc musl-dev libffi-dev

# Install Python packages into an isolated prefix for easy copying
COPY requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install/deps -r requirements.txt

# ============================================================
# Final Stage: Lightweight Alpine runtime
# ============================================================
FROM python:3.11-alpine AS runtime

# tini provides proper PID-1 signal forwarding / zombie reaping
RUN apk add --no-cache tini curl

WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=python-builder /install/deps /usr/local

# Copy backend application source
COPY backend/ ./backend/

# Copy built frontend static assets (produced by the frontend-builder stage)
COPY --from=frontend-builder /app/dist ./dist

# Persistent storage directory for SQLite database
RUN mkdir -p /app/data && chmod 777 /app/data

# Expose the single public port used by Cloud Run
EXPOSE 3000

# Runtime environment defaults (overridable via Cloud Run env vars)
ENV NODE_ENV=production \
    PORT=3000 \
    PYTHONUNBUFFERED=1

# Health check against the FastAPI /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Use tini as PID 1 for proper signal handling and zombie reaping
ENTRYPOINT ["/sbin/tini", "--"]

# FastAPI (uvicorn) serves both the REST API and the built React frontend
# on port 3000. Static file mounting is configured in backend/main.py.
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "3000", "--workers", "1"]
