import asyncio
import os
from platform import python_version

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from pykeyboard import InlineKeyboard

from skynoid import AdminSettings
from skynoid import app
from skynoid import ASSISTANT_VERSION
from skynoid import BotUsername
from skynoid import DB_AVAILABLE
from skynoid import SKYNOID_IMG
from skynoid import OwnerName
from skynoid import setbot
from skynoid import USERBOT_VERSION
from skynoid.languages.strings import tld
from skynoid.utils import filt
from skynoid.plugins.assistant.settings import get_button_settings
from skynoid.plugins.assistant.settings import get_text_settings
from skynoid.utils.dynamic_filt import dynamic_data_filter

if DB_AVAILABLE:
    from skynoid.plugins.database.chats_db import get_all_chats


@setbot.on_message(filters.private & ~filters.user(AdminSettings))
async def un_auth(_, message):
    if message.chat.id is AdminSettings:
        return

    msg = f"""
Hi {message.chat.first_name},
You must be looking forward on how I work.
In that case I can give you helpful links to self host me on your own.
Here are some links for you
        """
    buttons = InlineKeyboard(row_width=2)
    buttons.add(
        InlineKeyboardButton(
            'Documentation', url='https://t.me/SkinoidBot',
        ),
        InlineKeyboardButton(
            'Repository', url='https://github.com/TeamEviral/Skynoid',
        ),
        InlineKeyboardButton('Support', url='https://t.me/SkynoidSupport'),
    )
    await message.reply(msg, reply_markup=buttons)


@setbot.on_message(filters.user(AdminSettings) & filt.command(['start']))
async def start(_, message):
    if message.chat.type != 'private':
        await message.reply('henlo ^0^')
    else:
        if len(message.text.split()) >= 2:
            helparg = message.text.split()[1]
            if helparg == 'help_inline':
                await message.reply(
                    tld(
                        'inline_help_text',
                    ).format(
                        BotUsername,
                    ),
                )
                return
        try:
            me = await app.get_me()
        except ConnectionError:
            me = None
        userbot_stat = 'Stopped' if not me else 'Running'
        db_stat = len(get_all_chats()) if DB_AVAILABLE else 'None'
        buttons = InlineKeyboard(row_width=1)
        buttons.add(
            InlineKeyboardButton(tld('help_btn'), callback_data='help_back'),
        )
        if SKYNOID_IMG:
            await message.reply_photo(
                SKYNOID_IMG,
                caption=tld('start_message').format(
                    OwnerName,
                    python_version(),
                    userbot_stat,
                    USERBOT_VERSION,
                    ASSISTANT_VERSION,
                    DB_AVAILABLE,
                    db_stat,
                ),
                reply_markup=buttons,
            )
        else:
            await message.reply(
                tld('start_message').format(
                    OwnerName,
                    python_version(),
                    userbot_stat,
                    USERBOT_VERSION,
                    ASSISTANT_VERSION,
                    DB_AVAILABLE,
                    db_stat,
                ),
                reply_markup=buttons,
            )


@setbot.on_message(filters.user(AdminSettings) & filt.command(['getme']))
async def get_myself(client, message):
    try:
        me = await app.get_me()
    except ConnectionError:
        await message.reply('Bot is currently turned off!')
        return
    text = '**Myself**\n'
    text += f' - **First name**: `{me.first_name}`\n'
    if me.last_name:
        text += f' - **Last name**: `{me.last_name}`\n'
    text += f' - **User ID**: `{me.id}`\n'
    if me.username:
        text += f' - **Username**: `@{me.username}`\n'
    text += f' - **Phone number**: `{me.phone_number}`\n'
    text += f' - **Skynoid Version**: `v{USERBOT_VERSION}`\n'
    text += f' - **Manager Version**: `v{ASSISTANT_VERSION}`'
    button = InlineKeyboard(row_width=1)
    button.add(
        InlineKeyboardButton('Hide phone number', callback_data='hide_number'),
    )
    if me.photo:
        getpp = await client.download_media(
            me.photo.big_file_id,
            file_name='skynoid/downloads/pfp.png',
        )
        await message.reply_photo(
            photo=getpp,
            caption=text,
            reply_markup=button,
        )
    else:
        await message.reply(text, reply_markup=button)
    if os.path.exists(getpp):
        os.remove(getpp)


@setbot.on_callback_query(dynamic_data_filter('hide_number'))
async def get_myself_btn(client, query):
    try:
        me = await app.get_me()
    except ConnectionError:
        await client.answer_callback_query(
            query.id, 'Bot is currently turned off!', show_alert=True,
        )
        return

    if query.message.caption:
        text = query.message.caption.markdown
    else:
        text = query.message.text.markdown

    num = ['#' * len(me.phone_number)]
    button = InlineKeyboard(row_width=1)
    if '###' not in text.split(' - **Phone number**: `')[1].split('`')[0]:
        text = text.replace(
            ' - **Phone number**: `{}`\n'.format(
                me.phone_number,
            ),
            ' - **Phone number**: `{}`\n'.format(
                ''.join(num),
            ),
        )
        button.add(
            InlineKeyboardButton(
                'Show phone number',
                callback_data='hide_number',
            ),
        )
    else:
        text = text.replace(
            ' - **Phone number**: `{}`\n'.format(''.join(num)),
            f' - **Phone number**: `{me.phone_number}`\n',
        )
        button.add(
            InlineKeyboardButton(
                'Hide phone number',
                callback_data='hide_number',
            ),
        )

    if query.message.caption:
        await query.message.edit_caption(caption=text, reply_markup=button)
    else:
        await query.message.edit(text, reply_markup=button)
    await query.answer()


@setbot.on_callback_query(dynamic_data_filter('language_back'))
async def lang_back(_, query):
    text = await get_text_settings()
    button = await get_button_settings()
    await query.message.edit(text, reply_markup=button)
    await query.answer()


@setbot.on_callback_query(dynamic_data_filter('report_errors'))
async def report_some_errors(client, query):
    await app.join_chat('@SkynoidSupport')
    text = 'Hi @Eviral, i got an error for you.'
    err = query.message.text
    with open('skynoid/cache/errors.txt', 'w') as f:
        f.write(err)
    await asyncio.gather(
        query.message.edit_reply_markup(reply_markup=None),
        app.send_document(
            'SkynoidSupport',
            'skynoid/cache/errors.txt',
            caption=text,
        ),
        client.answer_callback_query(query.id, 'Report was sent!'),
    )
    os.remove('skynoid/cache/errors.txt')
