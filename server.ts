/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// =====================================================================
// Backend Server Entry Point (Full-Stack Express + Vite Integration)
// Entry-level architecture cleanly separating backend APIs and frontend
// =====================================================================

import express, { Request, Response } from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { apiRouter } from './backend/routes/api.ts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function startServer() {
  const app = express();
  const PORT = 3000;
  const isProduction = process.env.NODE_ENV === 'production';

  // 1. Middleware: Parse incoming JSON request bodies
  app.use(express.json());

  // 2. Backend API Routes
  app.use('/api', apiRouter);

  // 3. Frontend Integration (Vite Middleware in Dev, Static Files in Prod)
  if (!isProduction) {
    // Development Mode: Mount Vite's HMR/middleware onto Express
    const { createServer: createViteServer } = await import('vite');
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
    console.log('[Backend] Mounted Vite development server middleware.');
  } else {
    // Production Mode: Serve compiled frontend distribution
    const distPath = path.resolve(__dirname, 'dist');
    app.use(express.static(distPath));
    app.get('*', (_req: Request, res: Response) => {
      res.sendFile(path.resolve(distPath, 'index.html'));
    });
    console.log(`[Backend] Serving static production files from: ${distPath}`);
  }

  // 4. Start HTTP Server
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`[Server] Academic Performance System running on http://0.0.0.0:${PORT}`);
    console.log(`[API] Health endpoint ready at http://0.0.0.0:${PORT}/api/health`);
  });
}

startServer().catch((err) => {
  console.error('[Server Error] Failed to start server:', err);
  process.exit(1);
});
