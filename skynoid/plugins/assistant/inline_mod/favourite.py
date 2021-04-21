from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineQueryResultArticle
from pyrogram.types import InputTextMessageContent

from pykeyboard import InlineKeyboard

from skynoid import Owner


async def fav_func(fav, answers):
    keyb = InlineKeyboard(row_width=1)
    if fav:
        text = '**My watchlist:**\n'
        for title in fav:
            text += f' - {title.data}\n'
        keyb.add(
            InlineKeyboardButton(
                text='Watched ✅', callback_data=f'remfav_{Owner}',
            ),
        )
        answers.append(
            InlineQueryResultArticle(
                title='Favourites',
                description='Anime',
                input_message_content=InputTextMessageContent(
                    text, parse_mode='markdown',
                ),
                reply_markup=keyb,
            ),
        )
    else:
        answers.append(
            InlineQueryResultArticle(
                title='Fabourites',
                description='Anime',
                input_message_content=InputTextMessageContent(
                    '**No favourites yet!**', parse_mode='markdown',
                ),
            ),
        )
