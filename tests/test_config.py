"""配置模块测试"""

import pytest
from pathlib import Path
from src.config import Config


def test_config_paths():
    """测试配置路径"""
    assert Config.BASE_DIR.exists()
    assert isinstance(Config.CHUNK_SIZE, int)
    assert Config.CHUNK_SIZE > 0


def test_ensure_directories():
    """测试目录创建"""
    Config.ensure_directories()
    assert Config.UPLOAD_DIR.exists()
    assert Config.VECTOR_DB_DIR.exists()


def test_ollama_config():
    """测试 Ollama 配置"""
    assert Config.OLLAMA_BASE_URL.startswith("http")
    assert Config.OLLAMA_MODEL
    assert Config.LLM_TEMPERATURE >= 0
    assert Config.LLM_TEMPERATURE <= 2
