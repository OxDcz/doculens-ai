"""Health check endpoint."""

import torch
from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/health")
async def health_check():
    """Return system health and GPU availability."""
    gpu_available = torch.cuda.is_available()
    gpu_info = None
    if gpu_available:
        gpu_info = {
            "device_name": torch.cuda.get_device_name(0),
            "device_count": torch.cuda.device_count(),
            "memory_allocated_mb": round(torch.cuda.memory_allocated(0) / 1e6, 2),
            "memory_reserved_mb": round(torch.cuda.memory_reserved(0) / 1e6, 2),
        }

    return {
        "status": "ok",
        "version": "0.1.0",
        "device": "cuda" if gpu_available else "cpu",
        "gpu": gpu_info,
    }
