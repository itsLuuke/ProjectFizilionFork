from search_engine_parser.core.engines.google import Search as GoogleSearch
from userbot.events import register

@register(outgoing=True, pattern=r"^\.gooogle(?: |$)(\d*)? ?(.*)")
async def gsearch(gs):
    await gs.edit("Processing ...")
    query = gs.filtered_input_str
    flags = gs.flags
    page = int(flags.get("-p", 1))
    limit = int(flags.get("-l", 5))
    if gs.reply_to_message:
        query = gs.reply_to_message.text
    if not query:
        await gs.err(text="Give a query or reply to a message to google!")
        return
    try:
        g_search = GoogleSearch()
        gresults = await g_search.async_search(query, page)
    except Exception as e:
        await gs.err(text=e)
        return
    output = ""
    for i in range(limit):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            output += f"[{title}]({link})\n"
            output += f"`{desc}`\n\n"
        except IndexError:
            break
    output = f"**Google Search:**\n`{query}`\n\n**Results:**\n{output}"
    await gs.edit_or_send_as_file(
        text=output, caption=query, disable_web_page_preview=True
    )
    if BOTLOG:
        await gs.client.send_message(
            BOTLOG_CHATID, "Google Search query `" + match + "` was executed successfully"
        )
