import io
import os
import random
import textwrap
from emoji import get_emoji_regexp
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument

from userbot.events import register
from userbot.utils import edit_or_reply

def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return get_emoji_regexp().sub("", inputString)


@register(outgoing=True, pattern="^.stk(?: |$)(.*)")
async def sticklet(event):
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)
    reply_message = event.message
    # get the input text
    # the text on which we would like to do the magic on
    font_file_name = event.pattern_match.group(1)
    if not font_file_name:
        font_file_name = ""
    sticktext = event.pattern_match.group(1)
    if not sticktext:
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
            sticktext = reply_message.message
        else:
            await edit_or_reply(event, "need something, hmm")
            return
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    # delete the userbot command,
    # i don't know why this is required
    await event.delete()
    sticktext = deEmojify(sticktext)
    # https://docs.python.org/3/library/textwrap.html#textwrap.wrap
    sticktext = textwrap.wrap(sticktext, width=10)
    # converts back the list to a string
    sticktext = "\n".join(sticktext)
    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230
    FONT_FILE = ("Fizilion/resources/Aerospace.ttf", font_file_name)
    font = ImageFont.truetype(FONT_FILE, size=fontsize)
    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)
    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2, (512 - height) / 2), sticktext, font=font, fill=(R, G, B)
    )
    image_stream = io.BytesIO()
    image_stream.name = "@ProjectFizilion.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)
    # finally, reply the sticker
    await event.client.send_file(
        event.chat_id,
        image_stream,
        caption="Fizilion's Sticklet",
        reply_to=event.message.reply_to_msg_id,
    )
    # cleanup
    try:
        os.remove(FONT_FILE)
    except BaseException:
        pass
