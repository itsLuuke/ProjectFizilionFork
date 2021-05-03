import re
import asyncio
from search_engine_parser.core.engines.google import Search as GoogleSearch
from userbot.events import register


@register(outgoing=True, pattern=r"^\.gooogle(?: |$)(\d*)? ?(.*)")
async def gsearch(q_event):
    await q_event.edit("`searching........`")
    match = q_event.pattern_match.group(1)
    page = re.findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    try:
        gsearch = GoogleSearch()
        gresults = await gsearch.async_search(*search_args)
    except Exception:
        return await q_event.edit(
            "`Error: Your query could not be found or it was flagged as unusual traffic.`"
        )
    msg = ""

    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"👉[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await q_event.edit(
        "**Search Query:**\n`" + match + "`\n\n**Results:**\n" + msg, link_preview=False
    )
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID, "Google Search query `" + match + "` was executed successfully"
        )
