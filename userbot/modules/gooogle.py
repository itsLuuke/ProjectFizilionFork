import re
import asyncio
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError
from userbot.events import register
from userbot import BOTLOG, BOTLOG_CHATID


@register(outgoing=True, pattern=r"^\.gooogle(?: |$)(\d*)? ?(.*)")
async def gsearch(q_event):
    """For .google command, do a Google search."""
    textx = await q_event.get_reply_message()
    query = q_event.pattern_match.group(1)

    if query:
        pass
    elif textx:
        query = textx.text
    else:
        await q_event.edit(
            "`Pass a query as an argument or reply " "to a message for Google search!`"
        )
        return

    await q_event.edit("`Searching...`")

    search_args = (str(query), 1)
    googsearch = GoogleSearch()
    try:
        gresults = await googsearch.async_search(*search_args)
        msg = ""
        for i in range(0, 5):
            try:
                title = gresults["titles"][i]
                link = gresults["links"][i]
                desc = gresults["descriptions"][i]
                msg += f"{i+1}. [{title}]({link})\n`{desc}`\n\n"
            except IndexError:
                break
        await q_event.edit(
            "**Search Query:**\n`" + query + "`\n\n**Results:**\n" + msg,
            link_preview=False,
        )
    except NoResultsOrTrafficError as error:
        if BOTLOG:
            await q_event.client.send_message(
                BOTLOG_CHATID, f"`GoogleSearch error: {error}`"
            )
        return
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Search query `" + query + "` was executed successfully",
        )

