### 项目简介

本项目实现一个简易代码审查Agent。 

实现完整Agent循环：输入 → 推理 → 工具调用 → 输出。 

功能： 

1. 可以直接接收用户粘贴的代码，做代码审查，找出Bug、坏味道、给出重构建议

2. 支持调用工具读取本地代码文件，对磁盘上的py文件做审查 
3.  具备对话上下文记忆，多轮对话可以记住上一轮的代码 
4.  错误处理：文件不存在、解析异常、循环次数限制

### 核心技术栈

* Python 
* LangChain Agent框架 
* 通义千问 qwen‑turbo LLM 
* 自定义工具：读取本地代码文件

### 项目目录

├── main.py              # Agent 主程序 & 命令行交互入口 

├── read_code_tool.py    # 自定义工具：读取本地代码文件 

├── demo_code.py         # 用于测试的示例代码 

├── requirements.txt     # 依赖包 

├── .env                 # API 密钥配置（不提交公开仓库） 

└── README.md            # 项目文档

### Agent架构说明

1. System Prompt 定义 Agent 角色为代码审查专家
2. 工具调用 Agent：大模型自主判断是否需要调用读取文件工具
3. AgentExecutor 负责执行 Agent 循环，设置解析错误捕获，最大迭代次数，防止死循环
4. ChatMessageHistory 实现多轮上下文记忆
5. 命令行 CLI 作为交互界面