import os
import shutil

import requests
from pyrogram import filters

from nana import AdminSettings
from nana import app
from nana import COMMAND_PREFIXES
from nana import edit_or_reply

__MODULE__ = 'Uploader'
__HELP__ = """
Reupload URL image to telegram without save it first.

──「 **Upload image** 」──
-> `pic (url)`
Upload image from URL

──「 **Upload sticker** 」──
-> `stk (url)`
Upload image and convert to sticker,
please note image from telegraph will result bug (telegram bugs)
"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('pic', COMMAND_PREFIXES),
)
async def PictureUploader(client, message):
    if len(message.text.split()) == 1:
        await edit_or_reply(message, text='Usage: `.pic <url>`')
        return
    photo = message.text.split(None, 1)[1]
    await message.delete()
    if 'http' in photo:
        r = requests.get(photo, stream=True)
        with open('nana/cache/pic.png', 'wb') as stk:
            shutil.copyfileobj(r.raw, stk)
        if message.reply_to_message:
            await client.send_photo(
                message.chat.id,
                'nana/cache/pic.png',
                reply_to_message_id=message.reply_to_message.message_id,
            )
        else:
            await client.send_photo(message.chat.id, 'nana/cache/pic.png')
        os.remove('nana/cache/pic.png')
    else:
        if message.reply_to_message:
            await client.send_photo(
                message.chat.id,
                photo,
                '',
                reply_to_message_id=message.reply_to_message.message_id,
            )
        else:
            await client.send_photo(message.chat.id, photo, '')


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('stk', COMMAND_PREFIXES),
)
async def StickerUploader(client, message):
    if len(message.text.split()) == 1:
        await edit_or_reply(message, text='Usage: `.stk <url>`')
        return
    photo = message.text.split(None, 1)[1]
    await message.delete()
    if 'http' in photo:
        r = requests.get(photo, stream=True)
        with open('nana/cache/stiker.png', 'wb') as stk:
            shutil.copyfileobj(r.raw, stk)
        if message.reply_to_message:
            await client.send_sticker(
                message.chat.id,
                'nana/cache/stiker.png',
                reply_to_message_id=message.reply_to_message.message_id,
            )
        else:
            await client.send_sticker(message.chat.id, 'nana/cache/stiker.png')
        os.remove('nana/cache/stiker.png')
    else:
        if message.reply_to_message:
            await client.send_sticker(
                message.chat.id,
                photo,
                reply_to_message_id=message.reply_to_message.message_id,
            )
        else:
            await client.send_sticker(message.chat.id, photo)
