from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    """Ollama生成请求模型"""
    model: str
    prompt: str
    suffix: Optional[str] = None
    images: Optional[List[str]] = None
    think: Optional[bool] = None
    format: Optional[Union[str, Dict[str, Any]]] = None
    options: Optional[Dict[str, Any]] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    stream: Optional[bool] = False
    raw: Optional[bool] = False
    keep_alive: Optional[Union[int, str]] = None

class GenerateResponse(BaseModel):
    """Ollama生成响应模型"""
    model: str
    created_at: str
    response: str
    done: bool
    done_reason: Optional[str] = None
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None

class GenerateStreamResponse(BaseModel):
    """Ollama流式生成响应模型"""
    model: str
    created_at: str
    response: str
    done: bool
    done_reason: Optional[str] = None
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None

class Message(BaseModel):
    """聊天消息模型"""
    role: str  # system, user, assistant, tool
    content: str
    thinking: Optional[str] = None
    images: Optional[List[str]] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None

class Tool(BaseModel):
    """工具定义模型"""
    type: str
    function: Dict[str, Any]

class ChatRequest(BaseModel):
    """Ollama聊天请求模型"""
    model: str
    messages: List[Message]
    tools: Optional[List[Tool]] = None
    think: Optional[bool] = None
    format: Optional[Union[str, Dict[str, Any]]] = None
    options: Optional[Dict[str, Any]] = None
    stream: Optional[bool] = False
    keep_alive: Optional[Union[int, str]] = None

class ChatResponse(BaseModel):
    """Ollama聊天响应模型"""
    model: str
    created_at: str
    message: Message
    done: bool
    done_reason: Optional[str] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None

class EmbeddingRequest(BaseModel):
    """Ollama嵌入请求模型（已废弃，使用EmbedRequest）"""
    model: str
    prompt: str
    options: Optional[Dict[str, Any]] = None
    keep_alive: Optional[Union[int, str]] = None

class EmbeddingResponse(BaseModel):
    """Ollama嵌入响应模型（已废弃，使用EmbedResponse）"""
    embedding: List[float]

class EmbedRequest(BaseModel):
    """Ollama新版嵌入请求模型"""
    model: str
    input: Union[str, List[str]]
    truncate: Optional[bool] = None
    options: Optional[Dict[str, Any]] = None
    keep_alive: Optional[Union[int, str]] = None

class EmbedResponse(BaseModel):
    """Ollama新版嵌入响应模型"""
    model: str
    embeddings: List[List[float]]
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None

class ModelInfo(BaseModel):
    """模型信息"""
    name: str
    model: str
    modified_at: str
    size: int
    digest: str
    details: Dict[str, Any]

class TagsResponse(BaseModel):
    """模型列表响应"""
    models: List[ModelInfo]

class RunningModelInfo(BaseModel):
    """运行中的模型信息"""
    name: str
    model: str
    size: int
    digest: str
    details: Dict[str, Any]
    expires_at: str
    size_vram: int

class RunningModelsResponse(BaseModel):
    """运行中模型列表响应"""
    models: List[RunningModelInfo]

class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str
    code: Optional[int] = None
    details: Optional[str] = None