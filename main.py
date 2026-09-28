import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "history.json"
MODEL = "deepseek-chat"
MAX_HISTORY_MESSAGES = 20

load_dotenv(BASE_DIR / ".env", override=True)


def create_client():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("没有找到 DEEPSEEK_API_KEY，请检查项目根目录的 .env 文件。")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )


def load_history():
    """读取本地对话历史；文件不存在或损坏时从空对话开始。"""
    if not DATA_FILE.exists():
        return []

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("history.json 读取失败，已从空对话开始。")
        return []

    if isinstance(data, list):
        return data
    return []


def save_history(messages):
    """把完整对话保存到 history.json。"""
    DATA_FILE.write_text(
        json.dumps(messages, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def trim_history(messages):
    """保留 system 消息和最近若干条对话，避免上下文无限增长。"""
    system_messages = [m for m in messages if m.get("role") == "system"]
    chat_messages = [m for m in messages if m.get("role") != "system"]
    return system_messages + chat_messages[-MAX_HISTORY_MESSAGES:]


def ask_model(client, messages):
    """把消息发送给 DeepSeek，并返回模型的文本回复。"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=trim_history(messages),
        temperature=0.7,
    )
    return response.choices[0].message.content


def main():
    try:
        client = create_client()
    except RuntimeError as error:
        print(error)
        return

    messages = load_history()
    print("DeepSeek 对话程序已启动。输入 exit、quit 或 退出 结束。")

    while True:
        user_input = input("你：").strip()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "退出"}:
            print("再见。")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            reply = ask_model(client, messages)
        except Exception as error:
            messages.pop()
            print(f"调用模型失败：{error}")
            continue

        print(f"DeepSeek：{reply}")
        messages.append({"role": "assistant", "content": reply})
        save_history(messages)


if __name__ == "__main__":
    main()
