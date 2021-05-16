## 
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
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from userbot import LOGS, bot, BOT_TOKEN, BOT_USERNAME, API_KEY, API_HASH, ALIVE_LOGO, USERBOT_VERSION, StartTime, ALIVE_NAME, CMD_HELP, OWNER_ID
from userbot.modules import ALL_MODULES
from platform import python_version, uname
from shutil import which
import psutil
from git import Repo
from telethon import __version__, version

from userbot.utils import inlinebot


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
modules = CMD_HELP
repo = Repo()
alive_text = (
        
        f"`===============================`\n"
        f"**FIZILION IS UP AND RUNNING...**\n"
        f"`=============================== `\n"
        f"**[OS Info]:**\n"
        f"•`Platform Type   : {os.name}`\n"
        f"•`Distro          : {distro.name(pretty=False)} {distro.version(pretty=False, best=False)}`\n"
        f"`===============================`\n"
        f"**[PYPI Module Versions]:**\n"
        f"•`Python         : v{python_version()} `\n"   
        f"•`Telethon       : v{version.__version__} `\n"
        f"•`PIP            : v{pip.__version__} `\n"
        f"`===============================`\n"
        f"**[MISC Info]:**\n"
        f"•`User           : TEST `\n"
        f"•`Running on     : {repo.active_branch.name} `\n"
        f"•`Loaded modules : {len(modules)} `\n"
        f"•`Fizilion       : {USERBOT_VERSION} `\n"
        f"•`Bot Uptime     : TEST `\n"
        f"`===============================`\n"

    )


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time
    
@inlinebot.on(events.NewMessage(pattern="/start"))  # pylint: disable=oof
async def start_all(e):
        userid = e.chat_id
        if userid == OWNER_ID:
                await inlinebot.send_message(e.chat_id, ".")
                await start(e)
        
        else:
                await inlinebot.send_message(e.chat_id, "**You are not authorised to use me.**")
                await unauthorised(e)
        
                
async def start(e):
    userid = await e.client(GetFullUserRequest(e.sender_id))
    await e.reply(alive_text,
                  buttons=[
                          [Button.url("REPO", url="https://github.com/PrajjuS/ProjectFizilion"), Button.url("MASTER", url=f"t.me/{userid.user.username}"),],
                          [Button.url("ADD ME TO GROUP", url=f"http://t.me/{BOT_USERNAME}?startgroup=start")],
                          [Button.inline("SET PM PERMIT", data="pmpermit")],
                          ]
                  )


async def unauthorised(e):
    await e.reply("**Deploy your own Bot here.**",
                  buttons=[
                          [Button.url("REPO", url="https://github.com/PrajjuS/ProjectFizilion")],
                  ]
                 )   
    
@inlinebot.on(events.InlineQuery)
async def handler(event):
    userid = await event.client(GetFullUserRequest(event.query.user_id))
    builder = event.builder   
    if event.query.user_id == OWNER_ID:
          query = event.text
          uptime = await get_readable_time((time.time() - StartTime))  
          alive = builder.document(
                  title="Alive",
                  file=ALIVE_LOGO,
                  include_media=True,
                  text=alive_text,
                  buttons=[
                          [
                                  Button.url("REPO", url="https://github.com/PrajjuS/ProjectFizilion"),
                                  Button.url("MASTER", url=f"t.me/{userid.user.username}"),
                                  ],
                          [Button.url("ADD ME TO GROUP", url=f"http://t.me/{BOT_USERNAME}?startgroup=start")],
                          [Button.inline("HELP", data="help")],
                          ],
                  )
          await event.answer([alive])
    else:
          notmaster = builder.article(
                  title="Repo",
                  description="Setup your own Fizlion Userbot",
                  text="**Click here to open Fizilion Bot's Github Repo**",
                  link_preview=True,
                  buttons=[Button.url("REPO", url="https://github.com/PrajjuS/ProjectFizilion")],
          )
          await event.answer([notmaster])    
        
@inlinebot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmpermit"))      
async def pmpermit(e):              
