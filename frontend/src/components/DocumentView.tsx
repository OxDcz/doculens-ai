interface DocumentViewProps {
  documentId: string;
  filename: string;
}

export default function DocumentView({ documentId, filename }: DocumentViewProps) {
  return (
    <div style={{ padding: 20 }}>
      <h2>{filename}</h2>
      <p>Document ID: {documentId}</p>
      <section style={{ marginTop: 20 }}>
        <h3>Ask a Question</h3>
        <input
          type="text"
          placeholder="What is this document about?"
          style={{ width: "100%", padding: 8 }}
        />
        <button style={{ marginTop: 8 }}>Ask</button>
      </section>
      <section style={{ marginTop: 20 }}>
        <h3>Summary</h3>
        <button>Generate Summary</button>
      </section>
    </div>
  );
}
