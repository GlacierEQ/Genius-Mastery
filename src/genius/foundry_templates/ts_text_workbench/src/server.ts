/** Loopback-only application server, no wildcard CORS or runtime dependencies. */
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { analyzeText } from "./analysis.ts";

const ROOT = process.cwd();
const MAX_BODY = 65_536;
class PayloadTooLargeError extends Error {}

function json(response: ServerResponse, status: number, body: unknown): void {
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff"
  });
  response.end(JSON.stringify(body));
}

async function readJson(request: IncomingMessage): Promise<unknown> {
  let bytes = 0;
  const parts: Buffer[] = [];
  for await (const chunk of request) {
    const value = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    bytes += value.length;
    if (bytes > MAX_BODY) throw new PayloadTooLargeError("request body exceeds 65536 bytes");
    parts.push(value);
  }
  try {
    return JSON.parse(Buffer.concat(parts).toString("utf8")) as unknown;
  } catch {
    throw new SyntaxError("invalid JSON request body");
  }
}

async function handle(request: IncomingMessage, response: ServerResponse): Promise<void> {
  const path = request.url?.split("?", 1)[0] ?? "";
  if (request.method === "GET" && path === "/health") {
    json(response, 200, { status: "ok", profile: "typescript-text-workbench" });
    return;
  }
  if (request.method === "GET" && (path === "/" || path === "/app.js")) {
    try {
      const data = await readFile(join(ROOT, "web", path === "/" ? "index.html" : "app.js"));
      response.writeHead(200, {
        "Content-Type": path === "/" ? "text/html; charset=utf-8" : "text/javascript; charset=utf-8",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'self'"
      });
      response.end(data);
    } catch {
      json(response, 500, { error: "static asset unavailable" });
    }
    return;
  }
  if (request.method === "POST" && path === "/api/analyze") {
    if (!/^application\/json(?:;|$)/i.test(request.headers["content-type"] ?? "")) {
      json(response, 415, { error: "Content-Type must be application/json" });
      return;
    }
    try {
      const data = await readJson(request);
      if (!data || typeof data !== "object" || Array.isArray(data) ||
          !("text" in data) || typeof data.text !== "string" ||
          ("top" in data && data.top !== undefined &&
           (typeof data.top !== "number" || !Number.isInteger(data.top)))) {
        json(response, 400, { error: "expected JSON object with text string and optional integer top" });
        return;
      }
      const payload = data as { text: string; top?: number };
      json(response, 200, analyzeText(payload.text, payload.top));
    } catch (error) {
      if (error instanceof PayloadTooLargeError) json(response, 413, { error: error.message });
      else if (error instanceof SyntaxError || error instanceof TypeError || error instanceof RangeError) {
        json(response, 400, { error: error.message });
      } else json(response, 500, { error: "unexpected request failure" });
    }
    return;
  }
  json(response, 404, { error: "route not found" });
}

export function createAppServer() {
  return createServer((request, response) => {
    void handle(request, response).catch(() => {
      if (!response.headersSent) json(response, 500, { error: "internal server error" });
      else response.destroy();
    });
  });
}

const invoked = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invoked) {
  const port = Number(process.env.PORT ?? "3000");
  if (!Number.isInteger(port) || port < 1 || port > 65_535) {
    console.error("PORT must be an integer from 1 to 65535");
    process.exitCode = 2;
  } else {
    createAppServer().listen(port, "127.0.0.1", () =>
      console.log("Text Workbench: http://127.0.0.1:" + port));
  }
}
