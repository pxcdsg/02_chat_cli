# 02_chat_cli

一个命令行 DeepSeek 对话程序，支持多轮对话，并把历史保存到本地
`history.json`。

## 功能

- 调用 DeepSeek 的 OpenAI 兼容接口
- 保留最近 20 条对话消息
- 每次回复后保存对话历史
- 从 `.env` 读取 API 密钥，密钥不进入 Git

## 安装

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 配置

复制 `.env.example` 为 `.env`，填入真实密钥：

```text
DEEPSEEK_API_KEY=你的密钥
```

## 运行

```powershell
.\.venv\Scripts\python.exe main.py
```

## 下一步

- 增加流式输出
- 增加 Ollama 本地模型切换
- 增加 RAG 检索与引用来源
