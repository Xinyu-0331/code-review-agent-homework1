from langchain.tools import tool
import os

@tool
def read_local_code_file(file_path: str) -> str:
    """
    读取本地磁盘上的代码文件，获取全部源代码文本
    参数:
        file_path: 本地代码文件的路径，例如 ./demo_code.py
    返回:
        文件的全部代码字符串，如果文件不存在返回错误提示
    """
    if not os.path.exists(file_path):
        return f"错误：文件 {file_path} 不存在，请检查路径。"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return content
    except UnicodeDecodeError:
        return f"错误：文件 {file_path} 编码不是utf-8，读取失败。"
    except Exception as e:
        return f"读取文件异常：{str(e)}"

# 导出工具列表
tools = [read_local_code_file]
