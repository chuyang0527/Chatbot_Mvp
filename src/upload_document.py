"""文档上传工具"""

import argparse
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from src.document_processor import DocumentLoader, TextSplitter
from src.retrieval import VectorStoreManager
from src.utils.logger import logger

load_dotenv()
console = Console()


def upload_document(file_path: str):
    """
    上传并处理文档
    
    Args:
        file_path: 文档路径
    """
    try:
        console.print(f"[bold blue]📄 开始处理文档: {file_path}[/bold blue]")
        
        # 1. 加载文档
        documents = DocumentLoader.load(file_path)
        console.print(f"[green]✓[/green] 文档加载完成，共 {len(documents)} 页")
        
        # 2. 分割文档
        splitter = TextSplitter()
        chunks = splitter.split(documents)
        console.print(f"[green]✓[/green] 文档分割完成，共 {len(chunks)} 个片段")
        
        # 3. 向量化并存储
        vector_store = VectorStoreManager()
        ids = vector_store.add_documents(chunks)
        console.print(f"[green]✓[/green] 文档已添加到向量数据库，ID 数量: {len(ids)}")
        
        console.print(f"\n[bold green]✅ 文档处理完成！[/bold green]")
        console.print(f"文件: {file_path}")
        console.print(f"片段数: {len(chunks)}")
        console.print(f"现在可以开始提问了！")
        
    except Exception as e:
        logger.error(f"文档处理失败: {e}", exc_info=True)
        console.print(f"[red]❌ 错误: {e}[/red]")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="上传文档到向量数据库")
    parser.add_argument(
        "--file",
        "-f",
        required=True,
        help="文档路径 (支持 PDF, DOCX, MD, TXT)"
    )
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        console.print(f"[red]❌ 文件不存在: {args.file}[/red]")
        return
    
    upload_document(args.file)


if __name__ == "__main__":
    main()
