import UploadZone from "../components/UploadZone";
import SearchBar from "../components/SearchBar";

export default function Dashboard() {
  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: 40 }}>
      <h1>DocuLens AI</h1>
      <p style={{ color: "#666" }}>
        Experimental document intelligence toolkit -- upload, search, and analyze your documents.
      </p>

      <section style={{ marginTop: 40 }}>
        <h2>Upload a Document</h2>
        <UploadZone />
      </section>

      <section style={{ marginTop: 40 }}>
        <h2>Search</h2>
        <SearchBar />
      </section>
    </main>
  );
}
