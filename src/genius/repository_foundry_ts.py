"""Executable TypeScript taskboard profile for the existing GENIUS Repository Foundry.

Node 22's native TypeScript-stripping compiler creates deployable JavaScript
without dependency downloads. This is one bounded product profile, not a
claim that arbitrary natural-language missions are implemented.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from genius.naming import genius_name
from genius.lineage.publication import publish_domain
from genius.repository_foundry import MISSION_SCHEMA

PROFILE = "typescript-taskboard"

_STORE = r'''import { mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import { dirname } from "node:path";

export type Task = { id: string; title: string; done: boolean; createdAt: string };

function validateTitle(value: unknown): string {
  if (typeof value !== "string") throw new TypeError("title must be a string");
  const title = value.trim();
  if (!title || title.length > 120 || /[\x00-\x1f\x7f]/.test(title)) {
    throw new RangeError("title must contain 1-120 printable characters");
  }
  return title;
}

export class TaskStore {
  private chain: Promise<void> = Promise.resolve();
  private readonly filename: string;
  constructor(filename: string) { this.filename = filename; }

  async list(): Promise<Task[]> {
    let raw: string;
    try {
      raw = await readFile(this.filename, "utf8");
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "ENOENT") return [];
      throw error;
    }
    const rows: unknown = JSON.parse(raw);
    if (!Array.isArray(rows) || !rows.every((row: unknown) =>
      typeof row === "object" && row !== null &&
      typeof (row as Task).id === "string" &&
      typeof (row as Task).title === "string" &&
      typeof (row as Task).done === "boolean" &&
      typeof (row as Task).createdAt === "string")) {
      throw new Error("invalid task store data");
    }
    return rows as Task[];
  }

  private async save(rows: Task[]): Promise<void> {
    await mkdir(dirname(this.filename), { recursive: true });
    const temporary = `${this.filename}.tmp-${randomUUID()}`;
    try {
      await writeFile(temporary, JSON.stringify(rows, null, 2) + "\n", { mode: 0o600, flag: "wx" });
      await rename(temporary, this.filename);
    } finally {
      await rm(temporary, { force: true });
    }
  }

  private transact<T>(change: (rows: Task[]) => T): Promise<T> {
    const operation = this.chain.then(async () => {
      const rows = await this.list();
      const result = change(rows);
      await this.save(rows);
      return result;
    });
    this.chain = operation.then(() => undefined, () => undefined);
    return operation;
  }

  create(input: unknown): Promise<Task> {
    const title = validateTitle(input);
    return this.transact(rows => {
      if (rows.length >= 1000) throw new RangeError("task capacity reached");
      const task: Task = { id: randomUUID(), title, done: false, createdAt: new Date().toISOString() };
      rows.push(task);
      return task;
    });
  }

  setDone(id: string, done: unknown): Promise<Task | null> {
    if (typeof done !== "boolean") throw new TypeError("done must be boolean");
    return this.transact(rows => {
      const task = rows.find(row => row.id === id);
      if (!task) return null;
      task.done = done;
      return { ...task };
    });
  }

  remove(id: string): Promise<boolean> {
    return this.transact(rows => {
      const index = rows.findIndex(row => row.id === id);
      if (index < 0) return false;
      rows.splice(index, 1);
      return true;
    });
  }
}
'''

_SERVER = r'''import { createServer, type IncomingMessage, type Server, type ServerResponse } from "node:http";
import { readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { TaskStore } from "./store.js";

const publicDir = join(dirname(fileURLToPath(import.meta.url)), "..", "public");
const security = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "no-referrer",
  "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'",
};

class InputError extends Error {
  readonly status: number;
  constructor(status: number, message: string) { super(message); this.status = status; }
}

function send(res: ServerResponse, status: number, payload: unknown): void {
  res.writeHead(status, { ...security, "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" });
  res.end(JSON.stringify(payload));
}

async function body(req: IncomingMessage): Promise<Record<string, unknown>> {
  const contentType = req.headers["content-type"] ?? "";
  if (!/^application\/json(?:\s*;|$)/i.test(contentType)) throw new InputError(415, "application/json required");
  const chunks: Buffer[] = [];
  let total = 0;
  for await (const chunk of req) {
    const data = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    total += data.length;
    if (total > 16384) throw new InputError(413, "body exceeds 16 KiB");
    chunks.push(data);
  }
  let parsed: unknown;
  try { parsed = JSON.parse(Buffer.concat(chunks).toString("utf8")); }
  catch { throw new InputError(400, "invalid JSON body"); }
  if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
    throw new InputError(400, "JSON object required");
  }
  return parsed as Record<string, unknown>;
}

export function createApp(store: TaskStore): Server {
  return createServer(async (req, res) => {
    try {
      const path = new URL(req.url ?? "/", "http://localhost").pathname;
      if (req.method === "GET" && path === "/api/tasks") {
        return send(res, 200, { tasks: await store.list() });
      }
      if (req.method === "POST" && path === "/api/tasks") {
        const data = await body(req);
        if (Object.keys(data).sort().join() !== "title") throw new InputError(400, "only title accepted");
        return send(res, 201, { task: await store.create(data.title) });
      }
      const item = /^\/api\/tasks\/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$/i.exec(path);
      if (item && req.method === "PATCH") {
        const data = await body(req);
        if (Object.keys(data).sort().join() !== "done") throw new InputError(400, "only done accepted");
        const task = await store.setDone(item[1], data.done);
        return task ? send(res, 200, { task }) : send(res, 404, { error: "task not found" });
      }
      if (item && req.method === "DELETE") {
        const found = await store.remove(item[1]);
        if (!found) return send(res, 404, { error: "task not found" });
        res.writeHead(204, security); return res.end();
      }
      const staticPaths: Record<string, [string, string]> = {
        "/": ["index.html", "text/html; charset=utf-8"],
        "/app.js": ["app.js", "text/javascript; charset=utf-8"],
        "/style.css": ["style.css", "text/css; charset=utf-8"],
      };
      if (req.method === "GET" && staticPaths[path]) {
        const [filename, mime] = staticPaths[path];
        const file = await readFile(join(publicDir, filename));
        res.writeHead(200, { ...security, "Content-Type": mime, "Cache-Control": "no-store" });
        return res.end(file);
      }
      return send(res, 404, { error: "not found" });
    } catch (error) {
      if (error instanceof InputError) return send(res, error.status, { error: error.message });
      if (error instanceof TypeError || error instanceof RangeError) return send(res, 400, { error: error.message });
      // Do not expose internal filesystem paths or stack traces to clients.
      console.error("request failed", error);
      return send(res, 500, { error: "internal error" });
    }
  });
}
'''

_MAIN = r'''import { resolve } from "node:path";
import { TaskStore } from "./store.js";
import { createApp } from "./server.js";

const port = Number(process.env.PORT ?? "3000");
if (!Number.isInteger(port) || port < 1 || port > 65535) {
  console.error("PORT must be between 1 and 65535");
  process.exit(2);
}
const host = process.env.HOST ?? "127.0.0.1";
const store = new TaskStore(resolve(process.env.TASKBOARD_DATA ?? "data/tasks.json"));
const server = createApp(store);
server.listen(port, host, () => console.log(`Taskboard listening on http://${host}:${port}`));
'''

_BUILD = r'''import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { stripTypeScriptTypes } from "node:module";
import { join } from "node:path";

// Node >=22.13 includes TypeScript stripping. No toolchain download or
// implicit network access is required to build this deliberately constrained
// erasable-TypeScript profile. The compiler does not perform TS typechecking.
const source = ["main", "store", "server"];
await rm("dist", { recursive: true, force: true });
await mkdir("dist", { recursive: true });
for (const basename of source) {
  const input = await readFile(join("src", `${basename}.ts`), "utf8");
  const javascript = stripTypeScriptTypes(input, { mode: "strip" });
  await writeFile(join("dist", `${basename}.js`), javascript, "utf8");
}
console.log("Built Node 22 executable JavaScript into dist/");
'''

_HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>GENIUS Taskboard</title><link rel="stylesheet" href="/style.css"></head>
<body><main><h1>Taskboard</h1><p class="subtitle">A local, persistent task tracker.</p>
<form id="add-form"><label for="title">New task</label><div class="row"><input id="title" maxlength="120" required autocomplete="off" placeholder="What needs doing?"><button>Add</button></div></form>
<p id="error" role="alert" aria-live="polite"></p><ul id="tasks" aria-label="Tasks"></ul>
<p class="subtitle" id="count" aria-live="polite"></p></main><script src="/app.js" defer></script></body></html>
'''

_CSS = r'''body{font:16px/1.5 system-ui,sans-serif;color:#17212d;background:#f4f7fa;margin:0;padding:2rem}main{margin:auto;max-width:650px;background:white;padding:2rem;border-radius:14px;box-shadow:0 6px 24px #17212d12}h1{margin:0}.subtitle{color:#536779}.row{display:flex;gap:.7rem}input{font:inherit;padding:.7rem;flex:1;min-width:0}button{font:inherit;padding:.65rem 1rem;cursor:pointer}ul{padding:0;list-style:none}li{display:flex;align-items:center;gap:.7rem;padding:.8rem;border-bottom:1px solid #ddd}li span{flex:1;overflow-wrap:anywhere}.done{text-decoration:line-through;color:#536779}#error{color:#a12020}button:focus-visible,input:focus-visible{outline:3px solid #184d9e;outline-offset:2px}
'''

_CLIENT = r'''"use strict";
const form = document.querySelector("#add-form");
const list = document.querySelector("#tasks");
const error = document.querySelector("#error");
const counter = document.querySelector("#count");
async function request(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) { const body = await res.json(); throw new Error(body.error ?? `HTTP ${res.status}`); }
  return res.status === 204 ? null : res.json();
}
async function refresh() {
  const data = await request("/api/tasks");
  list.replaceChildren();
  for (const task of data.tasks) {
    const row = document.createElement("li");
    const check = document.createElement("input");
    check.type = "checkbox"; check.checked = task.done; check.setAttribute("aria-label", `Complete ${task.title}`);
    check.addEventListener("change", async () => {
      try { await request(`/api/tasks/${task.id}`, { method: "PATCH", headers: {"Content-Type":"application/json"}, body: JSON.stringify({done:check.checked}) }); await refresh(); }
      catch(e) { showError(e); await refresh(); }
    });
    const name = document.createElement("span"); name.textContent = task.title;
    if (task.done) name.classList.add("done");
    const remove = document.createElement("button"); remove.textContent = "Delete";
    remove.setAttribute("aria-label", `Delete ${task.title}`);
    remove.addEventListener("click", async () => {
      try { await request(`/api/tasks/${task.id}`, {method:"DELETE"}); await refresh(); }
      catch(e) { showError(e); }
    });
    row.append(check, name, remove); list.append(row);
  }
  counter.textContent = `${data.tasks.length} task(s)`;
}
function showError(e) { error.textContent = String(e.message ?? e); }
form.addEventListener("submit", async event => {
  event.preventDefault(); error.textContent = "";
  const title = document.querySelector("#title").value;
  try { await request("/api/tasks", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({title})}); form.reset(); await refresh(); }
  catch(e){showError(e);}
});
refresh().catch(showError);
'''

_TESTS = r'''import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { TaskStore } from "../dist/store.js";
import { createApp } from "../dist/server.js";

async function withServer(run) {
  const root = await mkdtemp(join(tmpdir(), "genius-taskboard-"));
  const filename = join(root, "tasks.json");
  const server = createApp(new TaskStore(filename));
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  const base = `http://127.0.0.1:${address.port}`;
  try { await run({ base, root, filename }); }
  finally { await new Promise(resolve => server.close(resolve)); await rm(root, {recursive:true, force:true}); }
}
const json = (body, method = "POST") => ({ method, headers: {"Content-Type":"application/json"}, body: JSON.stringify(body) });

 test("frontend and security headers serve actual browser assets", async () => withServer(async ({base}) => {
   const html = await fetch(base);
   assert.equal(html.status, 200);
   assert.match(await html.text(), /<form id="add-form">/);
   assert.match(html.headers.get("content-security-policy"), /default-src 'self'/);
   const client = await fetch(base + "/app.js");
   assert.equal(client.status, 200);
   assert.match(await client.text(), /textContent = task.title/);
   assert.equal((await fetch(base + "/not-allowed")).status, 404);
 }));

 test("real HTTP create, list, update, delete and persistence", async () => withServer(async ({base, filename}) => {
   const create = await fetch(base + "/api/tasks", json({title:"  Review PR  "}));
   assert.equal(create.status, 201);
   const task = (await create.json()).task;
   assert.equal(task.title, "Review PR");
   const list = (await (await fetch(base + "/api/tasks")).json()).tasks;
   assert.equal(list.length, 1);
   assert.equal((await (await fetch(base + "/api/tasks/" + task.id, json({done:true}, "PATCH"))).json()).task.done, true);
   assert.equal((await new TaskStore(filename).list())[0].done, true);
   assert.equal((await fetch(base + "/api/tasks/" + task.id, {method:"DELETE"})).status, 204);
   assert.equal((await new TaskStore(filename).list()).length, 0);
 }));

 test("invalid inputs fail with proper HTTP errors without crashing service", async () => withServer(async ({base}) => {
   assert.equal((await fetch(base + "/api/tasks", json({title:""}))).status, 400);
   assert.equal((await fetch(base + "/api/tasks", json({title:7}))).status, 400);
   assert.equal((await fetch(base + "/api/tasks", json({title:"x", extra:1}))).status, 400);
   assert.equal((await fetch(base + "/api/tasks", {method:"POST", body:"oops",headers:{"Content-Type":"application/json"}})).status, 400);
   assert.equal((await fetch(base + "/api/tasks", {method:"POST", body:"{}"})).status, 415);
   assert.equal((await fetch(base + "/api/tasks", json({title:"x".repeat(20000)}))).status, 413);
   assert.equal((await fetch(base + "/api/tasks")).status, 200);
 }));

 test("concurrent creation does not lose updates", async () => withServer(async ({base}) => {
   const result = await Promise.all(Array.from({length:30}, (_, i) => fetch(base + "/api/tasks", json({title:`T${i}`}))));
   assert.ok(result.every(x => x.status === 201));
   const rows = (await (await fetch(base + "/api/tasks")).json()).tasks;
   assert.equal(rows.length, 30);
   assert.equal(new Set(rows.map(row=>row.id)).size, 30);
 }));

 test("corrupt persistence is not silently reset", async () => withServer(async ({base, filename}) => {
   await writeFile(filename,"{broken", "utf8");
   const result = await fetch(base + "/api/tasks");
   assert.equal(result.status, 500);
   assert.equal((await readFile(filename,"utf8")),"{broken");
 }));
'''

_TSCONFIG = r'''{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noEmit": true,
    "types": ["node"],
    "skipLibCheck": true,
    "erasableSyntaxOnly": true,
    "isolatedModules": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*.ts"]
}
'''

_CI = '''name: Native TypeScript product verification
on:
  push:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - run: npm ci
      - run: npm test
'''


def generate_typescript_taskboard(objective: str, name: str, output_root: Path | str | None = None) -> Path:
    """Publish one locally functional, independently testable full-stack TS app."""
    if not isinstance(objective, str) or not objective.strip() or len(objective) > 20_000:
        raise ValueError("nonempty original objective up to 20,000 characters required")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("nonempty project name required")
    repo = genius_name(name)
    package = repo.lower()
    mission = {
        "schema_version": MISSION_SCHEMA,
        "mode": "NEW", "original_objective": objective, "project": repo,
        "profile": PROFILE, "status": "GENERATED_UNVERIFIED",
        "implemented_behavior": ["Live browser task interface", "HTTP task CRUD API", "Atomic local JSON persistence", "Native Node.js integration tests"],
        "unverified_requirements": "This bounded profile does not establish arbitrary objective satisfaction or external deployment.",
        "acceptance_command": "npm ci && npm test",
    }

    def render(staging: Path) -> Path:
        root = staging / repo
        pkg = {"name": package, "version": "0.1.0", "private": True, "type": "module",
               "engines": {"node": ">=22.13.0"},
               "scripts": {"build": "node scripts/build.mjs", "test": "npm run build && node --test tests/*.test.mjs", "start": "npm run build && node dist/main.js", "typecheck": "tsc --noEmit -p tsconfig.json"}}
        lock = {"name": package, "version": "0.1.0", "lockfileVersion": 3,
                "requires": True, "packages": {"": {"name": package, "version": "0.1.0", "engines": {"node": ">=22.13.0"}}}}
        files = {
            "mission.json": json.dumps(mission, sort_keys=True, ensure_ascii=False, indent=2) + "\n",
            "package.json": json.dumps(pkg, sort_keys=True, indent=2) + "\n",
            "package-lock.json": json.dumps(lock, sort_keys=True, indent=2) + "\n",
            "tsconfig.json": _TSCONFIG,
            "src/store.ts": _STORE,
            "src/server.ts": _SERVER,
            "src/main.ts": _MAIN,
            "scripts/build.mjs": _BUILD,
            "public/index.html": _HTML,
            "public/style.css": _CSS,
            "public/app.js": _CLIENT,
            "tests/taskboard.test.mjs": _TESTS,
            ".github/workflows/ci.yml": _CI,
            ".gitignore": "node_modules/\ndist/\ndata/\n.DS_Store\n",
            "README.md": (f"# {repo}\n\nIndependent full-stack taskboard with a typed TypeScript backend, browser UI, and file persistence. "
                          "Original mission and scope are preserved in `mission.json`.\n\n"
                          "## Clean checkout\n\nRequires Node.js >=22.13. `npm ci` requires no third-party packages. "
                          "The Node native TypeScript-stripping build API is experimental in this runtime; "
                          "the default offline `npm test` does not itself run `tsc` typechecking.\n\n"
                          "## Optional independent strict TypeScript typecheck\n\n"
                          "Install pinned verifier tools without changing the saved dependency lock:\n\n"
                          "```sh\nnpm install --no-save --package-lock=false --ignore-scripts typescript@5.8.3 @types/node@22.15.3\nnpm run typecheck\n```\n\n"
                          "The repository factory CI performs this extra compiler verification.\n\n"
                          "```sh\nnpm ci\nnpm test\nnpm start\n```\n\n"
                          "Open http://127.0.0.1:3000 . The server listens on loopback by default. "
                          "Set PORT and TASKBOARD_DATA to configure the port and durable JSON path. "
                          "The local data file contains user data: keep it private and back it up. "
                          "Run only one server process per data file; the write queue serializes requests within one process, "
                          "not across independent processes. Do not expose this unauthenticated service publicly.\n\n"
                          "Tests cover live HTTP CRUD, browser assets, invalid JSON, bounded payloads, concurrent writes, "
                          "persistence and corruption behavior. Generated is not equivalent to deployed or fully verified.\n"),
        }
        checksums = {filename: hashlib.sha256(content.encode("utf-8")).hexdigest()
                     for filename, content in sorted(files.items())}
        files["source-manifest.json"] = json.dumps({
            "schema_version": "glaciereq.repo-foundry.source-manifest.v1",
            "status": "GENERATED_UNVERIFIED", "files_sha256": checksums,
        }, sort_keys=True, indent=2) + "\n"
        for filename, content in files.items():
            target = root / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        return root

    return publish_domain(output_root, repo, render)