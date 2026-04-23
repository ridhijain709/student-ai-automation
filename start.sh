#!/usr/bin/env bash
# start.sh
# Startup script for the Ridhi Command Center container.
# Runs the FastAPI backend (Uvicorn) and the Express static server concurrently.
# Cloud Run sends traffic to port 3000 (Express); Express proxies /api/* to port 8000 (FastAPI).

set -e

BACKEND_PORT="${BACKEND_PORT:-8000}"
PORT="${PORT:-3000}"

# Ensure the data directory exists (SQLite)
mkdir -p /app/data

echo "[start.sh] Running database migrations..."
python -m backend.migrate_db

echo "[start.sh] Starting FastAPI backend on port ${BACKEND_PORT}..."
uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port "${BACKEND_PORT}" \
    --workers 1 \
    --log-level info &

BACKEND_PID=$!

echo "[start.sh] Starting Express server on port ${PORT}..."
NODE_ENV=production node /app/server.prod.mjs &

EXPRESS_PID=$!

# Wait for either process to exit; exit with its code.
wait -n $BACKEND_PID $EXPRESS_PID
EXIT_CODE=$?
echo "[start.sh] A process exited with code ${EXIT_CODE}. Shutting down."
kill $BACKEND_PID $EXPRESS_PID 2>/dev/null || true
exit $EXIT_CODE
