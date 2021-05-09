import asyncio
from asyncio import sleep
from random import choice
from userbot.events import register

T_R_D = [
    "@PrajjuS[Prajwal]",
    "@Vin02vin[Vinay]",
    "@Iamsaisharan[Sharan]",
    "@venomsamurai[Srinidh]",
]

@register(outgoing=True, pattern="^.trd$")
async def truthrdare(trd):
    """Truth or Dare"""
    await trd.edit("`Choosing Name...`")
    await sleep(1.5)
    await trd.edit("`..............`")
    await sleep(1.5)
    msg = await trd.edit("`Name is.....`")
    await sleep(3)
    await trd.delete()
    await msg.reply("**Name:** " + choice(T_R_D))
    
