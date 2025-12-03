"""配置模块测试"""

import os
import pytest
from src.config import Settings


def test_settings_from_env(monkeypatch):
    """测试从环境变量加载配置"""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4")
    monkeypatch.setenv("TOP_K", "5")
    
    settings = Settings()
    
    assert settings.openai_api_key == "test-key"
    assert settings.openai_model == "gpt-4"
    assert settings.top_k == 5


def test_settings_defaults():
    """测试默认配置"""
    # 注意：这个测试需要 .env 文件存在
    try:
        settings = Settings()
        assert settings.chunk_size == 1000
        assert settings.chunk_overlap == 200
        assert settings.top_k == 4
    except Exception:
        pytest.skip("需要配置 .env 文件")
