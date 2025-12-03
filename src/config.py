"""配置管理模块"""

import logging
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """应用配置"""
    
    # OpenAI 配置
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    
    # LangSmith 配置
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "chatbot-mvp"
    langchain_endpoint: str = "https://api.smith.langchain.com"
    
    # 向量数据库配置
    vector_db_path: str = "./data/vector_db"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # 检索配置
    top_k: int = 4
    similarity_threshold: float = 0.7
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "./logs/chatbot.log"
    enable_file_logging: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_log_level(self) -> int:
        """获取日志级别"""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        return level_map.get(self.log_level.upper(), logging.INFO)


def get_settings() -> Settings:
    """获取配置实例"""
    return Settings()
