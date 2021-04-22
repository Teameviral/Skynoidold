import os
from glob import glob

from mega import Mega
from pyrogram import filters

from nana import AdminSettings
from nana import app
from nana import COMMAND_PREFIXES
from nana import edit_or_reply

__MODULE__ = 'Mega'
__HELP__ = """
Download any file from URL or Telegram.

──「 **Download Mega File From URL** 」──
-> `mega (url)`
Give url as args to download it.

**Note**
- This is a synchronous module,
  you cannot use your userbot while this module is downloading a file.
- Folders are not supported atm.
"""


async def megadl(url):
    mega = Mega()
    mega.download_url(url, 'nana/downloads/mega')


@app.on_message(
    filters.user(AdminSettings) & filters.command(['mega'], COMMAND_PREFIXES),
)
async def mega_download(_, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await edit_or_reply(message, text='Usage: mega (url)')
        return
    await edit_or_reply(message, text='__Processing...__')
    if not os.path.exists('nana/downloads/mega'):
        os.makedirs('nana/downloads/mega')
    await megadl(args[1])
    files_list = glob('nana/downloads/mega/*')
    for doc in files_list:
        await message.reply_document(doc)
        os.remove(doc)
    await message.delete()
