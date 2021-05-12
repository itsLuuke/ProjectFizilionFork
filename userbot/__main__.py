# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot start point """

from importlib import import_module
from sys import argv
from telethon import TelegramClient
import telethon.utils
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from userbot import LOGS, bot, BOT_TOKEN, BOT_USERNAME, API_KEY, API_HASH
from userbot.modules import ALL_MODULES


INVALID_PH = '\nERROR: The Phone No. entered is INVALID' \
             '\n Tip: Use Country Code along with number.' \
             '\n or check your phone number and try again !'
async def add_bot(bot_token):
    await bot.start(bot_token)
    bot.me = await bot.get_me()
    bot.uid = telethon.utils.get_peer_id(bot.me)



bot.tgbot = None
if BOT_USERNAME is not None:
        LOGS.info("Initiating Inline Bot")
        inlinebot = TelegramClient(
            "BOT_TOKEN",
            api_id=API_KEY,
            api_hash=API_HASH
        ).start(bot_token=BOT_TOKEN)
        LOGS.info("SETTING BOT, no errors")
        LOGS.info("Starting Userbot")
        bot.loop.run_until_complete(add_bot(BOT_USERNAME))
        LOGS.info("Startup Completed")
else:
    LOGS.info("Inline Failed, Starting anyways")
    bot.start()

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

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
