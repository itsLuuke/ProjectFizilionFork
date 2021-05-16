import platform
import shutil
import sys
import pip
import distro
import time
import os
import re
import time
from importlib import import_module
from sys import argv
from telethon import TelegramClient, events, Button
import telethon.utils
from telethon.tl.functions.users import GetFullUserRequest
from userbot import LOGS, bot, BOT_TOKEN, BOT_USERNAME, API_KEY, API_HASH
from platform import python_version, uname
from shutil import which
import psutil
from git import Repo
from telethon import __version__, version

async def add_bot(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()

try:
    LOGS.info("Initiating InlineBot....")
    inlinebot = TelegramClient("inlinebot", API_KEY, API_HASH).start(bot_token=BOT_TOKEN)
    bot.loop.run_until_complete(add_bot(BOT_USERNAME))
    LOGS.info("InlineBot is online now")
except Exception as e:
    LOGS.info("InlineBot Failed .")
    LOGS.info("InlineBot is quiting...")
    LOGS.info(str(e))
    
