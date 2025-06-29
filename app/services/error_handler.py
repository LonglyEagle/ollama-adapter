from fastapi import HTTPException
from typing import Any
import litellm
from app.models.ollama_models import ErrorResponse

def handle_litellm_error(error: Exception) -> HTTPException:
    """处理LiteLLM异常并转换为Ollama风格的错误"""
    
    # LiteLLM认证错误
    if isinstance(error, litellm.AuthenticationError):
        return HTTPException(
            status_code=401,
            detail=ErrorResponse(
                error="Authentication failed",
                code=401,
                details=str(error)
            ).model_dump()
        )
    
    # LiteLLM权限错误
    if isinstance(error, litellm.AuthenticationError):
        return HTTPException(
            status_code=403,
            detail=ErrorResponse(
                error="Permission denied",
                code=403,
                details=str(error)
            ).model_dump()
        )
    
    # LiteLLM速率限制错误
    if isinstance(error, litellm.RateLimitError):
        return HTTPException(
            status_code=429,
            detail=ErrorResponse(
                error="Rate limit exceeded",
                code=429,
                details=str(error)
            ).model_dump()
        )
    
    # LiteLLM无效请求错误
    if isinstance(error, litellm.BadRequestError):
        return HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error="Invalid request",
                code=400,
                details=str(error)
            ).model_dump()
        )
    
    # LiteLLM服务不可用错误
    if isinstance(error, litellm.ServiceUnavailableError):
        return HTTPException(
            status_code=503,
            detail=ErrorResponse(
                error="Service unavailable",
                code=503,
                details=str(error)
            ).model_dump()
        )
    
    # LiteLLM超时错误
    if isinstance(error, litellm.Timeout):
        return HTTPException(
            status_code=408,
            detail=ErrorResponse(
                error="Request timeout",
                code=408,
                details=str(error)
            ).model_dump()
        )
    
    # LiteLLM API连接错误
    if isinstance(error, litellm.APIConnectionError):
        return HTTPException(
            status_code=502,
            detail=ErrorResponse(
                error="API connection failed",
                code=502,
                details=str(error)
            ).model_dump()
        )
    
    # LiteLLM内容过滤错误
    if isinstance(error, litellm.ContentPolicyViolationError):
        return HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error="Content policy violation",
                code=400,
                details=str(error)
            ).model_dump()
        )
    
    # 模型不存在错误
    if "model" in str(error).lower() and "not found" in str(error).lower():
        return HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error="Model not found",
                code=404,
                details=str(error)
            ).model_dump()
        )
    
    # 通用LiteLLM错误
    if isinstance(error, litellm.APIError):
        return HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="LLM API error",
                code=500,
                details=str(error)
            ).model_dump()
        )
    
    # 其他未知错误
    return HTTPException(
        status_code=500,
        detail=ErrorResponse(
            error="Internal server error",
            code=500,
            details=str(error)
        ).model_dump()
    )

def handle_validation_error(error: Any) -> HTTPException:
    """处理请求验证错误"""
    return HTTPException(
        status_code=422,
        detail=ErrorResponse(
            error="Validation error",
            code=422,
            details=str(error)
        ).model_dump()
    )

def handle_model_not_found(model_name: str) -> HTTPException:
    """处理模型未找到错误"""
    return HTTPException(
        status_code=404,
        detail=ErrorResponse(
            error=f"Model '{model_name}' not found",
            code=404,
            details=f"Available models: {', '.join(['qwen2:7b', 'qwen2:14b', 'qwen2:72b', 'deepseek-chat', 'deepseek-coder'])}"
        ).model_dump()
    )