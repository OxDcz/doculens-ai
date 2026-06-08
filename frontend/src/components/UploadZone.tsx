import { useState, useCallback } from "react";

export default function UploadZone() {
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (!file) return;
    await uploadFile(file);
  }, []);

  const handleChange = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    await uploadFile(file);
  }, []);

  async function uploadFile(file: File) {
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("chunk_size", "512");

    try {
      const res = await fetch("http://localhost:8000/api/v1/documents/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      style={{
        border: "2px dashed #ccc",
        borderRadius: 12,
        padding: 40,
        textAlign: "center",
        cursor: "pointer",
      }}
    >
      {uploading ? (
        <p>Processing document...</p>
      ) : result ? (
        <div>
          <p>Uploaded: {result.filename}</p>
          <p>Chunks: {result.num_chunks} | Pages: {result.num_pages}</p>
        </div>
      ) : (
        <>
          <p>Drag and drop a PDF, or click to browse</p>
          <input type="file" accept=".pdf,.txt,.md" onChange={handleChange} />
        </>
      )}
    </div>
  );
}
