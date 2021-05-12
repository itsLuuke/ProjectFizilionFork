import re
from telethon import events, Button
import asyncio
import os
import requests
from datetime import datetime
from telethon import events
from userbot import inlinebot
# start-others


@inlinebot.on(events.NewMessage(pattern="^/start"))  # pylint: disable=oof
async def start_all(event):
    if event.chat_id == OWNER_ID:
        return
    await inlinebot.send_message(event.chat_id, "TEST=NOTOWNER")
      

# start-owner


@inlinebot.on(events.NewMessage(pattern="^/start",
                            from_users=OWNER_ID))  # pylint: disable=oof
async def owner(event):
    await inlinebot.send_message(event.chat_id, "TEST=OWNER")


