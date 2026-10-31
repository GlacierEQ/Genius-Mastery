/** Typed, deterministic Unicode word statistics. */
export interface WordCount { word: string; count: number }
export interface Analysis {
  characters: number;
  lines: number;
  words: number;
  unique_words: number;
  top_words: WordCount[];
}
const WORD = /[\p{L}\p{N}]+(?:['’ʻ][\p{L}\p{N}]+)*/gu;

export function analyzeText(text: string, top = 10): Analysis {
  if (typeof text !== "string" || text.length > 20_000) {
    throw new TypeError("text must be a string with at most 20000 UTF-16 units");
  }
  if (!Number.isInteger(top) || top < 1 || top > 20) {
    throw new RangeError("top must be an integer between 1 and 20");
  }
  const words = Array.from(text.matchAll(WORD), match => match[0].toLowerCase());
  const counts = new Map<string, number>();
  for (const word of words) counts.set(word, (counts.get(word) ?? 0) + 1);
  const ranked = Array.from(counts, ([word, count]) => ({ word, count }))
    .sort((a, b) => b.count - a.count || (a.word < b.word ? -1 : a.word > b.word ? 1 : 0))
    .slice(0, top);
  return {
    characters: Array.from(text).length,
    lines: text.length ? text.split(/\r\n|\r|\n/).length : 0,
    words: words.length,
    unique_words: counts.size,
    top_words: ranked
  };
}
