import asyncio
import random

from pyrogram import filters

from skynoid import app, COMMAND_PREFIXES, AdminSettings, edit_or_reply
from skynoid.utils.Pyroutils import ReplyCheck


__MODULE__ = 'Stickerizer'
__HELP__ = """
Module that uses inline Stickerizer bot!

──「 **Mock** 」──
-> `mock`
Stikerize spongebob mocking sticker.

──「 **Waifu** 」──
-> `waifu`
Stickerize Waifu text.

──「 **Senpai** 」──
-> `senpai`
Stickerize senpai text.

──「 **Google Search Sticker** 」──
-> `ggl`
google search with a sticker.
"""


waifus = [20, 32, 33, 40, 41, 42, 58]
senpais = [37, 38, 48, 55]


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('ggl', COMMAND_PREFIXES),
)
async def google_search(client, message):
    cmd = message.command
    googles = ''
    if len(cmd) > 1:
        googles = ' '.join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        googles = message.reply_to_message.text
    elif len(cmd) == 1:
        await edit_or_reply(
            message, text='`No text Given hence can not google the void.`',
        )
        await asyncio.sleep(2)
        await message.delete()
        return
    x = await client.get_inline_bot_results('Stickerizerbot', f'#12{googles}')
    await message.delete()
    await client.send_inline_bot_result(
        chat_id=message.chat.id,
        query_id=x.query_id,
        result_id=x.results[0].id,
        reply_to_message_id=ReplyCheck(message),
        hide_via=True,
    )


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('mock', COMMAND_PREFIXES),
)
async def mock_spongebob(client, message):
    cmd = message.command
    mock = ''
    if len(cmd) > 1:
        mock = ' '.join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        mock = message.reply_to_message.text
    elif len(cmd) == 1:
        await edit_or_reply(message, text="`Can't mock the void.`")
        await asyncio.sleep(2)
        await message.delete()
        return
    x = await client.get_inline_bot_results('Stickerizerbot', f'#7{mock}')
    await message.delete()
    await client.send_inline_bot_result(
        chat_id=message.chat.id,
        query_id=x.query_id,
        result_id=x.results[0].id,
        reply_to_message_id=ReplyCheck(message),
        hide_via=True,
    )


@app.on_message(
    filters.user(AdminSettings) & filters.command('senpai', COMMAND_PREFIXES),
)
async def senpai_sticker(client, message):
    cmd = message.command
    senpai = ''
    if len(cmd) > 1:
        senpai = ' '.join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        senpai = message.reply_to_message.text
    elif len(cmd) == 1:
        await edit_or_reply(
            message,
            text='`No text Given hence the senpai Ran Away.`',
        )
        await asyncio.sleep(2)
        await message.delete()
        return
    x = await client.get_inline_bot_results(
        'Stickerizerbot', f'#{random.choice(senpais)}{senpai}',
    )
    await message.delete()
    await client.send_inline_bot_result(
        chat_id=message.chat.id,
        query_id=x.query_id,
        result_id=x.results[0].id,
        reply_to_message_id=ReplyCheck(message),
        hide_via=True,
    )


@app.on_message(
    filters.user(AdminSettings) & filters.command('waifu', COMMAND_PREFIXES),
)
async def waifu_sticker(client, message):
    cmd = message.command
    waifu = ''
    if len(cmd) > 1:
        waifu = ' '.join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        waifu = message.reply_to_message.text
    elif len(cmd) == 1:
        await edit_or_reply(
            message,
            text='`No text Given hence the waifu Ran Away.`',
        )
        await asyncio.sleep(2)
        await message.delete()
        return
    x = await client.get_inline_bot_results(
        'Stickerizerbot', f'#{random.choice(waifus)}{waifu}',
    )
    await message.delete()
    await client.send_inline_bot_result(
        chat_id=message.chat.id,
        query_id=x.query_id,
        result_id=x.results[0].id,
        reply_to_message_id=ReplyCheck(message),
        hide_via=True,
    )
