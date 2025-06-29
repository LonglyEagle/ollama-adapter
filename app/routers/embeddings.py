from fastapi import APIRouter, HTTPException
from app.models.ollama_models import (
    EmbeddingRequest, EmbeddingResponse,
    EmbedRequest, EmbedResponse
)
from app.services.llm_adapter import llm_adapter
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/api/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    """生成嵌入向量（已废弃，建议使用/api/embed）"""
    try:
        logger.info(f"Embedding request for model: {request.model}")
        
        response = await llm_adapter.create_embeddings(request)
        return response
        
    except Exception as e:
        logger.error(f"Embedding error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/embed", response_model=EmbedResponse)
async def create_embed(request: EmbedRequest):
    """生成嵌入向量（新版API）"""
    try:
        logger.info(f"Embed request for model: {request.model}")
        
        # 将新格式转换为旧格式以兼容现有服务
        if isinstance(request.input, str):
            inputs = [request.input]
        else:
            inputs = request.input
        
        embeddings = []
        for input_text in inputs:
            # 创建兼容的EmbeddingRequest
            embedding_request = EmbeddingRequest(
                model=request.model,
                prompt=input_text,
                options=request.options,
                keep_alive=request.keep_alive
            )
            
            embedding_response = await llm_adapter.create_embeddings(embedding_request)
            embeddings.append(embedding_response.embedding)
        
        # 构造新格式的响应
        embed_response = EmbedResponse(
            model=request.model,
            embeddings=embeddings
        )
        
        return embed_response
        
    except Exception as e:
        logger.error(f"Embed error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))