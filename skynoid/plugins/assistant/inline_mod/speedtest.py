from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineQueryResultArticle
from pyrogram.types import InputTextMessageContent

from pykeyboard import InlineKeyboard

from skynoid.languages.strings import tld


async def speedtest_func(answers):
    buttons = InlineKeyboard(row_width=2)
    buttons.add(
        InlineKeyboardButton(
            tld('speed_test_button_image'),
            callback_data='speedtest_image',
        ),
        InlineKeyboardButton(
            tld('speed_test_button_text'),
            callback_data='speedtest_text',
        ),
    )
    answers.append(
        InlineQueryResultArticle(
            title='Speed Test',
            description='test your speed',
            input_message_content=InputTextMessageContent(
                tld('speed_test_trigger'), parse_mode='markdown',
            ),
            reply_markup=buttons,
        ),
    )
