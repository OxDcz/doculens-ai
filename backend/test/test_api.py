"""Integration tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "device" in data


def test_upload_invalid_file_type():
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("test.exe", b"not a document", "application/octet-stream")},
    )
    assert response.status_code == 400
    assert "Unsupported" in response.json()["detail"]


def test_upload_txt_file():
    content = b"This is a sample document for testing upload functionality."
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("sample.txt", content, "text/plain")},
        data={"chunk_size": 256, "chunk_overlap": 20},
    )
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["filename"] == "sample.txt"
    assert data["num_chunks"] >= 1


def test_get_nonexistent_document():
    response = client.get("/api/v1/documents/nonexistent-id")
    assert response.status_code == 404


def test_search_empty_query():
    response = client.post(
        "/api/v1/search",
        json={"query": "", "top_k": 5},
    )
    assert response.status_code == 400
