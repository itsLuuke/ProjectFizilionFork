from userbot import CMD_HELP, bot, trgg
from userbot.events import register
from telethon.events import NewMessage


@register(outgoing=True, pattern="^\{trg}fstat(:? |$)(.*)".format(trg=trgg))
async def fstat(e: NewMessage.Event):
	inp = e.pattern_match.group(1)
	tmsg = await e.edit("Checking fstat...")

	rep_user = rep.from_id if (rep := await e.get_reply_messgage()) else None

	user = inp.split(" ")[0] if not inp else ((await e.client.get_me()).id if not rep_user else rep_user)
	fed = inp.split(" ")[1] if inp and len(inp.split(" ")) > 1 else ""

	async with bot.conversation("@MissRose_bot") as conv:
		try:
			await conv.send_message(f"/fstat {user} {fed}")
		except Exception as err:
			await tmsg.edit(f"Cannot check the fstat\nReason:{err}")
		resp = await conv.get_response()
		if resp.reply_markup:
			await resp.click(0)
			resp2 = await conv.get_response()
			await e.send_file(e.chat_id, resp2, caption=resp2.text)
			await tmsg.delete()
			return
		await tmsg.edit(resp.message)

CMD_HELP.update(
		{"fstat": "`.fstat <reply/mention/reply> <fed id>`\nUsage: Get the fstat of the user in @MissRose_bot."}
)
