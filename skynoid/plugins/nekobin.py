import asyncio
import os

from nekobin import NekoBin
from pyrogram import filters

from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply
from skynoid.utils import capture_err
from skynoid.utils.aiohttp_helper import AioHttp

__MODULE__ = '▲ Nekobin ▼'
__HELP__ = """
──「 **Paste to Nekobin** 」──
-> `neko`
Create a Nekobin paste with the content of replied message.
"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('neko', COMMAND_PREFIXES),
)
@capture_err
async def paste(client, message):
    nekobin = NekoBin()
    if message.reply_to_message:
        text = message.reply_to_message.text
    if (
        message.reply_to_message.document
        and message.reply_to_message.document.file_size < 2 ** 20 * 10
    ):
        var = os.path.splitext(message.reply_to_message.document.file_name)[1]
        print(var)
        path = await message.reply_to_message.download('skynoid/')
        with open(path) as doc:
            text = doc.read()
        os.remove(path)
    try:
        response = await nekobin.nekofy(text)
    except Exception:
        await message.edit_text('`Pasting failed`')
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        reply_text = '**Nekofied:**\n'
        reply_text += f' - **Link**: {response.url}\n'
        reply_text += f' - **Raw**: {response.raw}'
        delete = bool(
            len(message.command) > 1
            and message.command[1] in ['d', 'del']
            and message.reply_to_message.from_user.is_self,
        )
        if delete:
            await asyncio.gather(
                client.send_message(
                    message.chat.id, reply_text, disable_web_page_preview=True,
                ),
                message.reply_to_message.delete(),
                message.delete(),
            )
        else:
            await message.edit_text(
                reply_text,
                disable_web_page_preview=True,
            )


@app.on_message(
    filters.user(AdminSettings) &
    filters.command(['gpaste'], COMMAND_PREFIXES),
)
@capture_err
async def get_paste_(_, message):
    """fetches the content of a dogbin or nekobin URL."""
    link = message.reply_to_message.text
    if not link:
        await edit_or_reply(message, text='Give me a link!')
        return
    await edit_or_reply(message, text='`Getting paste content...`')
    format_view = 'https://del.dog/v/'
    if link.startswith(format_view):
        link = link[len(format_view):]
        raw_link = f'https://del.dog/raw/{link}'
    elif link.startswith('https://del.dog/'):
        link = link[len('https://del.dog/'):]
        raw_link = f'https://del.dog/raw/{link}'
    elif link.startswith('del.dog/'):
        link = link[len('del.dog/'):]
        raw_link = f'https://del.dog/raw/{link}'
    elif link.startswith('https://nekobin.com/'):
        link = link[len('https://nekobin.com/'):]
        raw_link = f'https://nekobin.com/raw/{link}'
    elif link.startswith('nekobin.com/'):
        link = link[len('nekobin.com/'):]
        raw_link = f'https://nekobin.com/raw/{link}'
    else:
        await edit_or_reply(message, text='Is that even a paste url?')
        return
    resp = await AioHttp().get_text(raw_link)
    await edit_or_reply(message, text=f'**Content**:\n`{resp}`')
