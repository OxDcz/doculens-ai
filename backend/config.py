"""Application configuration loaded from environment variables."""

from pathlib import Path
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DOCULENS_",
        case_sensitive=False,
    )

    device: Literal["cpu", "cuda", "mps", "rocm"] = "cpu"

    embed_model: str = "BAAI/bge-small-en-v1.5"
    llm_model: str = "microsoft/phi-2"
    summ_model: str = "facebook/bart-large-cnn"

    vector_store: Literal["chromadb"] = "chromadb"
    chroma_persist_dir: str = "./data/chroma"
    default_chunk_size: int = 512
    default_chunk_overlap: int = 50

    host: str = "0.0.0.0"
    port: int = 8000
    max_upload_size_mb: int = 50

    ocr_backend: Optional[Literal["tesseract", "paddleocr"]] = None
    tessdata_prefix: Optional[str] = None

    openai_api_key: Optional[str] = None
    hf_api_token: Optional[str] = None

    @property
    def chroma_path(self) -> Path:
        path = Path(self.chroma_persist_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
