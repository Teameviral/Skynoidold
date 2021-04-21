from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineQueryResultArticle
from pyrogram.types import InputTextMessageContent

from pykeyboard import InlineKeyboard

from nana import app, USERBOT_VERSION, DB_AVAILABLE
from nana.languages.strings import tld

from pyrogram import __version__
from platform import python_version


async def alive_func(answers):
    buttons = InlineKeyboard(row_width=1)
    try:
        me = await app.get_me()
    except ConnectionError:
        me = None
    nana_stats = 'stopped' if not me else 'alive'
    buttons.add(
        InlineKeyboardButton(
            '🏓',
            callback_data='alive_message',
        ),
    )
    answers.append(
        InlineQueryResultArticle(
            title='Alive',
            description='Nana Userbot',
            input_message_content=InputTextMessageContent(
                tld('alive_str').format(
                    nana_stats,
                    USERBOT_VERSION,
                    __version__,
                    python_version(),
                    DB_AVAILABLE,
                ),
                parse_mode='markdown',
                disable_web_page_preview=True,
            ),
            reply_markup=buttons,
        ),
    )
