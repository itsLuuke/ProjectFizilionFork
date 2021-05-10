# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import CMD_HELP, TIMEOUT, BOT_USERNAME, CMD_LIST
from userbot.events import register
from asyncio import sleep

@register(outgoing=True, pattern=r"^\.help(?: |$)(.*)")
async def help(event):
   
#   if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
 #       tgbotusername = BOT_USERNAME
  #      input_str = event.pattern_match.group(1)
   #     if tgbotusername is None or input_str == "text":
    #        string = ""
     ##       for i in CMD_HELP:
      #          string += "EMOJITEST" + " " + i + " " + "EMOPJITEST2" + "\n"
      ##          for iter_list in CMD_HELP[i]:
       #             string += "    `" + str(iter_list) + "`"
       #             string += "\n"
       #         string += "\n"
       #     if len(string) > 4095:
       #         with io.BytesIO(str.encode(string)) as out_file:
       #             out_file.name = "cmd.txt"
       #             await tgbot.send_file(
       ##                 event.chat_id,
        #                out_file,
        #                force_document=True,
       #                 allow_cache=False,
       #                 caption="**COMMANDS**",
       #                 reply_to=reply_to_id,
       #             )
       #             await event.delete()
       #     else:
       #         await event.edit(string)
       # elif input_str:
       #     if input_str in CMD_LIST:
       #         string = "**Commands available in {}** \n\n".format(input_str)
       #         if input_str in CMD_HELP:
       #             for i in CMD_HELP[input_str]:
       #                 string += i
       #             string += "\n\n**TEST1**"
       #             await event.edit(string)
       #         else:
       #             for i in CMD_LIST[input_str]:
       #                 string += "    " + i
       #                 string += "\n"
       #             string += "\n**TEST2**"
       #             await event.edit(string)
       #     else:
       #         await event.edit(input_str + " is not a valid plugin!")
       # else:
            tgbotusername = BOT_USERNAME
            help_string = f"""`Userbot Helper for TEST to reveal all the commands of `**TEST**\n\n"""
            try:
                results = await bot.inline_query(  # pylint:disable=E0602
                    tgbotusername, help_string
                )
                await results[0].click(
                    event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
                )
                await event.delete()
            except BaseException:
                await event.edit(
                    f"This bot has inline disabled. TESTFAILED"
                )
