"""DocuLens AI -- FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import documents, health, search
from backend.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting DocuLens AI on device: {settings.device}")
    yield
    print("Shutting down DocuLens AI")


app = FastAPI(
    title="DocuLens AI",
    description="AI-powered document intelligence toolkit (experimental)",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])
