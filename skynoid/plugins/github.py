import asyncio
import os
from asyncio import sleep
from glob import iglob
from random import randint

import aiofiles
import aiohttp
from pyrogram import filters
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from nana import AdminSettings
from nana import app
from nana import COMMAND_PREFIXES
from nana import edit_or_reply
from nana.utils.aiohttp_helper import AioHttp
from nana.utils.Pyroutils import ReplyCheck

__MODULE__ = 'Github'
__HELP__ = """
By using this module, you can get information about a GitHub user.

──「 **Github User Info** 」──
-> `git (username)`
"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('git', COMMAND_PREFIXES),
)
async def github(client, message):
    if len(message.text.split()) == 1:
        await edit_or_reply(message, text='Usage: `git (username)`')
        return
    username = message.text.split(None, 1)[1]
    URL = f'https://api.github.com/users/{username}'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await edit_or_reply(
                    message,
                    text='`' + username + ' not found`',
                )

            result = await request.json()

            url = result.get('html_url', None)
            name = result.get('name', None)
            company = result.get('company', None)
            bio = result.get('bio', None)
            created_at = result.get('created_at', 'Not Found')
            repo_url = f'https://github.com/{username}?tab=repositories'
            REPLY = (
                '**Info Of {}**'
                '\n**Username:** `{}`\n**Bio:** `{}`\n**Profile:** [Link]({})'
                '\n**Company:** `{}`\n**Created at:** `{}`'
                '\n**Repository:** [Link]({})'
            ).format(
                name,
                username,
                bio,
                url,
                company,
                created_at,
                repo_url,
            )
        url = f'https://ghchart.rshah.org/{username}'
        file_name = f'{randint(1, 999)}{username}'
        resp = await AioHttp.get_raw(url)
        f = await aiofiles.open(f'{file_name}.svg', mode='wb')
        await f.write(resp)
        await f.close()

        try:
            drawing = svg2rlg(f'{file_name}.svg')
            renderPM.drawToFile(drawing, f'{file_name}.png')
        except UnboundLocalError:
            await edit_or_reply(message, text='`User does not exist!`')
            await sleep(2)
            await message.delete()
            return
        await asyncio.gather(
            client.send_photo(
                chat_id=message.chat.id,
                photo=f'{file_name}.png',
                caption=REPLY,
                reply_to_message_id=ReplyCheck(message),
            ),
        )
    for file in iglob(f'{file_name}.*'):
        os.remove(file)
