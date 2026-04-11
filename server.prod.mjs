/**
 * server.prod.mjs
 * Production-only Express server for the Ridhi Command Center.
 *
 * - Serves the pre-built React SPA from ./dist
 * - Proxies all /api/* requests to the FastAPI backend (default: :8000)
 *   The /api/health route is answered directly to serve as a Cloud Run probe.
 *
 * Run with:  node server.prod.mjs
 */

import express from 'express';
import http from 'http';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const PORT = parseInt(process.env.PORT ?? '3000', 10);
const BACKEND_PORT = parseInt(process.env.BACKEND_PORT ?? '8000', 10);
const BACKEND_HOST = process.env.BACKEND_HOST ?? 'localhost';

const app = express();

// ── Health check (answered directly – used as Cloud Run readiness probe) ────
app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok' });
});

// ── Proxy all other /api/* requests to FastAPI ───────────────────────────────
app.all('/api/*', (req, res) => {
  const options = {
    hostname: BACKEND_HOST,
    port: BACKEND_PORT,
    path: req.url,
    method: req.method,
    headers: { ...req.headers, host: `${BACKEND_HOST}:${BACKEND_PORT}` },
  };

  const proxyReq = http.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode ?? 502, proxyRes.headers);
    proxyRes.pipe(res, { end: true });
  });

  proxyReq.on('error', (err) => {
    console.error('[proxy] Backend request failed:', err.message);
    if (!res.headersSent) {
      res.status(502).json({ error: 'Backend unavailable', detail: err.message });
    }
  });

  req.pipe(proxyReq, { end: true });
});

// ── Serve pre-built React SPA ────────────────────────────────────────────────
const distPath = path.join(__dirname, 'dist');
app.use(express.static(distPath));
app.get('*', (_req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

// ── Start ────────────────────────────────────────────────────────────────────
app.listen(PORT, '0.0.0.0', () => {
  console.log(`[server.prod] Express listening on port ${PORT}`);
  console.log(`[server.prod] Proxying /api/* → http://${BACKEND_HOST}:${BACKEND_PORT}`);
});
