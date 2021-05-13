# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import CMD_HELP, TIMEOUT, BOT_USERNAME, CMD_LIST, bot, LOGS
from userbot.events import register
from asyncio import sleep

@register(outgoing=True, pattern=r"^\.help(?: |$)(.*)")
async def help(event):
   
    args = event.pattern_match.group(1).lower()
    # Prevent Channel Bug to get any information and command from all modules
    if event.is_channel and not event.is_group:
        await event.edit("`Help command isn't permitted on channels`")
        return
    if args:
        if args in CMD_HELP:
            msg=await event.edit(str(CMD_HELP[args]))
            await sleep(45)
         
        else:
            msg=await event.edit("Please specify a valid module name.")
            await sleep(15)   
        else:
            tgbotusername = BOT_USERNAME
            help_string = "Userbot Helper for TEST to reveal all the commands of TEST"
            try:
                results = await bot.inline_query(  # pylint:disable=E0602
                 #   tgbotusername, help_string
                 "@senpaitorrentleechbot", help_string  
                )
                await results[0].click(
                    event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
                )
               # await event.answer([results])
                await event.delete()
            except Exception as e:
               LOGS.info(str(e))
         #   except BaseException:
          #      await event.edit(
           #         f"This bot has inline disabled. TESTFAILED"
            #    )
