// @ts-check
/** Browser client, kept JavaScript-compatible and TypeScript-checkable. */
const form = document.querySelector("#analyze-form");
const input = document.querySelector("#text");
const result = document.querySelector("#result");
if (!(form instanceof HTMLFormElement) || !(input instanceof HTMLTextAreaElement) || !(result instanceof HTMLOutputElement)) {
  throw new Error("Text Workbench requires its form, textarea and output elements");
}
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.textContent = "Analyzing…";
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input.value, top: 10 })
    });
    /** @typedef {{ word: string, count: number }} WordCount */
    /** @typedef {{ error?: string, words: number, unique_words: number, characters: number, top_words: WordCount[] }} AnalysisResult */
    const payload = /** @type {AnalysisResult} */ (await response.json());
    if (!response.ok) throw new Error(String(payload.error ?? ("HTTP " + response.status)));
    const rows = payload.top_words.map(row => row.word + ": " + row.count).join("\n");
    result.textContent = "Words: " + payload.words + " | Unique: " + payload.unique_words +
      " | Characters: " + payload.characters + "\n" + rows;
  } catch (error) {
    result.textContent = "Unable to analyze: " + (error instanceof Error ? error.message : String(error));
  }
});
