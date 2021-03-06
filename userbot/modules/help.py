# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import CMD_HELP, TIMEOUT, trgg, CUST_CMD_HELP
from userbot.events import register
from asyncio import sleep
@register(outgoing=True, pattern="^\{trg}help(?: |$)(.*)".format(trg=trgg))
async def help(event):
    """ For .help command,"""
    args = event.pattern_match.group(1).lower()
    # Prevent Channel Bug to get any information and command from all modules
    if event.is_channel and not event.is_group:
        await event.edit("`Help command isn't permitted on channels`")
        return
    if args:
        if args in CMD_HELP:
            msg=await event.edit(str(CMD_HELP[args]))
            await sleep(45)
        elif args in CUST_CMD_HELP:
            msg=await event.edit(str(CUST_CMD_HELP[args]))
            await sleep(45)
        else:
            msg=await event.edit("Please specify a valid module name.")
            await sleep(15)   
    else:
        final = "**List of all loaded module(s)**\n\
        \nSpecify which module do you want help for! \
        \n**Usage:** `.help` <module name>\n\n"
        temp = "".join(str(i) + " " for i in CMD_HELP)
        temp = sorted(temp.split())
        for i in temp:
            final += "`" + str(i)
            final += "`\t\t\t•\t\t\t"

        if len(CUST_CMD_HELP) > 0:
            final += "\n\n**List of all custom loaded module(s)**\n"
            temp2 = "".join(str(i) + " " for i in CUST_CMD_HELP)
            temp2 = sorted(temp2.split())
            for i in temp2:
                final += "`" + str(i)
                final += "`\t\t\t•\t\t\t"

        msg=await event.edit(f"{final[:-5]}")
        await sleep(45)
        
    if TIMEOUT:
        await msg.delete()
                
