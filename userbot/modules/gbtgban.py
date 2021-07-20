

from sqlalchemy.exc import IntegrityError

from userbot import CMD_HELP, bot, trgg
from userbot.events import register


gbtban_replies = [
    "Banned",
    "On it",
    "Done!",
    "already been",
    "GBan Reason update",
    "GBan reason updated",
    "user is already",
    "has been gbanned",
    "This user is already",
    "has already been gbanned, with the exact same reason.",
]

ungbtban_replies = ["New un-gBan", "I'll give", "Un-gBan" "UnGBan" "Fine"]

@register(outgoing=True, disable_edited=True, pattern=r"^{trg}(d)?gbtban(?: |$)(.*)".format(trg=trgg))
async def gbtban(event):
    """Bans a user from connected group bots."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import get_gbtlist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    match = event.pattern_match.group(2)

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        gbtban_id = reply_msg.sender_id

        if event.pattern_match.group(1) == "d":
            await reply_msg.delete()

        reason = match
    else:
        pattern = match.split()
        gbtban_id = pattern[0]
        reason = " ".join(pattern[1:])

    try:
        gbtban_id = await event.client.get_peer_id(gbtban_id)
    except Exception:
        pass

    if event.sender_id == gbtban_id:
        return await event.edit(
            "**Error: This action has been prevented by Forkzilion-dev-bot self preservation protocols.**"
        )

    gbt_list = get_gbtlist()
    if len(gbt_list) == 0:
        return await event.edit("**You haven't connected to any group bots yet!**")

    user_link = f"[{gbtban_id}](tg://user?id={gbtban_id})"

    await event.edit(f"**Globally banning** {user_link}...")
    failed = []
    total = 0

    for i in gbt_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"!gban {user_link} {reason}")
                reply = await conv.get_response()
                await bot.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )

                if not any(i in reply.text for i in gbtban_replies):
                    failed.append(i.gbt_name)
        except Exception:
            failed.append(i.gbt_name)

    reason = reason if reason else "Not specified."

    if failed:
        status = f"Failed to Globally ban by {len(failed)}/{total} bots.\n"
        for i in failed:
            status += f"• {i}\n"
    else:
        status = f"Success! Globally banned by {total} bots."

    await event.edit(
        f"**Globally banned **{user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, disable_edited=True, pattern=r"^{trg}ungbtban(?: |$)(.*)".format(trg=trgg))
async def ungbtban(event):
    """Unbans a user from connected connected bots."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import get_gbtlist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    match = event.pattern_match.group(1)
    if event.is_reply:
        ungbtban_id = (await event.get_reply_message()).sender_id
        reason = match
    else:
        pattern = match.split()
        ungbtban_id = pattern[0]
        reason = " ".join(pattern[1:])

    try:
        ungbtban_id = await event.client.get_peer_id(ungbtban_id)
    except:
        pass

    if event.sender_id == ungbtban_id:
        return await event.edit("**Wait, that's illegal**")

    gbt_list = get_gbtlist()
    if len(gbt_list) == 0:
        return await event.edit("**You haven't connected to any group bots yet!**")

    user_link = f"[{ungbtban_id}](tg://user?id={ungbtban_id})"

    await event.edit(f"**Globally unbanning **{user_link}**...**")
    failed = []
    total = 0

    for i in gbt_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"!ungban {user_link}")
                reply = await conv.get_response()
                await bot.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )

                if not any(i in reply.text for i in ungbtban_replies):
                    failed.append(i.gbt_name)
        except Exception:
            failed.append(i.gbt_name)

    reason = reason if reason else "Not specified."

    if failed:
        status = f"Failed to un-ban in {len(failed)}/{total} gbts.\n"
        for i in failed:
            status += f"• {i}\n"
    else:
        status = f"Success! Globally unbanned in {total} gbts."

    reason = reason if reason else "Not specified."
    await event.edit(
        f"**Globally Un-banned** {user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, pattern=r"^{trg}addgb(?: |$)(.*)".format(trg=trgg))
async def addf(event):
    """Adds current chat to connected global bots."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import add_gbtlist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    gbt_name = event.pattern_match.group(1)
    if not gbt_name:
        return await event.edit("**Pass a name in order connect to this chat!**")

    try:
        add_gbtlist(event.chat_id, gbt_name)
    except IntegrityError:
        return await event.edit(
            "**This chat is already connected to group bots list.**"
        )

    await event.edit("**Added this chat to group bots list!**")


@register(outgoing=True, pattern=r"^{trg}delgb$".format(trg=trgg))
async def delf(event):
    """Removes current chat from connected gbterations."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import del_gbtlist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_gbtlist(event.chat_id)
    await event.edit("**Removed this group from gbterations list!**")


@register(outgoing=True, pattern=r"^{trg}listgb$".format(trg=trgg))
async def listf(event):
    """List all connected group bots."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import get_gbtlist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    gbt_list = get_gbtlist()
    if len(gbt_list) == 0:
        return await event.edit("**You haven't connected to any group bots yet!**")

    msg = "**Connected group bots:**\n\n"

    for i in gbt_list:
        msg += f"• {i.gbt_name}\n"

    await event.edit(msg)


@register(outgoing=True, disable_edited=True, pattern=r"^{trg}cleargb$".format(trg=trgg))
async def clearf(event):
    """Removes all chats from connected group bots."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import del_gbtlist_all
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_gbtlist_all()
    await event.edit("**Disconnected from all connected group bots!**")


CMD_HELP.update(
    {
        "gbtban": ">`.gbtban <id/username> <reason>`"
        "\nUsage: Bans user from connected group bots."
        "\nYou can reply to the user whom you want to globally ban or manually pass the username/id."
        "\n`.dgbtban` does the same but deletes the replied message."
        "\n\n`>.ungbtban <id/username> <reason>`"
        "\nUsage: Same as gbtban but unbans the user"
        "\n\n>`.addgb <name>`"
        "\nUsage: Adds current chat and stores it as <name> in connected group bots to gban."
        "\nAdding one group is enough for one ban."
        "\n\n>`.delgb`"
        "\nUsage: Removes current group from connected group bots chats."
        "\n\n>`.listgb`"
        "\nUsage: Lists all connected group bots chats by specified name."
        "\n\n>`.cleargb`"
        "\nUsage: Disconnects from all connected group bots to gban. Use it carefully."
    }
)
