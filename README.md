# 02_chat_cli

一个命令行对话程序，支持 DeepSeek 云端和 Ollama 本地模型，支持多轮对话和流式输出，并把历史保存到本地 `history.json`。

## 功能

- 支持 DeepSeek 与 Ollama 模型切换
- 流式输出模型回复
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
LLM_PROVIDER=deepseek

DEEPSEEK_API_KEY=你的密钥
DEEPSEEK_MODEL=deepseek-chat

OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=gemma3:4b
```

切换模型时只改 `LLM_PROVIDER`：

```text
LLM_PROVIDER=deepseek
LLM_PROVIDER=ollama
```

## 运行

```powershell
.\.venv\Scripts\python.exe main.py
```

## 下一步

- 增加 RAG 检索与引用来源
- 增加工具调用和页面界面
