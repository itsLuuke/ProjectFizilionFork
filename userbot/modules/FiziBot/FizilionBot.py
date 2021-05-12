import re
import asyncio
import os
import requests
from telethon import events, TelegramClient
from userbot import BOT_TOKEN, API_KEY, API_HASH, LOGS
# start-others
try:
    LOGS.info("INITIATING BOT....")
    inlinebot = TelegramClient("inlinebot", API_KEY, API_HASH).start(bot_token=BOT_TOKEN)
except Exception as e:
    LOGS.info("INLINEBOT FAILED.")
    LOGS.info("INLINEBOT is quiting...")
    LOGS.info(str(e))
    exit()

@inlinebot.on(events.NewMessage(pattern="/start"))  # pylint: disable=oof
async def start_all(event):
    if event.chat_id == OWNER_ID:
        return
    await inlinebot.send_message(event.chat_id, "TEST=NOTOWNER")
      

# start-owner


@inlinebot.on(events.NewMessage(pattern="/start",
                            from_users=OWNER_ID))  # pylint: disable=oof
async def owner(event):
    await inlinebot.send_message(event.chat_id, "TEST=OWNER")


