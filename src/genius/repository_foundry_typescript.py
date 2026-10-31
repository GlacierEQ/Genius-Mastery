"""GENIUS Repository Foundry: independent TypeScript full-stack product profile.

Implements one explicit application profile, not arbitrary code generation.
Outputs have no runtime dependency on GENIUS-Mastery.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from genius.lineage.publication import publish_domain
from genius.naming import genius_name
from genius.repository_foundry import MISSION_SCHEMA

PROFILE = "typescript-task-board"

_SERVER = r'''import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
import { TaskStore, ValidationError } from './store.js';

type HttpError = { error: string };
const MAX_BODY = 16 * 1024;
const json = (res: ServerResponse, status: number, value: unknown) => {
  const body = JSON.stringify(value);
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8', 'content-length': Buffer.byteLength(body), 'cache-control': 'no-store' });
  res.end(body);
};
const parseBody = async (req: IncomingMessage): Promise<unknown> => {
  const chunks: Buffer[] = [];
  let length = 0;
  for await (const chunk of req) {
    const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    length += bytes.length;
    if (length > MAX_BODY) throw new ValidationError('request body exceeds 16 KiB', 413);
    chunks.push(bytes);
  }
  let parsed: unknown;
  try { parsed = JSON.parse(Buffer.concat(chunks).toString('utf8')); }
  catch { throw new ValidationError('invalid JSON'); }
  if (!parsed || Array.isArray(parsed) || typeof parsed !== 'object') throw new ValidationError('JSON body must be an object');
  return parsed;
};

/** In-process HTTP server for local/offline use. No authentication, TLS or multi-tenant claims. */
export function createAppServer(dataFile: string = process.env.TASK_BOARD_DATA ?? path.resolve('data/tasks.json')) {
  const store = new TaskStore(dataFile);
  const root = path.dirname(fileURLToPath(import.meta.url));
  const publicHtml = path.resolve(root, '../public/index.html');
  const clientJs = path.resolve(root, './public/client.js');
  return createServer(async (req, res) => {
    try {
      const url = new URL(req.url ?? '/', 'http://127.0.0.1');
      const route = url.pathname;
      const method = req.method ?? 'GET';
      if (route === '/health' && method === 'GET') return json(res, 200, { status: 'ok' });
      if (route === '/api/tasks' && method === 'GET') return json(res, 200, { tasks: store.list() });
      if (route === '/api/tasks' && method === 'POST') {
        const body = await parseBody(req) as Record<string, unknown>;
        return json(res, 201, { task: store.add(body.title) });
      }
      const idMatch = /^\/api\/tasks\/([a-f0-9-]{36})$/.exec(route);
      if (idMatch && method === 'PATCH') {
        const body = await parseBody(req) as Record<string, unknown>;
        return json(res, 200, { task: store.update(idMatch[1]!, body.done) });
      }
      if (idMatch && method === 'DELETE') {
        store.remove(idMatch[1]!);
        return json(res, 200, { removed: true });
      }
      if (method === 'GET' && (route === '/' || route === '/client.js' || route === '/style.css')) {
        const filename = route === '/' ? publicHtml : route === '/client.js' ? clientJs : path.resolve(root, '../public/style.css');
        const data = fs.readFileSync(filename);
        res.writeHead(200, {
          'content-type': route === '/' ? 'text/html; charset=utf-8' : route === '/client.js' ? 'text/javascript; charset=utf-8' : 'text/css; charset=utf-8',
          'content-length': data.length,
          'content-security-policy': "default-src 'self'; script-src 'self'; connect-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'",
          'x-content-type-options': 'nosniff',
        });
        return res.end(data);
      }
      return json(res, 404, { error: 'not found' } satisfies HttpError);
    } catch (error) {
      if (error instanceof ValidationError) return json(res, error.status, { error: error.message });
      console.error('request failed', error);
      return json(res, 500, { error: 'internal server error' });
    }
  });
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const raw = process.env.PORT ?? '3000';
  const port = Number(raw);
  if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error('PORT must be 0-65535');
  const server = createAppServer();
  server.listen(port, '127.0.0.1', () => {
    const address = server.address();
    console.log('Task Board listening on http://127.0.0.1:' + (typeof address === 'object' ? address?.port : port));
  });
}
'''
_STORE = r'''import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

export type Task = { id: string; title: string; done: boolean; createdAt: string };
export class ValidationError extends Error {
  constructor(message: string, public readonly status: number = 400) { super(message); }
}

/** Synchronous single-process store with atomic file replacement per operation. */
export class TaskStore {
  private tasks: Task[];
  constructor(private readonly filename: string) {
    if (!fs.existsSync(filename)) { this.tasks = []; return; }
    const decoded: unknown = JSON.parse(fs.readFileSync(filename, 'utf8'));
    if (!Array.isArray(decoded) || !decoded.every((x: unknown) =>
      x && typeof x === 'object' && typeof (x as Task).id === 'string' &&
      typeof (x as Task).title === 'string' && typeof (x as Task).done === 'boolean' &&
      typeof (x as Task).createdAt === 'string')) {
      throw new Error('invalid persisted task store');
    }
    this.tasks = decoded as Task[];
  }
  list(): Task[] { return this.tasks.map(task => ({ ...task })); }
  add(title: unknown): Task {
    const normalized = typeof title === 'string' ? title.trim() : '';
    if (!normalized || normalized.length > 120)
      throw new ValidationError('title must be 1-120 characters');
    if (this.tasks.length >= 500) throw new ValidationError('task limit reached', 409);
    const task: Task = { id: crypto.randomUUID(), title: normalized, done: false, createdAt: new Date().toISOString() };
    this.commit([...this.tasks, task]);
    return { ...task };
  }
  update(id: string, done: unknown): Task {
    if (typeof done !== 'boolean') throw new ValidationError('done must be a boolean');
    const index = this.tasks.findIndex(task => task.id === id);
    if (index < 0) throw new ValidationError('task not found', 404);
    const next = this.list();
    next[index] = { ...next[index]!, done };
    this.commit(next);
    return { ...next[index]! };
  }
  remove(id: string): void {
    if (!this.tasks.some(task => task.id === id)) throw new ValidationError('task not found', 404);
    this.commit(this.tasks.filter(task => task.id !== id));
  }
  private commit(next: Task[]): void {
    const parent = path.dirname(this.filename);
    fs.mkdirSync(parent, { recursive: true });
    const temporary = path.join(parent, '.task-board-' + crypto.randomUUID() + '.tmp');
    try {
      fs.writeFileSync(temporary, JSON.stringify(next, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
      fs.renameSync(temporary, this.filename);
    } finally {
      if (fs.existsSync(temporary)) fs.unlinkSync(temporary);
    }
    this.tasks = next;
  }
}
'''
_CLIENT = r'''type Task = { id: string; title: string; done: boolean; createdAt: string };
type ResponseData = { tasks?: Task[]; task?: Task; removed?: boolean; error?: string };
const form = document.querySelector<HTMLFormElement>('#new-task')!;
const input = document.querySelector<HTMLInputElement>('#title')!;
const list = document.querySelector<HTMLUListElement>('#tasks')!;
const message = document.querySelector<HTMLParagraphElement>('#message')!;

async function api(endpoint: string, method = 'GET', body?: unknown): Promise<ResponseData> {
  const res = await fetch(endpoint, { method, headers: body ? { 'content-type': 'application/json' } : {}, body: body ? JSON.stringify(body) : undefined });
  const data = await res.json() as ResponseData;
  if (!res.ok) throw new Error(data.error ?? 'request failed');
  return data;
}
function showError(error: unknown) { message.textContent = error instanceof Error ? error.message : 'request failed'; }
async function refresh() {
  try {
    const { tasks = [] } = await api('/api/tasks');
    list.replaceChildren();
    for (const task of tasks) {
      const row = document.createElement('li');
      const box = document.createElement('input');
      box.type = 'checkbox'; box.checked = task.done; box.setAttribute('aria-label', 'Complete ' + task.title);
      box.addEventListener('change', () => void api('/api/tasks/' + task.id, 'PATCH', { done: box.checked }).then(refresh).catch(showError));
      const label = document.createElement('span');
      label.textContent = task.title; // user content never enters HTML parser
      if (task.done) label.classList.add('complete');
      const remove = document.createElement('button');
      remove.textContent = 'Remove'; remove.type = 'button'; remove.setAttribute('aria-label', 'Remove ' + task.title);
      remove.addEventListener('click', () => void api('/api/tasks/' + task.id, 'DELETE').then(refresh).catch(showError));
      row.append(box, label, remove); list.append(row);
    }
    message.textContent = tasks.length ? tasks.length + ' tasks' : 'No tasks yet';
  } catch (error) { showError(error); }
}
form.addEventListener('submit', event => {
  event.preventDefault();
  void api('/api/tasks', 'POST', { title: input.value }).then(() => {
    input.value = ''; return refresh();
  }).catch(showError);
});
void refresh();
'''
_HTML = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>GENIUS Task Board</title><link rel="stylesheet" href="/style.css"></head>
<body><main><h1>Task Board</h1><p>Local task tracking with persistent storage.</p>
<form id="new-task"><label for="title">Task</label><input id="title" name="title" type="text" maxlength="120" required><button type="submit">Add task</button></form>
<p id="message" role="status" aria-live="polite">Loading…</p><ul id="tasks"></ul></main><script type="module" src="/client.js"></script></body></html>
'''
_CSS = '''body{font:16px system-ui,sans-serif;max-width:680px;margin:3rem auto;padding:0 1rem;color:#172034;background:#f8fafd}
h1{font-size:1.8rem}form,li{display:flex;gap:.8rem;align-items:center;margin:1rem 0}
input[type=text]{flex:1;padding:.65rem}button{padding:.5rem .8rem;cursor:pointer}
ul{list-style:none;padding:0}li{padding:.8rem;background:white;border:1px solid #dde3ee;border-radius:8px}
li span{flex:1;overflow-wrap:anywhere}.complete{text-decoration:line-through;color:#666}
'''

_TEST = r'''import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { once } from 'node:events';
import { createAppServer } from '../dist/server.js';

async function fixture() {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'genius-board-'));
  const filename = path.join(directory, 'tasks.json');
  const server = createAppServer(filename);
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  const addr = server.address();
  if (!addr || typeof addr === 'string') throw new Error('no listener port');
  const base = 'http://127.0.0.1:' + addr.port;
  return { base, filename, close: async () => { await new Promise((resolve, reject) => server.close(err => err ? reject(err) : resolve(undefined))); fs.rmSync(directory, { recursive: true, force: true }); } };
}
async function request(base, route, method = 'GET', body) {
  const res = await fetch(base + route, { method, headers: body !== undefined ? { 'content-type': 'application/json' } : {}, body: body !== undefined ? JSON.stringify(body) : undefined });
  return { status: res.status, content: await res.text() };
}

test('real HTTP create, list, update, delete and persistent file', async () => {
  const f = await fixture();
  try {
    const create = await request(f.base, '/api/tasks', 'POST', { title: '  Ship real code  ' });
    assert.equal(create.status, 201);
    const task = JSON.parse(create.content).task;
    assert.equal(task.title, 'Ship real code');
    assert.equal(JSON.parse((await request(f.base, '/api/tasks')).content).tasks.length, 1);
    assert.equal(JSON.parse(fs.readFileSync(f.filename, 'utf8'))[0].title, 'Ship real code');
    const done = await request(f.base, '/api/tasks/' + task.id, 'PATCH', { done: true });
    assert.equal(JSON.parse(done.content).task.done, true);
    assert.equal((await request(f.base, '/api/tasks/' + task.id, 'DELETE')).status, 200);
    assert.deepEqual(JSON.parse((await request(f.base, '/api/tasks')).content).tasks, []);
  } finally { await f.close(); }
});

test('malformed, oversized, nonexistent and unsafe routes fail correctly', async () => {
  const f = await fixture();
  try {
    assert.equal((await request(f.base, '/api/tasks', 'POST', { title: ' ' })).status, 400);
    assert.equal((await request(f.base, '/api/tasks', 'POST', { title: 'x'.repeat(121) })).status, 400);
    assert.equal((await request(f.base, '/api/tasks', 'POST', { title: 7 })).status, 400);
    assert.equal((await request(f.base, '/api/tasks', 'PATCH', { done: true })).status, 404);
    assert.equal((await request(f.base, '/api/tasks/00000000-0000-4000-8000-000000000000', 'DELETE')).status, 404);
    assert.equal((await request(f.base, '/src/server.ts')).status, 404);
    const response = await fetch(f.base + '/api/tasks', { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{' });
    assert.equal(response.status, 400);
    assert.equal((await request(f.base, '/api/tasks', 'POST', { title: 'y'.repeat(17000) })).status, 413);
  } finally { await f.close(); }
});

test('HTML and compiled browser JS served; health endpoint functional', async () => {
  const f = await fixture();
  try {
    const html = await request(f.base, '/');
    assert.equal(html.status, 200);
    assert.match(html.content, /<form id="new-task">/);
    const client = await request(f.base, '/client.js');
    assert.equal(client.status, 200);
    assert.match(client.content, /textContent = task.title/);
    const css = await request(f.base, '/style.css');
    assert.equal(css.status, 200);
    assert.match(css.content, /background:/);
    const health = await request(f.base, '/health');
    assert.deepEqual(JSON.parse(health.content), { status: 'ok' });
  } finally { await f.close(); }
});

test('store persists tasks across fresh server instances', async () => {
  const f = await fixture();
  const task = JSON.parse((await request(f.base, '/api/tasks', 'POST', { title: 'Persist' })).content).task;
  const saved = fs.readFileSync(f.filename);
  // Instantiate another independent store before fixture cleanup.
  const { TaskStore } = await import('../dist/store.js');
  const reload = new TaskStore(f.filename);
  assert.equal(reload.list()[0].id, task.id);
  assert.equal(reload.list()[0].title, 'Persist');
  assert.ok(saved.length > 10);
  await f.close();
});
'''
_TSCONFIG = '''{
  "compilerOptions": {
    "target": "ES2022", "lib": ["ES2022", "DOM"],
    "module": "NodeNext", "moduleResolution": "NodeNext",
    "rootDir": "src", "outDir": "dist", "strict": true,
    "esModuleInterop": true, "noUncheckedIndexedAccess": true,
    "skipLibCheck": true, "forceConsistentCasingInFileNames": true
  }, "include": ["src/**/*.ts"]
}
'''
_CI = '''name: TypeScript Full Stack Verification
on:
  push:
  pull_request:
permissions:
  contents: read
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm ci --ignore-scripts
      - run: npm run build
      - run: npm test
'''


def generate_typescript_task_board(objective: str, name: str, output_root: Path | str | None = None) -> Path:
    """Generate an independently runnable HTTP and browser TypeScript task board."""
    if not isinstance(objective, str) or not objective.strip() or len(objective) > 20_000:
        raise ValueError("nonempty original objective under 20,001 characters required")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("nonempty project name required")
    repository = genius_name(name)
    mission = {
        "schema_version": MISSION_SCHEMA,
        "mode": "NEW", "original_objective": objective, "project": repository,
        "profile": PROFILE, "status": "GENERATED_UNVERIFIED",
        "implemented_behavior": ["TypeScript HTTP JSON CRUD API", "browser task-board UI",
                                 "local JSON persistence", "native HTTP integration tests"],
        "unverified_requirements": "Only task-board behavior is implemented; no authentication, TLS, remote deployment or arbitrary objective satisfaction.",
        "acceptance_command": "npm ci --ignore-scripts && npm run build && npm test",
    }
    package_name = repository.lower()
    files: dict[str, str] = {
        "mission.json": json.dumps(mission, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        "package.json": json.dumps({
            "name": package_name, "version": "0.1.0", "private": True,
            "type": "module", "engines": {"node": ">=22"},
            "scripts": {"build": "tsc -p tsconfig.json", "test": "node --test tests/*.test.mjs", "start": "node dist/server.js"},
            "devDependencies": {"typescript": "5.8.3", "@types/node": "22.15.3"},
        }, indent=2, sort_keys=True) + "\n",
        "src/server.ts": _SERVER,
        "src/store.ts": _STORE,
        "src/public/client.ts": _CLIENT,
        "public/index.html": _HTML,
        "public/style.css": _CSS,
        "tests/task-board.test.mjs": _TEST,
        "tsconfig.json": _TSCONFIG,
        ".github/workflows/verify.yml": _CI,
        ".gitignore": "node_modules/\ndist/\ndata/\n.env\n.DS_Store\n",
        "README.md": (
            f"# {repository}\n\nIndependently runnable TypeScript task-board with real HTTP JSON API, browser UI, and local persistence.\n\n"
            "## Clean checkout\n\n`npm ci --ignore-scripts`\n`npm run build`\n`npm test`\n`npm start`\n\n"
            "Visit `http://127.0.0.1:3000`; override `PORT` or `TASK_BOARD_DATA`.\n\n"
            "Run locally only: this project deliberately does not provide internet authentication, multi-user isolation, or production deployment.\n"
            "The original objective and evidence status are recorded in `mission.json`.\n"
        ),
    }
    # Lockfile is a deterministic, fully resolved npm v3 lockfile generated once
    # with the exact pinned dependencies, then embedded as a stable template.
    lock = Path(__file__).with_name("typescript_task_board_lock.json")
    lock_data = json.loads(lock.read_text(encoding="utf-8"))
    lock_data["name"] = package_name
    lock_data["packages"][""]["name"] = package_name
    files["package-lock.json"] = json.dumps(lock_data, indent=2) + "\n"
    digests = {name: hashlib.sha256(data.encode("utf-8")).hexdigest() for name, data in sorted(files.items())}
    files["source-manifest.json"] = json.dumps({"schema_version": "glaciereq.repo-foundry.source-manifest.v1",
                                                "status": "GENERATED_UNVERIFIED", "files_sha256": digests}, indent=2, sort_keys=True) + "\n"

    def render(staging: Path) -> Path:
        root = staging / repository
        for relative, content in files.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return root
    return publish_domain(output_root, repository, render)