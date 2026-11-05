import express from 'express';
import { createServer as createViteServer } from 'vite';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';

const PORT = 3000;
const ROOT_DIR = process.cwd();
const BRIDGE_SCRIPT = path.join(ROOT_DIR, 'django_atm_project', 'atm_app', 'cli_bridge.py');

function runPythonBridge(payload: Record<string, unknown>): Promise<Record<string, unknown>> {
  return new Promise((resolve, reject) => {
    const py = spawn('python3', [BRIDGE_SCRIPT], {
      cwd: ROOT_DIR,
    });

    let stdout = '';
    let stderr = '';

    py.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });

    py.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
    });

    py.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(stderr || `Python process exited with code ${code}`));
        return;
      }
      try {
        resolve(JSON.parse(stdout));
      } catch (err) {
        reject(new Error(`Failed to parse Python output: ${stdout}`));
      }
    });

    py.stdin.write(JSON.stringify(payload));
    py.stdin.end();
  });
}

async function startServer() {
  const app = express();
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  // Ensure the downloadable Django ZIP is up to date on startup
  try {
    await runPythonBridge({
      action: 'build_zip',
      output_path: path.join(ROOT_DIR, 'public', 'CTU_PELEC1_ATM_Simulator_Django.zip'),
    });
  } catch (e) {
    console.error('Failed to prebuild Django ZIP:', e);
  }

  // API endpoint that executes real Python 3.10 OOP classes in django_atm_project/atm_app/oop_models.py
  app.post('/api/atm', async (req, res) => {
    try {
      const result = await runPythonBridge(req.body || { action: 'state' });
      res.json(result);
    } catch (error) {
      res.status(500).json({
        error: error instanceof Error ? error.message : 'Python OOP execution failed',
      });
    }
  });

  app.get('/api/atm', async (_req, res) => {
    try {
      const result = await runPythonBridge({ action: 'state' });
      res.json(result);
    } catch (error) {
      res.status(500).json({
        error: error instanceof Error ? error.message : 'Python OOP execution failed',
      });
    }
  });

  // Endpoint to read the actual Python, Django, HTML, CSS, and README source files
  app.get('/api/source-files', (_req, res) => {
    const filesToRead = [
      {
        path: 'atm_app/oop_models.py',
        label: 'atm_app/oop_models.py (Core Python OOP Classes)',
        language: 'python',
      },
      {
        path: 'atm_app/views.py',
        label: 'atm_app/views.py (Django Views & Session Logic)',
        language: 'python',
      },
      {
        path: 'atm_app/urls.py',
        label: 'atm_app/urls.py (Django URL Routes)',
        language: 'python',
      },
      {
        path: 'atm_app/templates/atm/index.html',
        label: 'atm_app/templates/atm/index.html (Pure HTML Django Template)',
        language: 'html',
      },
      {
        path: 'atm_app/static/atm/style.css',
        label: 'atm_app/static/atm/style.css (Light Blue & White Glassmorphic CSS)',
        language: 'css',
      },
      {
        path: 'atm_project/settings.py',
        label: 'atm_project/settings.py (Django Configuration)',
        language: 'python',
      },
      {
        path: 'manage.py',
        label: 'manage.py (Django CLI Entry Point)',
        language: 'python',
      },
      {
        path: 'README.md',
        label: 'README.md (Setup, UML, OOP Map & 6 Test Cases)',
        language: 'markdown',
      },
    ];

    const loaded = filesToRead.map((item) => {
      const fullPath = path.join(ROOT_DIR, 'django_atm_project', item.path);
      const content = fs.existsSync(fullPath) ? fs.readFileSync(fullPath, 'utf-8') : '';
      return { ...item, content };
    });

    res.json({ files: loaded });
  });

  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(ROOT_DIR, 'dist');
    app.use(express.static(distPath));
    app.get('*', (_req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`CTU Express ATM Simulator server running on http://0.0.0.0:${PORT}`);
  });
}

startServer();
