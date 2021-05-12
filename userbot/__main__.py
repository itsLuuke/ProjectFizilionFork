# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot start point """
import re
from importlib import import_module
from sys import argv
from telethon import TelegramClient, events, Button
import telethon.utils
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from userbot import LOGS, bot, BOT_TOKEN, BOT_USERNAME, API_KEY, API_HASH
from userbot.modules import ALL_MODULES


INVALID_PH = '\nERROR: The Phone No. entered is INVALID' \
             '\n Tip: Use Country Code along with number.' \
             '\n or check your phone number and try again !'


try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("You are running Project Fizilion")

LOGS.info(
    "Congratulations, your userbot is now running !! Test it by typing .alive / .on in any chat."
    "If you need assistance, head to https://t.me/ProjectFizilionChat")
OWNER_ID = 1391975600
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


if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
