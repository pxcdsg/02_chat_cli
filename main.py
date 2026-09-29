import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
#上面是导入本代码需要用到的包，但是我不知道每个包具体是导入来干什么的。


BASE_DIR = Path(__file__).parent#这段我不理解是做什么的
DATA_FILE = BASE_DIR / "history.json"#这个文件我知道是用来记录对话内容的，但是我不不知道BASE_DIR / 是上面语法，我好像没见过。
MODEL = "deepseek-chat"#这个是定义所使用的大语言模型
MAX_HISTORY_MESSAGES = 20#这个是定义最大的上下文条数

load_dotenv(BASE_DIR / ".env", override=True)#这段我知道是强制使用.env中的密钥，但是我不值得load_dotenv（）这个函数是什么意思。

#定义一个链接第三方大语言模型的函数，接入密钥，要是密钥不存在的话就输出：没有找到 DEEPSEEK_API_KEY，请检查项目根目录的 .env 文件。
# 但是我不知道os.getenv这个函数是什么意思
#最终返回一个带有baseURL和api_key的内容，我不知道这个OpenAI（）是什么格式的返回。
# 但是我能大概明白这个应该是想和deepseek去建立链接，因为我用codex++或者ccswitch还有进行一些大模型配置的时候好像都需要填写这类内容。
def create_client():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("没有找到 DEEPSEEK_API_KEY，请检查项目根目录的 .env 文件。")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

#定义一个函数，首先判断DATA_FILE是否为空，若为空则返回一个[]。这是一个空列表吗？
#后面的json.loads这个函数我没看懂，还有isinstance这个函数我也没看懂
#这个整体的一个语言我不太明白。
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

#这是定义了一个对话保存函数，其中json.dumps这个函数我不知道是什么意思，然后把字符编码格式改为了utf-8
def save_history(messages):
    """把完整对话保存到 history.json。"""
    DATA_FILE.write_text(
        json.dumps(messages, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

#这些代码我都看不太懂，上下文目前就是靠只保留最近的几点来解决上下文溢出的内容吗？我看面试好像很多都喜欢问我们自己的项目是怎么解决上下文的问题的。
def trim_history(messages):
    """保留 system 消息和最近若干条对话，避免上下文无限增长。"""
    system_messages = [m for m in messages if m.get("role") == "system"]
    chat_messages = [m for m in messages if m.get("role") != "system"]
    return system_messages + chat_messages[-MAX_HISTORY_MESSAGES:]
#拼接固定system消息和最近的MAX_HISTORY_MESSAGES这个数量的对话messages


#这个就是与将消息发送给Deepseek，然后接收deepseek的回复并返回。
def ask_model(client, messages):
    # 流式发送，边接收边打印，返回完整文本
    stream = client.chat.completions.create(
        model=MODEL,
        messages=trim_history(messages),
        temperature=0.7,
        stream=True,
    )

    print('DeepSeek：', end='', flush=True)

    parts = []
    for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        if delta and delta.content:
            print(delta.content, end='', flush=True)
            parts.append(delta.content)

    print()
    return ''.join(parts)


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
            print(f'\n调用模型失败：{error}')
            continue

        messages.append({"role": "assistant", "content": reply})
        save_history(messages)


if __name__ == "__main__":
    main()
