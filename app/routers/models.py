from fastapi import APIRouter
from app.models.ollama_models import TagsResponse, ModelInfo, RunningModelsResponse, RunningModelInfo
from app.services.llm_adapter import llm_adapter
from app.config.settings import settings
from app.config.model_manager import model_manager
from datetime import datetime, timedelta
import hashlib

router = APIRouter()

@router.get("/api/tags", response_model=TagsResponse)
async def list_local_models():
    """列出本地模型 - 兼容Ollama格式"""
    models = []
    
    # 获取可用模型列表，模拟为本地模型
    available_models = llm_adapter.get_available_models()
    
    for model_name in available_models:
        # 模拟模型大小（基于模型名称生成一致的大小）
        model_size = hash(model_name) % 5000000000 + 500000000  # 0.5-5GB范围
        
        # 生成digest（匹配Ollama格式）
        digest = hashlib.sha256(model_name.encode()).hexdigest()
        
        # 模拟修改时间（随机过去几天）
        days_ago = hash(model_name) % 30 + 1
        modified_at = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "-07:00"
        
        # 从模型管理器获取模型配置
        model_config = model_manager.get_model_config(model_name)
        if model_config:
            family = model_config.family
            families = model_config.families
            parameter_size = model_config.parameter_size
            quantization = model_config.quantization
        else:
            # 如果配置中没有找到，使用默认值
            family = "unknown"
            families = ["unknown"]
            parameter_size = "7B"
            quantization = "Q4_0"
        
        # 添加:latest后缀（如果没有版本标签）
        display_name = model_name + ":latest" if ":" not in model_name else model_name
        
        model_info = ModelInfo(
            name=display_name,
            model=display_name,
            modified_at=modified_at,
            size=model_size,
            digest=digest,
            details={
                "parent_model": "",
                "format": "gguf",
                "family": family,
                "families": families,
                "parameter_size": parameter_size,
                "quantization_level": quantization
            }
        )
        models.append(model_info)
    
    return TagsResponse(models=models)

@router.get("/api/ps", response_model=RunningModelsResponse)
async def list_running_models():
    """列出当前加载到内存中的模型 - 兼容Ollama格式"""
    running_models = []
    
    # 获取可用模型列表，模拟一些模型正在运行
    available_models = llm_adapter.get_available_models()
    
    # 模拟所有可用模型都在运行（实际场景中，这里应该查询真实的运行状态）
    for i, model_name in enumerate(available_models):
        provider = model_name.split('/')[0] if '/' in model_name else "openai"
        
        # 从模型管理器获取模型大小
        model_config = model_manager.get_model_config(model_name)
        if model_config:
            # 根据参数大小字符串估算字节大小
            param_size = model_config.parameter_size
            if "175B" in param_size:
                model_size = 175000000000
            elif "100B" in param_size:
                model_size = 100000000000
            elif "72B" in param_size:
                model_size = 72000000000
            elif "70B" in param_size:
                model_size = 70000000000
            elif "34B" in param_size:
                model_size = 34000000000
            elif "32B" in param_size:
                model_size = 32000000000
            else:
                model_size = 7000000000  # 默认7B
        else:
            model_size = 7000000000    # 默认7B参数
        
        # 模拟过期时间（5分钟后）
        expires_at = (datetime.now() + timedelta(minutes=5)).isoformat()
        
        # 生成更短的digest（匹配Ollama格式）
        digest = hashlib.sha256(model_name.encode()).hexdigest()[:64]
        
        # 格式化过期时间（包含时区信息）
        expires_at_formatted = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "-07:00"
        
        # 从模型管理器获取模型配置
        if model_config:
            family = model_config.family
            families = model_config.families
            parameter_size = model_config.parameter_size
            quantization = model_config.quantization
        else:
            # 如果配置中没有找到，使用默认值
            family = "unknown"
            families = ["unknown"]
            parameter_size = "7B"
            quantization = "Q4_0"

        running_model = RunningModelInfo(
            name=model_name,
            model=model_name,
            size=model_size,
            digest=digest,
            details={
                "parent_model": "",
                "format": "gguf",
                "family": family,
                "families": families,
                "parameter_size": parameter_size,
                "quantization_level": quantization
            },
            expires_at=expires_at_formatted,
            size_vram=model_size
        )
        running_models.append(running_model)
    
    return RunningModelsResponse(models=running_models)

@router.get("/api/version")
async def get_version():
    """获取版本信息 - 兼容Ollama格式"""
    return {
        "version": settings.app_version,
        "name": settings.app_name,
        "adapter": True,
        "supported_providers": [
            "alibaba",
            "deepseek", 
            "siliconflow",
            "volcengine"
        ]
    }

@router.head("/")
@router.get("/")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "message": "Ollama Adapter is running",
        "version": settings.app_version
    }