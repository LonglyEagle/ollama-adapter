import litellm
from typing import AsyncGenerator, Dict, Any, List
import json
import time
from datetime import datetime
from app.config.settings import settings
from app.models.ollama_models import GenerateResponse, GenerateStreamResponse, EmbeddingResponse
from app.services.error_handler import handle_litellm_error

class LLMAdapter:
    """LiteLLM适配器服务"""
    
    def __init__(self):
        # 配置LiteLLM
        litellm.set_verbose = False
        
        # 配置各提供商的API密钥
        self._setup_api_keys()
    
    def _setup_api_keys(self):
        """设置各提供商的API密钥"""
        # 设置环境变量方式配置API密钥
        import os
        
        if settings.deepseek_api_key:
            os.environ["DEEPSEEK_API_KEY"] = settings.deepseek_api_key
            
        if settings.volcengine_api_key:
            os.environ["VOLCENGINE_API_KEY"] = settings.volcengine_api_key
    
    def _get_litellm_model(self, ollama_model: str) -> str:
        """转换模型名称为LiteLLM格式"""
        # 将dashscope/和siliconflow/前缀转换为openai/格式
        if ollama_model.startswith("dashscope/"):
            return ollama_model.replace("dashscope/", "openai/")
        elif ollama_model.startswith("siliconflow/"):
            return ollama_model.replace("siliconflow/", "openai/")
        else:
            return ollama_model
    
    def _get_model_config(self, original_model: str) -> dict:
        """根据原始模型名称获取API配置"""
        config = {}
        
        # 阿里百炼模型配置
        if original_model.startswith("dashscope/"):
            if settings.dashscope_api_key:
                config["api_key"] = settings.dashscope_api_key
                config["api_base"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        
        # 硅基流动模型配置
        elif original_model.startswith("siliconflow/"):
            if settings.siliconflow_api_key:
                config["api_key"] = settings.siliconflow_api_key
                config["api_base"] = "https://api.siliconflow.cn/v1"
        
        return config
    
    async def generate_completion(self, 
                                model: str, 
                                prompt: str, 
                                system: str = None,
                                stream: bool = False,
                                **kwargs) -> Any:
        """生成文本完成"""
        try:
            # 构建消息
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            # 调用LiteLLM
            if stream:
                return self._stream_completion(model, messages, **kwargs)
            else:
                return await self._complete_completion(model, messages, **kwargs)
                
        except Exception as e:
            raise handle_litellm_error(e)
    
    async def _complete_completion(self, model: str, messages: List[Dict], **kwargs) -> GenerateResponse:
        """非流式完成"""
        start_time = time.time()
        
        # 获取模型配置
        litellm_model = self._get_litellm_model(model)
        model_config = self._get_model_config(model)
        
        response = await litellm.acompletion(
            model=litellm_model,
            messages=messages,
            stream=False,
            **model_config,
            **kwargs
        )
        
        end_time = time.time()
        duration_ns = int((end_time - start_time) * 1_000_000_000)
        
        return GenerateResponse(
            model=model,
            created_at=datetime.now().isoformat(),
            response=response.choices[0].message.content,
            done=True,
            total_duration=duration_ns,
            eval_count=response.usage.completion_tokens if response.usage else None,
            prompt_eval_count=response.usage.prompt_tokens if response.usage else None
        )
    
    async def _stream_completion(self, original_model: str, messages: List[Dict], **kwargs):
        """流式完成"""
        try:
            # 获取模型配置
            litellm_model = self._get_litellm_model(original_model)
            model_config = self._get_model_config(original_model)
        
            response = await litellm.acompletion(
                model=litellm_model,
                messages=messages,
                stream=True,
                **model_config,
                **kwargs
            )
            
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    
                    # 使用Ollama兼容的格式
                    ollama_response = {
                        "model": original_model,
                        "created_at": datetime.now().isoformat(),
                        "message": {
                            "role": "assistant",
                            "content": content
                        },
                        "done": False
                    }
                    
                    yield json.dumps(ollama_response) + "\n"
            
            # 发送结束标记
            final_response = {
                "model": original_model,
                "created_at": datetime.now().isoformat(),
                "message": {
                    "role": "assistant",
                    "content": ""
                },
                "done": True
            }
            yield json.dumps(final_response) + "\n"
            
        except Exception as e:
            error_response = {
                "error": str(e),
                "model": original_model,
                "done": True
            }
            yield json.dumps(error_response) + "\n"
    
    async def generate(self, request) -> GenerateResponse:
        """生成文本（兼容GenerateRequest）"""
        return await self.generate_completion(
            model=request.model,
            prompt=request.prompt,
            system=request.system,
            stream=False,
            **{k: v for k, v in request.model_dump().items() 
               if k not in ['model', 'prompt', 'system', 'stream'] and v is not None}
        )
    
    async def generate_stream(self, request):
        """生成流式文本（兼容GenerateRequest）"""
        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})
        
        async for chunk in self._stream_completion(
            original_model=request.model,
            messages=messages,
            **{k: v for k, v in request.model_dump().items() 
               if k not in ['model', 'prompt', 'system', 'stream'] and v is not None}
        ):
            yield chunk
    
    async def create_embeddings(self, request) -> EmbeddingResponse:
        """创建嵌入向量（兼容EmbeddingRequest）"""
        return await self.generate_embedding(
            model=request.model,
            prompt=request.prompt,
            **{k: v for k, v in request.model_dump().items() 
               if k not in ['model', 'prompt'] and v is not None}
        )

    async def generate_embedding(self, model: str, prompt: str, **kwargs) -> EmbeddingResponse:
        """生成嵌入向量"""
        try:
            litellm_model = self._get_litellm_model(model)
            model_config = self._get_model_config(model)
            
            response = await litellm.aembedding(
                model=litellm_model,
                input=prompt,
                **model_config,
                **kwargs
            )
            
            # 根据用户反馈的格式处理响应
            if hasattr(response, 'data') and len(response.data) > 0:
                # 响应格式：EmbeddingResponse(data=[{'embedding': [...], 'index': 0, 'object': 'embedding'}])
                embedding_data = response.data[0]

                if isinstance(embedding_data, dict) and 'embedding' in embedding_data:
                    embedding = embedding_data['embedding']
                elif hasattr(embedding_data, 'embedding'):
                    embedding = embedding_data.embedding
                else:
                    # 如果embedding_data本身就是列表
                    embedding = embedding_data if isinstance(embedding_data, list) else []
            else:
                embedding = []
            
            return EmbeddingResponse(
                embedding=embedding
            )
            
        except Exception as e:
            raise handle_litellm_error(e)
    
    def get_available_models(self) -> List[str]:
        """获取可用的模型列表"""
        from app.config.model_manager import model_manager
        return model_manager.get_available_models()

# 全局适配器实例
llm_adapter = LLMAdapter()