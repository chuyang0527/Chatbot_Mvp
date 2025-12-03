"""主程序入口"""

import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from dotenv import load_dotenv
from src.agent.graph import ChatbotGraph
from src.utils.logger import logger

# 加载环境变量
load_dotenv()

console = Console()


class ChatbotApp:
    """聊天机器人应用"""
    
    def __init__(self):
        self.graph = ChatbotGraph()
        self.chat_history = []
    
    def display_welcome(self):
        """显示欢迎信息"""
        welcome_text = """
# 🤖 智能文档问答聊天机器人

欢迎使用！我可以帮你回答关于已上传文档的问题。

**功能特性：**
- 📄 支持多种文档格式 (PDF, Word, Markdown, TXT)
- 🔍 智能语义检索
- 💬 多轮对话支持
- 📊 完整的调用链追踪 (LangSmith)

**使用说明：**
- 输入你的问题，我会基于文档内容回答
- 输入 'exit' 或 'quit' 退出
- 输入 'clear' 清除对话历史
- 输入 'history' 查看对话历史

---
        """
        console.print(Panel(Markdown(welcome_text), border_style="blue"))
    
    def display_answer(self, result: dict):
        """显示回答"""
        answer = result["answer"]
        citations = result["citations"]
        
        # 显示回答
        console.print("\n[bold green]🤖 助手回答：[/bold green]")
        console.print(Panel(answer, border_style="green"))
        
        # 显示引用
        if citations:
            console.print("\n[bold blue]📚 引用来源：[/bold blue]")
            for cite in citations:
                console.print(
                    f"  [{cite['index']}] {cite['source']} (页码: {cite['page']})"
                )
                console.print(f"      {cite['content'][:100]}...\n")
    
    def run(self):
        """运行聊天机器人"""
        self.display_welcome()
        
        while True:
            try:
                # 获取用户输入
                question = console.input("\n[bold cyan]👤 你的问题：[/bold cyan] ").strip()
                
                if not question:
                    continue
                
                # 处理特殊命令
                if question.lower() in ['exit', 'quit']:
                    console.print("[yellow]再见！👋[/yellow]")
                    break
                
                if question.lower() == 'clear':
                    self.chat_history = []
                    console.print("[yellow]对话历史已清除[/yellow]")
                    continue
                
                if question.lower() == 'history':
                    if not self.chat_history:
                        console.print("[yellow]暂无对话历史[/yellow]")
                    else:
                        for i, h in enumerate(self.chat_history, 1):
                            console.print(f"\n[bold]对话 {i}:[/bold]")
                            console.print(f"  问: {h['question']}")
                            console.print(f"  答: {h['answer'][:100]}...")
                    continue
                
                # 处理问题
                with console.status("[bold green]正在思考...", spinner="dots"):
                    result = self.graph.run(question, self.chat_history)
                
                # 显示结果
                self.display_answer(result)
                
                # 更新历史
                self.chat_history.append({
                    "question": question,
                    "answer": result["answer"]
                })
                
            except KeyboardInterrupt:
                console.print("\n[yellow]再见！👋[/yellow]")
                break
            except Exception as e:
                logger.error(f"发生错误: {e}", exc_info=True)
                console.print(f"[red]❌ 错误: {e}[/red]")


def main():
    """主函数"""
    app = ChatbotApp()
    app.run()


if __name__ == "__main__":
    main()
