# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port From UniBorg to UserBot by keselekpermen69

import io
import re

from sqlalchemy.exc import IntegrityError
import userbot.modules.sql_helper.blacklist_sql as sql
from userbot import CMD_HELP
from userbot.events import register


@register(incoming=True, disable_edited=True, disable_errors=True)
async def on_new_message(event):
    # TODO: exempt admins from locks
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await event.reply("I do not have DELETE permission in this chat")
                sql.rm_from_blacklist(event.chat_id, snip.lower())
            break


@register(outgoing=True, pattern="^.addbl(?: |$)(.*)")
async def on_add_black_list(addbl):
    text = addbl.pattern_match.group(1)
    to_blacklist = list(
        set(trigger.strip() for trigger in text.split("\n") if trigger.strip())
    )
    for trigger in to_blacklist:
        sql.add_to_blacklist(addbl.chat_id, trigger.lower())
    await addbl.edit(
        "Added {} triggers to the blacklist in the current chat".format(
            len(to_blacklist)
        )
    )


@register(outgoing=True, pattern="^.listbl(?: |$)(.*)")
async def on_view_blacklist(listbl):
    all_blacklisted = sql.get_chat_blacklist(listbl.chat_id)
    OUT_STR = "Blacklists in the Current Chat:\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"`{trigger}`\n"
    else:
        OUT_STR = "No BlackLists. Start Saving using `.addbl`"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await listbl.client.send_file(
                listbl.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="BlackLists in the Current Chat",
                reply_to=listbl,
            )
            await listbl.delete()
    else:
        await listbl.edit(OUT_STR)


@register(outgoing=True, pattern="^.rmbl(?: |$)(.*)")
async def on_delete_blacklist(rmbl):
    text = rmbl.pattern_match.group(1)
    to_unblacklist = list(
        set(trigger.strip() for trigger in text.split("\n") if trigger.strip())
    )
    successful = 0
    for trigger in to_unblacklist:
        if sql.rm_from_blacklist(rmbl.chat_id, trigger.lower()):
            successful += 1
    await rmbl.edit(f"Removed {successful} / {len(to_unblacklist)} from the blacklist")
@register(outgoing=True, pattern=r"^\.blacklist (.*)")
async def blacklist(event):
    """Adds given chat to blacklist."""
    try:
        from userbot.modules.sql_helper.blacklist_sql import add_blacklist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    try:
        chat_id = int(event.pattern_match.group(1))
    except ValueError:
        chat_id = event.pattern_match.group(1)

    try:
        chat_id = await event.client.get_peer_id(chat_id)
    except Exception:
        return await event.edit("**Error: Invalid username/ID provided.**")

    try:
        add_blacklist(str(chat_id))
    except IntegrityError:
        return await event.edit("**Given chat is already blacklisted.**")

    await event.edit("**Blacklisted given chat!**")


@register(outgoing=True, pattern=r"^\.unblacklist (.*)")
async def unblacklist(event):
    """Unblacklists given chat."""
    try:
        from userbot.modules.sql_helper.blacklist_sql import (
            del_blacklist,
            get_blacklist,
        )
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    chat_id = event.pattern_match.group(1)
    try:
        chat_id = str(await event.client.get_peer_id(chat_id))
    except Exception:
        pass  # this way, deleted chats can be unblacklisted

    if chat_id == "all":
        from userbot.modules.sql_helper.blacklist_sql import del_blacklist_all

        del_blacklist_all()
        return await event.edit("**Cleared all blacklists!**")

    id_exists = False
    for i in get_blacklist():
        if chat_id == i.chat_id:
            id_exists = True

    if not id_exists:
        return await event.edit("**This chat isn't blacklisted.**")

    del_blacklist(chat_id)
    await event.edit("**Un-blacklisted given chat!**")


@register(outgoing=True, pattern=r"^\.blacklists$")
async def list_blacklist(event):
    """Lists all blacklisted chats."""
    try:
        from userbot.modules.sql_helper.blacklist_sql import get_blacklist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    chat_list = get_blacklist()
    if not chat_list:
        return await event.edit("**You haven't blacklisted any chats yet!**")

    msg = "**Blacklisted chats:**\n\n"

    for i in chat_list:
        try:
            chat = await event.client.get_entity(int(i.chat_id))
            chat = f"{chat.title} | `{i.chat_id}`"
        except (TypeError, ValueError):
            chat = f"__Couldn't fetch chat info__ | `{i.chat_id}`"

        msg += f"• {chat}\n"

    await event.edit(msg)


CMD_HELP.update(
    {
        "blacklist": ".listbl\
    \nUsage: Lists all active userbot blacklist in a chat.\
    \n\n.addbl <keyword>\
    \nUsage: Saves the message to the 'blacklist keyword'.\
    \nThe bot will delete to the message whenever 'blacklist keyword' is mentioned.\
    \n\n.rmbl <keyword>\
    \nUsage: Stops the specified blacklist.\
	\n btw you need permissions **Delete Messages** of admin."
    }
)
