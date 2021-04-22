from asyncio import sleep

from pyrogram import filters

from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply
from skynoid.utils.expand import expand_url

__MODULE__ = '▲ Link Expander ▼'
__HELP__ = """
──「 **Expand URL** 」──
-> `expand (link)`
Reply a short URL or include as an arg to expand it.
"""


@app.on_message(
    filters.command('expand', COMMAND_PREFIXES) &
    filters.user(AdminSettings),
)
async def expand(_, message):
    if message.reply_to_message:
        url = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        url = message.command[1]
    else:
        url = None

    if url:
        expanded = await expand_url(url)
        if expanded:
            await edit_or_reply(
                message,
                text=f'Shortened URL: {url}\nExpanded URL: {expanded}',
                disable_web_page_preview=True,
            )
            return
        else:
            await edit_or_reply(message, text="`I can't expand this url :p`")
            await sleep(3)
            await message.delete()
    else:
        await edit_or_reply(message, text='Nothing given to expand.')
