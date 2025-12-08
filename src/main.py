"""主程序入口"""

import sys
from pathlib import Path

from config import Config
from document_processor import DocumentProcessor
from vector_store import VectorStore
from chat_agent import ChatAgent


def print_banner():
    """打印欢迎信息"""
    print("=" * 60)
    print("  聊天机器人 RAG 系统")
    print("  基于 LangGraph + LangChain + Ollama DeepSeek")
    print("=" * 60)
    print()


def print_help():
    """打印帮助信息"""
    print("\n可用命令:")
    print("  upload <文件路径>  - 上传并处理文档")
    print("  clear             - 清空向量库")
    print("  history           - 清空对话历史")
    print("  help              - 显示帮助")
    print("  exit/quit         - 退出程序")
    print("\n直接输入问题开始对话\n")


def main():
    """主函数"""
    # 初始化配置
    Config.ensure_directories()
    Config.setup_langsmith()
    
    print_banner()
    print("正在初始化系统...")
    
    # 初始化组件
    doc_processor = DocumentProcessor()
    vector_store = VectorStore()
    chat_agent = ChatAgent(vector_store)
    
    print("✓ 系统初始化完成\n")
    print_help()
    
    # 主循环
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            
            # 处理命令
            if user_input.lower() in ["exit", "quit"]:
                print("\n再见！")
                break
            
            elif user_input.lower() == "help":
                print_help()
                continue
            
            elif user_input.lower().startswith("upload "):
                file_path = user_input[7:].strip()
                try:
                    print(f"\n正在处理文档: {file_path}")
                    documents = doc_processor.load_document(file_path)
                    vector_store.add_documents(documents)
                    print(f"✓ 文档已成功上传并向量化")
                except Exception as e:
                    print(f"✗ 文档处理失败: {e}")
                continue
            
            elif user_input.lower() == "clear":
                vector_store.clear()
                continue
            
            elif user_input.lower() == "history":
                chat_agent.clear_history()
                continue
            
            # 处理对话
            print("\n思考中...")
            result = chat_agent.chat(user_input)

            print(f"\n机器人: {result['answer']}")
            
            # 显示引用的上下文（可选）
            if "--debug" in sys.argv:
                print(f"\n[调试] 检索到的上下文:\n{result['context']}")
        
        except KeyboardInterrupt:
            print("\n\n程序被中断")
            break
        except Exception as e:
            print(f"\n✗ 发生错误: {e}")
            if "--debug" in sys.argv:
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    main()
