from skynoid.utils.sauce import anime_sauce
from pyrogram.types import InlineKeyboardButton
from skynoid.plugins.animelist import shorten
from pyrogram.types import InlineQueryResultArticle
from pyrogram.types import InlineQueryResultPhoto
from pyrogram.types import InputTextMessageContent

from pykeyboard import InlineKeyboard


async def anime_func(string, answers):
    json = (
        await anime_sauce(
            string.split(None, 1)[1],
        )
    )['data'].get('Media', None)
    if json:
        msg = (
            '**{}** (`{}`)\n'
            '**Type**: {}\n'
            '**Status**: {}\n'
            '**Episodes**: {}\n'
            '**Duration**: {}'
            'Per Ep.\n**Score**: {}\n**Genres**: `'
        ).format(
            json['title']['romaji'],
            json['title']['native'],
            json['format'],
            json['status'],
            json.get('episodes', 'N/A'),
            json.get('duration', 'N/A'),
            json['averageScore'],
        )
        for x in json['genres']:
            msg += f'{x}, '
        msg = msg[:-2] + '`\n'
        msg += '**Studios**: `'
        for x in json['studios']['nodes']:
            msg += f"{x['name']}, "
        msg = msg[:-2] + '`\n'
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == 'youtube':
                trailer = 'https://youtu.be/' + trailer_id
        description = (
            json.get('description', 'N/A')
            .replace('<i>', '')
            .replace('</i>', '')
            .replace('<br>', '')
        )
        msg += shorten(description, info)
        image = f'https://img.anili.st/media/{json["id"]}'
        buttons = InlineKeyboard(row_width=2)
        if trailer:
            buttons.add(
                InlineKeyboardButton('Trailer 🎬', url=trailer),
            )
        buttons.add(
            InlineKeyboardButton('More Info', url=info),
            InlineKeyboardButton(
                'Add to Watchlist',
                callback_data=f'addfav_{json["title"]["romaji"]}',
            ),
        )
        if image:
            answers.append(
                InlineQueryResultPhoto(
                    caption=msg,
                    photo_url=image,
                    parse_mode='markdown',
                    title=f"{json['title']['romaji']}",
                    description=f"{json['format']}",
                    reply_markup=buttons,
                ),
            )
        else:
            answers.append(
                InlineQueryResultArticle(
                    title=f"{json['title']['romaji']}",
                    description=f"{json['averageScore']}",
                    input_message_content=InputTextMessageContent(
                        msg,
                        parse_mode='markdown',
                        disable_web_page_preview=True,
                    ),
                    reply_markup=buttons,
                ),
            )
