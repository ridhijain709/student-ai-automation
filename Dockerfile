# ─────────────────────────────────────────────────────────
# Stage 1 – Install Python backend dependencies
# ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS python-deps

WORKDIR /app

# Install build tools needed by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────
# Stage 2 – Build the React / Vite frontend
# ─────────────────────────────────────────────────────────
FROM node:20-slim AS frontend-build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci --ignore-scripts

# Copy everything needed for the Vite build
COPY index.html tsconfig.json vite.config.prod.ts ./
COPY src ./src

# Build for production using the production config (outputs to /app/dist)
RUN npx vite build --config vite.config.prod.ts

# ─────────────────────────────────────────────────────────
# Stage 3 – Runtime image
# ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# ── Python runtime ──────────────────────────────────────
# Copy installed packages and executables from the build stage
COPY --from=python-deps /usr/local/lib/python3.11/site-packages \
                        /usr/local/lib/python3.11/site-packages
COPY --from=python-deps /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# ── Node.js (for the Express static server) ─────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Application source ──────────────────────────────────
# Backend
COPY backend ./backend

# Frontend build artefacts + production Express server
COPY --from=frontend-build /app/dist ./dist
COPY package.json package-lock.json* ./
# Install only production npm deps (express is a prod dep)
RUN npm ci --omit=dev --ignore-scripts

# Production server (plain ESM – no tsx required)
COPY server.prod.mjs ./

# Startup script (copied before USER switch so root can set perms)
COPY start.sh ./
RUN chmod +x start.sh

# ── Data directory for SQLite ────────────────────────────
RUN mkdir -p /app/data

# ── Non-root user for security ───────────────────────────
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser \
    && chown -R appuser:appgroup /app
USER appuser

# ── Environment defaults ─────────────────────────────────
ENV NODE_ENV=production \
    PORT=3000 \
    BACKEND_PORT=8000 \
    DATABASE_URL=sqlite:////app/data/ridhi.db

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

CMD ["./start.sh"]
