#!/usr/bin/env python3
"""自动下载 Embedding 模型脚本"""

import os
import sys
from pathlib import Path

def download_embedding_model():
    """下载 Sentence Transformers 模型"""
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    model_path = Path(__file__).parent.parent / "model" / "paraphrase-multilingual-MiniLM-L12-v2"
    
    print(f"正在下载模型: {model_name}")
    print(f"保存路径: {model_path}")
    print("模型大小约 470MB，请耐心等待...\n")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # 下载并保存模型
        model = SentenceTransformer(model_name)
        model.save(str(model_path))
        
        print("\n✓ 模型下载完成！")
        print(f"✓ 模型已保存到: {model_path}")
        return True
        
    except ImportError:
        print("✗ 错误: 未安装 sentence-transformers")
        print("请运行: pip install sentence-transformers")
        return False
        
    except Exception as e:
        print(f"✗ 下载失败: {e}")
        return False

def download_ollama_model():
    """下载 Ollama 模型（需要 Ollama 服务运行）"""
    model_name = "deepseek-r1:7b"
    
    print(f"\n正在下载 Ollama 模型: {model_name}")
    print("注意: 需要 Ollama 服务正在运行\n")
    
    try:
        import subprocess
        result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✓ Ollama 模型下载完成: {model_name}")
            return True
        else:
            print(f"✗ 下载失败: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("✗ 错误: 未找到 ollama 命令")
        print("请确保 Ollama 已安装并在 PATH 中")
        return False
        
    except Exception as e:
        print(f"✗ 下载失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("  模型下载工具")
    print("=" * 60)
    print()
    
    # 下载 Embedding 模型
    embedding_success = download_embedding_model()
    
    # 询问是否下载 Ollama 模型
    if embedding_success:
        print("\n" + "=" * 60)
        response = input("是否下载 Ollama 模型？(y/n): ").strip().lower()
        if response == 'y':
            download_ollama_model()
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
