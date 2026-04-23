/**
 * vite.config.prod.ts
 * Production-specific Vite configuration for the Ridhi Command Center.
 *
 * Build with:
 *   npx vite build --config vite.config.prod.ts
 */

import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  // Load env variables from .env / .env.production etc.
  const env = loadEnv(mode, '.', '');

  return {
    plugins: [react(), tailwindcss()],

    define: {
      // Expose only the Gemini key; the Express proxy handles the backend URL.
      'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY ?? ''),
      'process.env.NODE_ENV': JSON.stringify('production'),
    },

    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },

    build: {
      // Output to dist/ (consumed by the Express static server)
      outDir: 'dist',
      emptyOutDir: true,

      // Generate source maps for error reporting (upload to Sentry / Cloud Logging)
      sourcemap: true,

      // Minify for production
      minify: 'esbuild',

      // Warn when chunks exceed 500 kB
      chunkSizeWarningLimit: 500,

      rollupOptions: {
        output: {
          // Split vendor code into a separate chunk for better caching
          manualChunks: {
            vendor: ['react', 'react-dom', 'react-router-dom'],
          },
        },
      },
    },

    // No dev-server settings needed for production builds
  };
});
