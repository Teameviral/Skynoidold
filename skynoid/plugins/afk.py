import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from pykeyboard import InlineKeyboard

from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import DB_AVAILABLE
from skynoid import edit_or_reply
from skynoid import Owner
from skynoid import OwnerName
from skynoid import setbot
from skynoid.utils.msg_types import get_message_type
from skynoid.utils.msg_types import Types
from skynoid.utils.parser import escape_markdown
from skynoid.utils.parser import mention_markdown

if DB_AVAILABLE:
    from skynoid.plugins.database.afk_db import set_afk, get_afk

__MODULE__ = '▲ AFK ▼'
__HELP__ = """
Module for enabling auto replies when you are AFK.
When enabled,
anyone who mentions you will be replied with a message saying that
you are AFK plus the assistant will
send you a message saying that someone mentioned you.

Restarting your bot won't remove your AFK status.

──「 **Setting AFK Status** 」──
-> `afk (*reason)`
Enable auto replies when you are AFK.

To stop it, send something somewhere (excluding PM and saved messages).

* = Optional
"""

# Set priority to 11 and 12
MENTIONED = []
AFK_RESTIRECT = {}
DELAY_TIME = 60  # seconds


@app.on_message(filters.me & (filters.command('afk', COMMAND_PREFIXES)))
async def afk(_, message):
    if not DB_AVAILABLE:
        await message.edit("You haven't set up a database!")
        return
    if len(message.text.split()) >= 2:
        set_afk(True, message.text.split(None, 1)[1])
        await message.edit(
            '{} is now AFK!\nReason: {}'.format(
                mention_markdown(
                    message.from_user.id,
                    message.from_user.first_name,
                ),
                message.text.split(None, 1)[1],
            ),
        )
        await setbot.send_message(
            Owner,
            'You are now AFK!\nReason: {}'.format(
                message.text.split(None, 1)[1],
            ),
        )
    else:
        set_afk(True, '')
        await message.edit(
            '{} is now AFK!'.format(
                mention_markdown(
                    message.from_user.id,
                    message.from_user.first_name,
                ),
            ),
        )
        await setbot.send_message(Owner, 'You are now AFK!')
    await message.stop_propagation()


@app.on_message(filters.mentioned & ~filters.bot, group=11)
async def afk_mentioned(_, message):
    if not DB_AVAILABLE:
        return
    global MENTIONED
    get = get_afk()
    if get and get['afk']:
        if '-' in str(message.chat.id):
            cid = str(message.chat.id)[4:]
        else:
            cid = str(message.chat.id)

        if cid in list(
            AFK_RESTIRECT,
        ) and int(
            AFK_RESTIRECT[cid],
        ) >= int(time.time()):
            return
        AFK_RESTIRECT[cid] = int(time.time()) + DELAY_TIME
        if get['reason']:
            await edit_or_reply(
                message,
                text='Sorry, {} is AFK!\nReason: {}'.format(
                    mention_markdown(Owner, OwnerName),
                    get['reason'],
                ),
            )
        else:
            await edit_or_reply(
                message, text='Sorry, {} is AFK!'.format(
                    mention_markdown(Owner, OwnerName),
                ),
            )

        _, message_type = get_message_type(message)
        if message_type == Types.TEXT:
            text = message.text or message.caption
        else:
            text = message_type.name

        MENTIONED.append(
            {
                'user': message.from_user.first_name,
                'user_id': message.from_user.id,
                'chat': message.chat.title,
                'chat_id': cid,
                'text': text,
                'message_id': message.message_id,
            },
        )
        button = InlineKeyboard(row_width=1)
        button.add(InlineKeyboardButton('🔗', url=message.link))
        await setbot.send_message(
            Owner,
            '{} mentioned you in {}\n\n{}\n\nTotal mentions: `{}`'.format(
                mention_markdown(
                    message.from_user.id,
                    message.from_user.first_name,
                ),
                message.chat.title,
                text[:3500],
                len(MENTIONED),
            ),
            reply_markup=button,
        )


@app.on_message(filters.me & filters.group, group=12)
async def no_longer_afk(_, message):
    if not DB_AVAILABLE:
        return
    global MENTIONED
    get = get_afk()
    if get and get['afk']:
        await setbot.send_message(
            message.from_user.id,
            'You are no longer AFK!',
        )
        set_afk(False, '')
        text = '**While you were AFK, you were mentioned {} times.**\n'.format(
            len(MENTIONED),
        )
        for x in MENTIONED:
            msg_text = x['text']
            if len(msg_text) >= 11:
                msg_text = '{}...'.format(x['text'])
            text += '- [{}](https://t.me/c/{}/{}) ({}): {}\n'.format(
                escape_markdown(x['user']),
                x['chat_id'],
                x['message_id'],
                x['chat'],
                msg_text,
            )
        await setbot.send_message(message.from_user.id, text)
        MENTIONED = []
