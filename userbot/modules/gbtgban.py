

from sqlalchemy.exc import IntegrityError

from userbot import CMD_HELP, bot
from userbot.events import register


gbtban_replies = [
    "Banned",
    "On it",
    "already been",
    "GBan Reason update",
    "GBan reason updated",
    "has already been gbanned, with the exact same reason.",
]

ungbtban_replies = ["New un-gBan", "I'll give", "Un-gBan" "UnGBan" "Fine"]

@register(outgoing=True, disable_edited=True, pattern=r"^\.(d)?gbtban(?: |$)(.*)")
async def gbtban(event):
    """Bans a user from connected gbterations."""
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
        return await event.edit("**You haven't connected to any gbterations yet!**")

    user_link = f"[{gbtban_id}](tg://user?id={gbtban_id})"

    await event.edit(f"**gbtbanning** {user_link}...")
    failed = []
    total = 0

    for i in gbt_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"/gban {user_link} {reason}")
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
        status = f"Failed to gbtban in {len(failed)}/{total} gbts.\n"
        for i in failed:
            status += f"• {i}\n"
    else:
        status = f"Success! gbtbanned in {total} gbts."

    await event.edit(
        f"**gbtbanned **{user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, disable_edited=True, pattern=r"^\.ungbtban(?: |$)(.*)")
async def ungbtban(event):
    """Unbans a user from connected gbterations."""
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
        return await event.edit("**You haven't connected to any gbterations yet!**")

    user_link = f"[{ungbtban_id}](tg://user?id={ungbtban_id})"

    await event.edit(f"**Un-gbtbanning **{user_link}**...**")
    failed = []
    total = 0

    for i in gbt_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"/ungban {user_link}")
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
        status = f"Failed to un-gbtban in {len(failed)}/{total} gbts.\n"
        for i in failed:
            status += f"• {i}\n"
    else:
        status = f"Success! Un-gbtbanned in {total} gbts."

    reason = reason if reason else "Not specified."
    await event.edit(
        f"**Un-gbtbanned** {user_link}!\n**Reason:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, pattern=r"^\.addgb(?: |$)(.*)")
async def addf(event):
    """Adds current chat to connected gbterations."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import add_gbtlist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    gbt_name = event.pattern_match.group(1)
    if not gbt_name:
        return await event.edit("**Pass a name in order connect to this group!**")

    try:
        add_gbtlist(event.chat_id, gbt_name)
    except IntegrityError:
        return await event.edit(
            "**This group is already connected to gbterations list.**"
        )

    await event.edit("**Added this group to gbterations list!**")


@register(outgoing=True, pattern=r"^\.delgb$")
async def delf(event):
    """Removes current chat from connected gbterations."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import del_gbtlist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_gbtlist(event.chat_id)
    await event.edit("**Removed this group from gbterations list!**")


@register(outgoing=True, pattern=r"^\.listgb$")
async def listf(event):
    """List all connected gbterations."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import get_gbtlist
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    gbt_list = get_gbtlist()
    if len(gbt_list) == 0:
        return await event.edit("**You haven't connected to any gbterations yet!**")

    msg = "**Connected gbterations:**\n\n"

    for i in gbt_list:
        msg += f"• {i.gbt_name}\n"

    await event.edit(msg)


@register(outgoing=True, disable_edited=True, pattern=r"^\.cleargb$")
async def clearf(event):
    """Removes all chats from connected gbterations."""
    try:
        from userbot.modules.sql_helper.gbtban_sql import del_gbtlist_all
    except IntegrityError:
        return await event.edit("**Running on Non-SQL mode!**")

    del_gbtlist_all()
    await event.edit("**Disconnected from all connected gbterations!**")


CMD_HELP.update(
    {
        "gbtban": ">`.gbtban <id/username> <reason>`"
        "\nUsage: Bans user from connected gbterations."
        "\nYou can reply to the user whom you want to gbtban or manually pass the username/id."
        "\n`.dgbtban` does the same but deletes the replied message."
        "\n\n`>.ungbtban <id/username> <reason>`"
        "\nUsage: Same as gbtban but unbans the user"
        "\n\n>`.addgb <name>`"
        "\nUsage: Adds current group and stores it as <name> in connected gbterations."
        "\nAdding one group is enough for one gbteration."
        "\n\n>`.delgb`"
        "\nUsage: Removes current group from connected gbterations."
        "\n\n>`.listgb`"
        "\nUsage: Lists all connected gbterations by specified name."
        "\n\n>`.cleargb`"
        "\nUsage: Disconnects from all connected gbterations. Use it carefully."
    }
)
