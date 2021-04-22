import re
import time

from __main__ import HELP_COMMANDS  # pylint: disable-msg=E0611
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.raw import functions

from skynoid import (
    setbot,
    AdminSettings,
    COMMAND_PREFIXES,
    DB_AVAILABLE,
    SKYNOID_IMG,
    BotUsername,
    app,
    StartTime,
)
from skynoid.utils import filt
from skynoid.utils.misc import paginate_modules
from skynoid.plugins.chats import get_msgc
from skynoid.languages.strings import tld

if DB_AVAILABLE:
    from skynoid.plugins.database.chats_db import get_all_chats
    from skynoid.plugins.database.notes_db import get_all_selfnotes


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ''
    time_list = []
    time_suffix_list = ['s', 'm', 'h', 'days']
    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60,
        ) if count < 3 else divmod(
            seconds, 24,
        )
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ', '
    time_list.reverse()
    ping_time += ':'.join(time_list)
    return ping_time


async def help_parser(client, chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(
            paginate_modules(0, HELP_COMMANDS, 'help'),
        )
    if SKYNOID_IMG:
        await client.send_photo(
            chat_id,
            SKYNOID_IMG,
            caption=text,
            reply_markup=keyboard,
        )
    else:
        await client.send_message(chat_id, text, reply_markup=keyboard)


@setbot.on_message(filters.user(AdminSettings) & filt.command(['help']))
async def help_command(client, message):
    if message.chat.type != 'private':
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text='Help',
                        url=f't.me/{BotUsername}?start=help',
                    ),
                ],
            ],
        )
        await message.reply(
            '**OWNER ONLY**\nContact me in PM',
            reply_markup=buttons,
        )
        return
    await help_parser(
        client,
        message.chat.id,
        tld('help_str').format(', '.join(COMMAND_PREFIXES)),
    )


async def help_button_callback(_, __, query):
    if re.match(r'help_', query.data):
        return True


help_button_create = filters.create(help_button_callback)


@setbot.on_callback_query(help_button_create)
async def help_button(_, query):
    mod_match = re.match(r'help_module\((.+?)\)', query.data)
    back_match = re.match(r'help_back', query.data)
    if mod_match:
        module = mod_match.group(1)
        text = (
            'This is help for the module **{}**:\n'.format(
                HELP_COMMANDS[module].__MODULE__,
            )
            + HELP_COMMANDS[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text='Back',
                            callback_data='help_back',
                        ),
                    ],
                ],
            ),
        )

    elif back_match:
        await query.message.edit(
            text=tld('help_str').format(', '.join(COMMAND_PREFIXES)),
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELP_COMMANDS, 'help'),
            ),
        )
    await query.answer()


@setbot.on_message(
    filters.user(AdminSettings)
    & filt.command(['stats'])
    & (filters.group | filters.private),
)
async def stats(_, message):
    text = '**Current stats**\n'
    if DB_AVAILABLE:
        text += ' - **Notes**: `{} notes`\n'.format(
            len(get_all_selfnotes(message.from_user.id) or ''),
        )
        text += ' - **Group joined**: `{} groups`\n'.format(
            len(get_all_chats()),
        )
    stk = await app.send(functions.messages.GetAllStickers(hash=0))
    all_sets = stk.sets
    count = sum(x.count for x in all_sets)
    text += ' - **Stickers Count**: <code>{} over {} packs</code>\n'.format(
        count,
        len(all_sets),
    )
    text += ' - **Message received**: `{} messages`\n'.format(
        get_msgc(),
    )
    uptime = get_readable_time(time.time() - StartTime)
    text += f' - **Skynoid uptime**: `{uptime}`'
    await message.reply_text(text, quote=True)
