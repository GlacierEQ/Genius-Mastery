import assert from "node:assert/strict";
import { test } from "node:test";
import type { AddressInfo } from "node:net";
import { analyzeText } from "../src/analysis.ts";
import { createAppServer } from "../src/server.ts";

test("Unicode counts are stable; boundaries fail correctly", () => {
  const report = analyzeText("Hawaiʻi HAWAIʻI\nHello hello\n");
  assert.equal(report.words, 4);
  assert.equal(report.lines, 3);
  assert.deepEqual(report.top_words, [{ word: "hawaiʻi", count: 2 }, { word: "hello", count: 2 }]);
  assert.deepEqual(analyzeText(""), { characters: 0, lines: 0, words: 0, unique_words: 0, top_words: [] });
  assert.throws(() => analyzeText("x", 0), RangeError);
  assert.throws(() => analyzeText("x", 21), RangeError);
  assert.throws(() => analyzeText("x".repeat(20_001)), TypeError);
});

test("health, actual UI assets, working API, negative HTTP paths", async () => {
  const server = createAppServer();
  await new Promise<void>(resolve => server.listen(0, "127.0.0.1", resolve));
  const base = "http://127.0.0.1:" + (server.address() as AddressInfo).port;
  try {
    let res = await fetch(base + "/health");
    assert.equal(res.status, 200);
    assert.equal((await res.json()).status, "ok");
    res = await fetch(base);
    assert.equal(res.status, 200);
    assert.match(await res.text(), /<form id="analyze-form">/);
    res = await fetch(base + "/app.js");
    assert.equal(res.status, 200);
    assert.match(await res.text(), /addEventListener/);
    res = await fetch(base + "/api/analyze", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ text: "one one two" })
    });
    assert.equal(res.status, 200);
    assert.deepEqual((await res.json()).top_words[0], { word: "one", count: 2 });
    res = await fetch(base + "/api/analyze", { method: "POST", headers: { "content-type": "application/json" }, body: "{" });
    assert.equal(res.status, 400);
    res = await fetch(base + "/api/analyze", { method: "POST", headers: { "content-type": "text/plain" }, body: "hello" });
    assert.equal(res.status, 415);
    res = await fetch(base + "/api/analyze", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ text: "x", top: 0 }) });
    assert.equal(res.status, 400);
    res = await fetch(base + "/api/analyze", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ text: "x".repeat(70_000) }) });
    assert.equal(res.status, 413);
    res = await fetch(base + "/../does-not-exist");
    assert.equal(res.status, 404);
    assert.equal(res.headers.get("access-control-allow-origin"), null);
  } finally {
    await new Promise<void>((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
  }
});
