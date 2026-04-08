import asyncio
import os
import sys
from telethon import TelegramClient

# 从环境变量获取，设置默认值为空字符串
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID_RAW = os.environ.get("CHAT_ID")
MESSAGE_THREAD_ID_RAW = os.environ.get("MESSAGE_THREAD_ID")
VERSION = os.environ.get("VERSION", "Unknown")
COMMIT = os.environ.get("COMMIT", "n/a")
DATE = os.environ.get("DATE", "")
CHANGELOG = os.environ.get("CHANGELOG", "No changelog provided.")

MSG_TEMPLATE = """
📦 **box for root模块**

**版本:** {version} ({commit})
**日期:** {date}
**内容:** {changelog}

[仓库地址](https://github.com/ljrgov/box_for_root) | [Release 详情](https://github.com/ljrgov/box_for_root/releases)

#module #ksu #apatch #magisk #root
""".strip()

def check_environ():
    # 核心的 TG 连接参数为必填
    required = {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "BOT_TOKEN": BOT_TOKEN,
        "CHAT_ID": CHAT_ID_RAW,
    }
    for k, v in required.items():
        if not v:
            print(f"[-] Critical missing: {k}")
            exit(1)

def get_caption():
    # 这里的变量名要和 MSG_TEMPLATE 里的 {xxx} 对应
    # 使用 .get() 并在没有值时提供默认字符串，防止 KeyError
    data = {
        "version": os.environ.get("VERSION", "Unknown"),
        "commit": os.environ.get("COMMIT", "N/A"),
        "date": os.environ.get("DATE", "N/A"),
        "changelog": os.environ.get("CHANGELOG", "无更新日志")
    }
    
    try:
        msg = MSG_TEMPLATE.format_map(data)
    except Exception as e:
        msg = f"📦 Box for Root 更新\n版本: {data['version']}\n提交: {data['commit']}"
    # 限制长度在 1024 字符内 (TG Caption 硬性限制)
    return msg[:1024]

async def main():
    print("[+] Uploading to telegram")
    check_environ()

    chat_id = int(CHAT_ID_RAW)
    thread_id = int(MESSAGE_THREAD_ID_RAW) if MESSAGE_THREAD_ID_RAW else None

    files = sys.argv[1:]
    print("[+] Files:", files)
    if len(files) == 0:
        print("[-] No files to upload")
        exit(1)

    print("[+] Logging in Telegram with bot")
    async with await TelegramClient(
        session="/tmp/bot.session",
        api_id=API_ID,
        api_hash=API_HASH
    ).start(bot_token=BOT_TOKEN) as bot:
        caption = [""] * len(files)
        caption[-1] = get_caption()
        print("[+] Caption:")
        print("---")
        print(caption[-1])
        print("---")
        print("[+] Sending")
        await bot.send_file(
            entity=int(CHAT_ID_RAW),
            file=files,
            caption=get_caption(),
            reply_to=thread_id,
            parse_mode="markdown"
        )
        print("[+] Done!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        exit(1)