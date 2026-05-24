import { useState } from "react";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);

  async function handleSearch() {
    try {
      const res = await fetch("http://localhost:8000/api/v1/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 5 }),
      });
      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      console.error("Search failed:", err);
    }
  }

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        placeholder="Search your documents..."
        style={{ width: "100%", padding: 10, fontSize: 16 }}
      />
      {results.map((r: any, i: number) => (
        <div key={i} style={{ padding: 10, borderBottom: "1px solid #eee" }}>
          <small>Score: {r.score.toFixed(3)}</small>
          <p>{r.chunk_text}</p>
        </div>
      ))}
    </div>
  );
}
