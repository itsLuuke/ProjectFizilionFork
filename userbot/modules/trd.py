import asyncio
from asyncio import sleep
from random import choice
from userbot.events import register

T_R_D = [
    "[Prajwal](https://t.me/PrajjuS)",
    "[Vinay](https://t.me/Vin02vin)",
    "[Shara](https://t.me/Iamsaisharan)",
    "[Srinidh](https://t.me/venomsamurai)",
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
    
