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
from userbot import LOGS, bot, BOT_TOKEN, BOT_USERNAME, API_KEY, API_HASH, ALIVE_LOGO, USERBOT_VERSION, StartTime, ALIVE_NAME, CMD_HELP
from userbot.modules import ALL_MODULES
from platform import python_version, uname
from shutil import which
import psutil
from git import Repo
from telethon import __version__, version

OWNER_ID = 1391975600

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


async def add_bot(bot_token):
    await bot.start(bot_token)
    bot.me = await bot.get_me()
    bot.uid = telethon.utils.get_peer_id(bot.me)

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

try:
    LOGS.info("INITIATING INLINEBOT....")
    inlinebot = TelegramClient("inlinebot", API_KEY, API_HASH).start(bot_token=BOT_TOKEN)
    bot.loop.run_until_complete(add_bot(BOT_USERNAME))
    LOGS.info("INLINEBOT IS ONLINE NOW")
except Exception as e:
    LOGS.info("INLINEBOT FAILED.")
    LOGS.info("INLINEBOT is quiting...")
    LOGS.info(str(e))
    
    
@inlinebot.on(events.NewMessage(pattern="/start"))  # pylint: disable=oof
async def start_all(e):
    if e.chat_id == OWNER_ID:
        return
    await inlinebot.send_message(e.chat_id, "You are not my boss but proceed anyway")  
    await start(e)

# start-owner


@inlinebot.on(events.NewMessage(pattern="/start", from_users=OWNER_ID))
async def boss(e):   
    await inlinebot.send_message(e.chat_id, "YES BOSS")
    await start(e)
## TO FORWARD MESSAGES TO OWNER    
#@inlinebot.on(events.NewMessage(incoming=True))
#async def incoming_messages(e):
#  await inlinebot.
  
async def start(e):
    yourname = await e.client(GetFullUserRequest(e.sender_id))
    await e.reply(
        f"THIS IS YOUR NAME {yourname.user.first_name} NOW TEST",
        buttons=[
            [Button.inline("TESTBUTTON", data="test")],
            [
            
                Button.url("MASTER", url="t.me/senpaiaf"),
            ],
        ],
    )
async def back(e):
    yourname = await e.client(GetFullUserRequest(e.sender_id))
    await e.edit(
        f"THIS IS YOUR NAME {yourname.user.first_name} NOW TEST",
        buttons=[
            [Button.inline("TESTBUTTON", data="test")],
            [
            
                Button.url("MASTER", url="t.me/senpaiaf"),
            ],
        ],
    )
async def test(e):
    await e.edit(
        "SUCCESSFULLY TESTED",
        buttons=[Button.inline("TEST TO GO BACK", data="back")],
    )    
  
## CALLBACKS
@inlinebot.on(events.callbackquery.CallbackQuery(data=re.compile(b"test(.*)")))
async def _(e):
    await test(e)
    
@inlinebot.on(events.callbackquery.CallbackQuery(data=re.compile(b"back(.*)")))
async def _(e):
    await back(e)    
    
@inlinebot.on(events.InlineQuery)
async def handler(event):
#    builder = event.builder

    # Two options (convert user text to UPPERCASE or lowercase)
   # await event.answer([
   #     builder.article('UPPERCASE', text=event.text.upper()),
   #     builder.article('lowercase', text=event.text.lower()),
   # ])
    builder = event.builder
    query = event.text
    if event.query.user_id == bot.uid:
      uptime = await get_readable_time((time.time() - StartTime))  
      alive = builder.photo(
                file=ALIVE_LOGO,
                text=alive_text,
                buttons=[
                    [
                        Button.inline("BUTTON1", data="one"),
                        Button.inline("BUTTON2", data="two"),
                    ],
                    [Button.inline("BUTTTON3", data="three")],
                    [Button.inline("BUTTON4", data="four")],
                ],
            )
      r1 = builder.article('1. TEST', text="TEST HELP")
      r2 = builder.article('2. TEST', text="TEST HELP2")
      await event.answer([alive, r1, r2])
    else:
      notmaster = builder.article('Not for you boss', text='You are not my master you bastard')
      await event.answer([notmaster])    
