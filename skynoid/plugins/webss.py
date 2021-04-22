import os

from pyrogram import filters

from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply
from skynoid import SCREENSHOTLAYER_API

__MODULE__ = '▲ SS Website ▼'
__HELP__ = """
Take a picture of website. You can select one for use this.

──「 **Take ss website (more)** 」──
-> `ss (url) (*full)`
Take screenshot of that website, if `full` args given,
take full of website and send image as document

* = optional
"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('ss', COMMAND_PREFIXES),
)
async def ss_web(client, message):
    if len(message.text.split()) == 1:
        await edit_or_reply(message, text='Usage: `print web.url`')
        return
    if not SCREENSHOTLAYER_API:
        await edit_or_reply(
            message, text='You need to fill screenshotlayer_API to use this!',
        )
        return
    args = message.text.split(None, 1)
    t = args[1]
    full = False
    if len(
        message.text.split(),
    ) >= 3 and message.text.split(None, 2)[2] == 'full':
        full = True

    t = t if 'http://' in t or 'https://' in t else 'http://' + t
    capt = f'Website: `{t}`'

    await client.send_chat_action(message.chat.id, action='upload_photo')
    api_uri = 'http://api.screenshotlayer.com/api/capture?access_key='
    if full:
        r = '{}{}&url={}&fullpage=1'.format(
            api_uri,
            SCREENSHOTLAYER_API,
            t,
        )
    else:
        r = '{}{}&url={}&fullpage=0'.format(
            api_uri,
            SCREENSHOTLAYER_API,
            t,
        )
    await message.delete()
    await client.send_photo(message.chat.id, photo=r, caption=capt)
    os.remove('skynoid/cache/web.png')
    await client.send_chat_action(message.chat.id, action='cancel')
