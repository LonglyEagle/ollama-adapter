"""数据模型模块"""

from .ollama_models import (
    GenerateRequest,
    GenerateResponse,
    GenerateStreamResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    ModelInfo,
    TagsResponse,
    ErrorResponse
)

__all__ = [
    "GenerateRequest",
    "GenerateResponse", 
    "GenerateStreamResponse",
    "EmbeddingRequest",
    "EmbeddingResponse",
    "ModelInfo",
    "TagsResponse",
    "ErrorResponse"
]