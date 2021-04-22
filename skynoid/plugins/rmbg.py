# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.
# Ported to Nana by @pokurt
import os
from asyncio import sleep

from pyrogram import filters
from removebg import RemoveBg

from nana import AdminSettings
from nana import app
from nana import COMMAND_PREFIXES
from nana import edit_or_reply
from nana import REMOVE_BG_API
from nana.utils.Pyroutils import ReplyCheck

DOWN_PATH = 'nana/'

IMG_PATH = DOWN_PATH + 'image.jpg'


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('rmbg', COMMAND_PREFIXES),
)
async def remove_bg(client, message):
    if not REMOVE_BG_API:
        await edit_or_reply(
            message,
            text='Invalid API',
            disable_web_page_preview=True,
            parse_mode='html',
        )
    replied = message.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and 'image' in replied.document.mime_type)
        )
    ):
        if os.path.exists(IMG_PATH):
            os.remove(IMG_PATH)
        await client.download_media(message=replied, file_name=IMG_PATH)
        try:
            rmbg = RemoveBg(REMOVE_BG_API, 'rm_bg_error.txt')
            rmbg.remove_background_from_img_file(IMG_PATH)
            remove_img = IMG_PATH + '_no_bg.png'
            await client.send_document(
                chat_id=message.chat.id,
                document=remove_img,
                reply_to_message_id=ReplyCheck(message),
                disable_notification=True,
            )
            await message.delete()
            os.remove(remove_img)
            os.remove(IMG_PATH)
        except Exception as e:
            print(e)
            await edit_or_reply(message, text='`Something went wrong!`')
            await sleep(3)
            await message.delete()
    else:
        await edit_or_reply(
            message, text='Usage: reply to a photo to remove background!',
        )
