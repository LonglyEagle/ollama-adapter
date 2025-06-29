from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.models.ollama_models import (
    GenerateRequest, GenerateResponse, GenerateStreamResponse,
    ChatRequest, ChatResponse, Message
)
from app.services.llm_adapter import llm_adapter
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/api/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """生成文本接口 - 兼容Ollama格式"""
    try:
        logger.info(f"Generating text with model: {request.model}, stream: {request.stream}")
        
        # 处理流式请求
        if request.stream:
            async def stream_generator():
                async for chunk in await llm_adapter.generate_completion(
                    model=request.model,
                    prompt=request.prompt,
                    system=request.system,
                    stream=True,
                    **(request.options or {})
                ):
                    yield chunk
            
            return StreamingResponse(
                stream_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "text/event-stream; charset=utf-8"
                }
            )
        
        # 处理非流式请求
        response = await llm_adapter.generate_completion(
            model=request.model,
            prompt=request.prompt,
            system=request.system,
            stream=False,
            **(request.options or {})
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to generate text",
                "details": str(e)
            }
        )

@router.post("/api/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """聊天完成接口"""
    try:
        logger.info(f"Chat completion request for model: {request.model}")
        
        # 将ChatRequest转换为GenerateRequest以兼容现有服务
        # 分离system消息和其他消息
        system_message = None
        prompt_parts = []
        
        for message in request.messages:
            if message.role == "system":
                system_message = message.content
            elif message.role == "user":
                prompt_parts.append(f"User: {message.content}")
            elif message.role == "assistant":
                prompt_parts.append(f"Assistant: {message.content}")
        
        combined_prompt = "\n".join(prompt_parts)
        
        # 创建兼容的GenerateRequest
        generate_request = GenerateRequest(
            model=request.model,
            prompt=combined_prompt,
            system=system_message,
            format=request.format,
            options=request.options,
            stream=request.stream,
            keep_alive=request.keep_alive
        )
        
        if request.stream:
            return StreamingResponse(
                llm_adapter.generate_stream(generate_request),
                media_type="application/x-ndjson"
            )
        else:
            response = await llm_adapter.generate_completion(
                model=generate_request.model,
                prompt=generate_request.prompt,
                system=generate_request.system,
                stream=False,
                **(generate_request.options or {})
            )
            
            # 将GenerateResponse转换为ChatResponse
            chat_response = ChatResponse(
                model=response.model,
                created_at=response.created_at,
                message=Message(
                    role="assistant",
                    content=response.response
                ),
                done=response.done,
                done_reason=response.done_reason,
                total_duration=response.total_duration,
                load_duration=response.load_duration,
                prompt_eval_count=response.prompt_eval_count,
                prompt_eval_duration=response.prompt_eval_duration,
                eval_count=response.eval_count,
                eval_duration=response.eval_duration
            )
            return chat_response
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Chat completion error: {str(e)}")
        logger.error(f"Full traceback: {error_details}")
        raise HTTPException(status_code=500, detail=str(e))