# pm and tagged messages logger for catuserbot by @mrconfused (@sandy1709)
# imported from catuserbot 
# modified by @AbOuLfOoOoOuF for fizilion

import asyncio, re

from userbot import bot, PMLOG, PMLOG_CHATID, CMD_HELP, LOGS, ISAFK, BOTLOG, BOTLOG_CHATID, trgg, tgbott, bot

from userbot.modules.sql_helper import pm_permit_sql
from userbot.modules.sql_helper.globals import gvarstatus, addgvar
from userbot.events import register
from telethon import events
from telethon.utils import get_display_name
from userbot.utils.tools import media_type
from telethon.tl.types import User
class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


def do_log():
    return bool(gvarstatus("PMLOG") \
        and gvarstatus("PMLOG") == "true"\
            and PMLOG_CHATID not in [-100, 0])

LOG_CHATS_ = LOG_CHATS()

def mentionchannel(name, uname):
    return f"[{name}](https://t.me/{uname})"

def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"

def htmlmentionuser(name, userid):
    return f"<a href='tg://user?id={userid}'>{name}</a>"

def htmlmentionchannel(name, uname):
    return f"<a href='https://t.me/{uname}'>{name}</a>"

@register(incoming=True, func=lambda e: e.is_private, disable_edited=False)
async def monito_p_m_s(event):  # sourcery no-metrics
    if not do_log():
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        # if not pm_permit_sql.is_approved(chat.id) and chat.id != 777000:
        if chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    if LOG_CHATS_.COUNT > 1:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "new message", f"{LOG_CHATS_.COUNT} messages"
                            )
                        )
                    else:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "new message", f"{LOG_CHATS_.COUNT} message"
                            )
                        )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await tgbott.send_message(
                    PMLOG_CHATID,
                    f"👤{mentionuser(sender.first_name , sender.id)} has sent a new message \nId : `{chat.id}`",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        PMLOG_CHATID, event.message, silent=True
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))


@register(incoming=True, func=lambda e: e.mentioned, disable_edited=False)
async def log_tagged_messages(event):
    hmm = await event.get_chat()

    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "False":
        return
    try:
        sendr = await event.get_sender()
    except:
        return
    if (
        (pm_permit_sql.is_approved(hmm.id))
        or (PMLOG_CHATID == -100)
        or (ISAFK == True)
        or (isinstance(sendr, User) and sendr.bot)
    ):
        return
    full = None
    try:
        full = await event.client.get_entity(event.message.from_id)
    except Exception as e:
        LOGS.info(str(e))
    messaget = media_type(event)
    resalt = f"#TAGS \n<b>Group : </b><code>{hmm.title}</code>"
    if full is not None:
        if isinstance(full, User):
            resalt += f"\n<b>From : </b> 👤{htmlmentionuser(full.first_name, full.id)}"
        else:
            resalt += f"\n<b>From : </b> 📣{htmlmentionchannel(full.title, full.username)}" # cant be without username
    if messaget is not None:
        resalt += f"\n<b>Message type : </b><code>{messaget}</code>"
    else:
        try:
            meee = await bot.get_me()
            mytag = f"@{meee.username}"
            if event.message.message.find(mytag) == "-1":
                msgggg = event.message.message
            else:
                msgggg = event.message.message.replace(f"@{meee.username}",f"@ {meee.username}")
        except Exception as e:
            LOGS.warn(str(e))
        resalt += f"\n<b>Message : </b>\n{msgggg}"
    resalt += f"\n<b>Message link: </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> link</a>"
    if not event.is_private:
        await tgbott.send_message(
            PMLOG_CHATID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )


@register(
    outgoing=True, pattern="^\{trg}log$".format(trg=trgg),

)
async def set_no_log_p_m(setnologpmm):
    "To turn on logging of messages from that chat."
    if PMLOG_CHATID not in [-100, 0]:
        chat = await setnologpmm.get_chat()
        if pm_permit_sql.is_approved(chat.id):
            pm_permit_sql.dissprove(chat.id)
            await setnologpmm.edit(
                "`logging of messages from this group has been started`"
            )
            if BOTLOG:
                await setnologpmm.client.send_message(
                    BOTLOG_CHATID,
                    "#PMLOG\n" + f"Enabled logging for CHAT: {setnologpmm.chat.title}(`{setnologpmm.chat_id}`)",
                )


@register(
    outgoing=True, pattern="^\{trg}nolog$".format(trg=trgg),
)
async def set_no_log_p_m(setlogpmm):
    "To turn off logging of messages from that chat."
    if PMLOG_CHATID not in [-100, 0]:
        chat = await setlogpmm.get_chat()
        if not pm_permit_sql.is_approved(chat.id):
            pm_permit_sql.approve(chat.id)
            await setlogpmm.edit(
                "`Logging of messages from this chat has been stopped`"
            )
            if BOTLOG:
                await setlogpmm.client.send_message(
                    BOTLOG_CHATID,
                    "#PMLOG\n" + f"Disabled logging for CHAT: {setlogpmm.chat.title}(`{setlogpmm.chat_id}`)",
                )

@register(
    outgoing=True, pattern="^\{trg}pmlog (on|off)$".format(trg=trgg),
)
async def set_pmlog(event):
    "To turn on or turn off logging of Private messages"
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    PMLOG = bool(do_log())
    if PMLOG:
        if h_type:
            await event.edit("`Pm logging is already enabled`")
        else:
            addgvar("PMLOG", h_type)
            await event.edit("`Pm logging is disabled`")
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#PMLOG\n" + "Disabled pm logging.",
                )
    elif h_type:
        addgvar("PMLOG", h_type)
        await event.edit("`Pm logging is enabled`")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PMLOG\n" + "Enabled pm logging.",
            )
    else:
        await event.edit("`Pm logging is already disabled`")




@register(
    outgoing=True, pattern="^\{trg}grplog (on|off)$".format(trg=trgg),
)
async def set_grplog(event):
    "To turn on or turn off group tags logging"
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    GRPLOG = bool(do_log())
    if GRPLOG:
        if h_type:
            await event.edit("`Group logging is already enabled`")
        else:
            addgvar("GRPLOG", h_type)
            await event.edit("`Group logging is disabled`")
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#PMLOG\n" + "Disabled group logging.",
                )
    elif h_type:
        addgvar("GRPLOG", h_type)
        await event.edit("`Group logging is enabled`")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PMLOG\n" + "Enabled pm logging.",
            )
    else:
        await event.edit("`Group logging is already disabled`")






CMD_HELP.update(
    {
        "log": "\
.log\
\nUsage: To turn on logging of messages from that chat.\
\n\n.nolog\
\nUsage: To turn off logging of messages from that chat.\
\n\n.pmlog on|off\
\nUsage: To turn on or turn off logging of Private messages in pmlogger group.\
\n\n.save\
\nUsage: To log the replied message to bot log group so you can check later.\
\n\n.grplog\
\nUsage: To turn on or turn off group tags logging in pmlogger group."
    }
)

