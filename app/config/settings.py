from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # 服务配置
    app_name: str = "Ollama Adapter"
    app_version: str = "0.1.0"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = os.getenv("PORT", 11434)  # 使用Ollama默认端口
    
    # 模型提供商API密钥
    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY", "")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    siliconflow_api_key: str = os.getenv("SILICONFLOW_API_KEY", "")
    volcengine_api_key: str = os.getenv("VOLCENGINE_API_KEY", "")
    
    # 日志级别
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()