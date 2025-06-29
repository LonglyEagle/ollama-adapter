import json
import os
from typing import Dict, List, Optional
from pathlib import Path

class ModelConfig:
    """模型配置类"""
    def __init__(self, name: str, config: Dict):
        self.name = name
        self.provider = config.get('provider', 'unknown')
        self.family = config.get('family', 'unknown')
        self.families = config.get('families', [self.family])
        self.parameter_size = config.get('parameter_size', '7B')
        self.quantization = config.get('quantization', 'Q4_0')
        self.format = config.get('format', 'gguf')
        self.description = config.get('description', '')
        self.context_length = config.get('context_length', 4096)
        self.capabilities = config.get('capabilities', ['text', 'chat'])

class ModelManager:
    """模型配置管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            # 默认配置文件路径
            config_path = Path(__file__).parent / 'models_config.json'
        
        self.config_path = config_path
        self._models: Dict[str, ModelConfig] = {}
        self._default_settings = {}
        self.load_config()
    
    def load_config(self):
        """加载模型配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 加载默认设置
            self._default_settings = config_data.get('default_settings', {})
            
            # 加载模型配置
            models_data = config_data.get('models', {})
            for model_name, model_config in models_data.items():
                # 合并默认设置
                merged_config = {**self._default_settings, **model_config}
                self._models[model_name] = ModelConfig(model_name, merged_config)
                
        except FileNotFoundError:
            print(f"警告: 模型配置文件 {self.config_path} 不存在，使用默认配置")
            self._load_default_config()
        except json.JSONDecodeError as e:
            print(f"错误: 模型配置文件格式错误: {e}")
            self._load_default_config()
    
    def _load_default_config(self):
        """加载默认配置（当配置文件不存在或损坏时使用）"""
        default_models = [
            "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo",
            "claude-3-opus", "claude-3-sonnet", "claude-3-haiku",
            "dashscope/qwen-turbo", "dashscope/qwen-plus", "dashscope/qwen-max",
            "deepseek/deepseek-chat", "deepseek/deepseek-coder",
            "siliconflow/Yi-34B-Chat", "siliconflow/Meta-Llama-3-8B-Instruct",
            "volcengine/doubao-lite-4k", "volcengine/doubao-pro-4k",
            "gemini/gemini-pro", "gemini/gemini-pro-vision",
            "ollama/llama2", "ollama/codellama"
        ]
        
        self._default_settings = {
            "format": "gguf",
            "quantization": "Q4_0",
            "context_length": 4096,
            "capabilities": ["text", "chat"]
        }
        
        for model_name in default_models:
            config = {
                "provider": model_name.split('/')[0] if '/' in model_name else "openai",
                "family": "llama",
                "families": ["llama"],
                "parameter_size": "7B",
                "description": f"Default configuration for {model_name}"
            }
            merged_config = {**self._default_settings, **config}
            self._models[model_name] = ModelConfig(model_name, merged_config)
    
    def get_available_models(self) -> List[str]:
        """获取所有可用模型名称列表"""
        return list(self._models.keys())
    
    def get_model_config(self, model_name: str) -> Optional[ModelConfig]:
        """获取指定模型的配置"""
        return self._models.get(model_name)
    
    def get_models_by_provider(self, provider: str) -> List[str]:
        """根据提供商获取模型列表"""
        return [name for name, config in self._models.items() 
                if config.provider == provider]
    
    def get_models_by_capability(self, capability: str) -> List[str]:
        """根据能力获取模型列表"""
        return [name for name, config in self._models.items() 
                if capability in config.capabilities]
    
    def add_model(self, model_name: str, config: Dict):
        """动态添加模型配置"""
        merged_config = {**self._default_settings, **config}
        self._models[model_name] = ModelConfig(model_name, merged_config)
    
    def remove_model(self, model_name: str) -> bool:
        """移除模型配置"""
        if model_name in self._models:
            del self._models[model_name]
            return True
        return False
    
    def save_config(self):
        """保存当前配置到文件"""
        config_data = {
            "default_settings": self._default_settings,
            "models": {}
        }
        
        for model_name, model_config in self._models.items():
            config_data["models"][model_name] = {
                "provider": model_config.provider,
                "family": model_config.family,
                "families": model_config.families,
                "parameter_size": model_config.parameter_size,
                "quantization": model_config.quantization,
                "format": model_config.format,
                "description": model_config.description,
                "context_length": model_config.context_length,
                "capabilities": model_config.capabilities
            }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)

# 全局模型管理器实例
model_manager = ModelManager()