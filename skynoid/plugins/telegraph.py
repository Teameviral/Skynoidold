import os

from pyrogram import filters
from telegraph import upload_file

from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply

__MODULE__ = 'Telegra.ph'
__HELP__ = """
Paste Media Documents on Telegra.ph

──「 **Telegra.ph** 」──
-> `telegraph (reply to a media)`
Reply to Media as args to upload it to telegraph.
- Supported Media Types (.jpg, .jpeg, .png, .gif, .mp4)

"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('telegraph', COMMAND_PREFIXES),
)
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await edit_or_reply(message, text='reply to a supported media file')
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith('.mp4')
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                ('.jpg', '.jpeg', '.png', '.gif', '.mp4'),
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await edit_or_reply(message, text='not supported!')
        return
    download_location = await client.download_media(
        message=message.reply_to_message, file_name='root/skynoid/',
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await edit_or_reply(message, text=document)
    else:
        await edit_or_reply(
            message,
            text=f'**Link: https://telegra.ph{response[0]}**',
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)
