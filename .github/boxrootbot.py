import asyncio
import os
import sys
from telethon import TelegramClient

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID_RAW = os.environ.get("CHAT_ID")
MESSAGE_THREAD_ID_RAW = os.environ.get("MESSAGE_THREAD_ID")
VERSION = os.environ.get("VERSION")
COMMIT = os.environ.get("COMMIT")

MSG_TEMPLATE = """
{version}

{commit}

[Github](https://github.com/ljrgov/box_for_root)
[Releases](https://github.com/ljrgov/box_for_root/releases)

#module #ksu #apatch #magisk #root #debug
""".strip()


def check_environ():
    required = {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "BOT_TOKEN": BOT_TOKEN,
        "CHAT_ID": CHAT_ID_RAW,
        "MESSAGE_THREAD_ID": MESSAGE_THREAD_ID_RAW,
        "VERSION": VERSION,
        "COMMIT": COMMIT,
    }
    for k, v in required.items():
        if not v:
            print(f"[-] Invalid or missing: {k}")
            exit(1)


def get_caption():
    msg = MSG_TEMPLATE.format(version=VERSION, commit=COMMIT)
    if len(msg) > 1024:
        return COMMIT
    return msg


async def main():
    print("[+] Uploading to telegram")
    check_environ()

    chat_id = int(CHAT_ID_RAW)
    thread_id = int(MESSAGE_THREAD_ID_RAW)

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
            entity=chat_id,
            file=files,
            caption=caption,
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