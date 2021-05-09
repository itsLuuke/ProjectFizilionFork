import asyncio
from asyncio import sleep
from random import choice
from userbot.events import register

T_R_D = [
    "Prajwal",
    "Vinaya",
    "Sharan",
    "Srinidhi",
]

@register(outgoing=True, pattern="^.trd$")
async def truthrdare(trd):
    """Truth or Dare"""
    await trd.edit("`Choosing Name...`")
    await sleep(3)
    await trd.edit("**Name:** ", choice(T_R_D))
