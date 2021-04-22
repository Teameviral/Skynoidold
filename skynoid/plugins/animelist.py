import asyncio
import re

from pyrogram import filters

from skynoid import AdminSettings
from skynoid import app
from skynoid import BotUsername
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply
from skynoid import Owner
from skynoid import setbot
from skynoid.plugins.database import anime_db as sql
from skynoid.utils.Pyroutils import ReplyCheck
from skynoid.utils.sauce import airing_sauce
from skynoid.utils.sauce import character_sauce
from skynoid.utils.sauce import manga_sauce


__MODULE__ = '▲ Animelist ▼'

__HELP__ = """
Module to get information about anime,
manga or characters from [Anilist](https://anilist.co).

──「 **Anime** 」──
-> `anime <anime>`
Returns information about provided anime

__Original Module by @Zero_cooll7870__

──「 **Character** 」──
-> `character <character>`
Returns information about the provided character

──「 **Manga** 」──
-> `manga <manga>`
Returns information about the provided manga

──「 **Airing** 」──
-> `airing <anime>`
Get airing time of an anime

──「 **Favourite List** 」──
-> `favourite`
Get your favourite list of anime
"""


def shorten(description, info='anilist.co'):
    ms_g = ''
    if len(description) > 700:
        description = description[0:500] + '....'
        ms_g += f'\n**Description**: __{description}__[Read More]({info})'
    else:
        ms_g += f'\n**Description**: __{description}__'
    return (
        ms_g.replace('<br>', '')
        .replace('</br>', '')
        .replace('<i>', '')
        .replace('</i>', '')
    )


# time formatter from uniborg
def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + ' Days, ') if days else '')
        + ((str(hours) + ' Hours, ') if hours else '')
        + ((str(minutes) + ' Minutes, ') if minutes else '')
        + ((str(seconds) + ' Seconds, ') if seconds else '')
        + ((str(milliseconds) + ' ms, ') if milliseconds else '')
    )
    return tmp[:-2]


@app.on_message(
    filters.user(AdminSettings) & filters.command('airing', COMMAND_PREFIXES),
)
async def anime_airing(_, message):
    search_str = message.text.split(' ', 1)
    if len(search_str) == 1:
        await edit_or_reply(message, text='Format: `airing <anime name>`')
        return
    response = (await airing_sauce(search_str[1]))['data']['Media']
    ms_g = '**Name**: **{}**(`{}`)\n**ID**: `{}`'.format(
        response['title']['romaji'],
        response['title']['native'],
        response['id'],
    )
    if response['nextAiringEpisode']:
        airing_time = response['nextAiringEpisode']['timeUntilAiring'] * 1000
        airing_time_final = t(airing_time)
        ms_g += '\n**Episode**: `{}`\n**Airing In**: `{}`'.format(
            response['nextAiringEpisode']['episode'],
            airing_time_final,
        )
    else:
        ms_g += f"\n**Episode**:{response['episodes']}\n**Status**: `N/A`"
    await edit_or_reply(message, text=ms_g)


@app.on_message(
    filters.user(AdminSettings) & filters.command('anime', COMMAND_PREFIXES),
)
async def anime_search(client, message):
    cmd = message.command
    mock = ''
    if len(cmd) > 1:
        mock = ' '.join(cmd[1:])
    elif len(cmd) == 1:
        await edit_or_reply(message, text='`Format: anime <anime name>`')
        await asyncio.sleep(2)
        await message.delete()
        return
    x = await client.get_inline_bot_results(f'{BotUsername}', f'anime {mock}')
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
    filters.command('character', COMMAND_PREFIXES),
)
async def character_search(client, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    json = (await character_sauce(search[1]))['data'].get('Character', None)
    if json:
        ms_g = (
            '**{}**(`{}`)\n'.format(
                json.get('name').get('full'),
                json.get('name').get('native'),
            )
        )
        description = f"{json['description']}"
        site_url = json.get('siteUrl')
        ms_g += shorten(description, site_url)
        image = json.get('image', None)
        if image:
            image = image.get('large')
            await message.delete()
            await client.send_photo(message.chat.id, photo=image, caption=ms_g)
        else:
            await edit_or_reply(message, text=ms_g)


@app.on_message(
    filters.user(AdminSettings) & filters.command('manga', COMMAND_PREFIXES),
)
async def manga_search(client, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return

    json = (await manga_sauce(search[1]))['data'].get('Media', None)
    ms_g = ''
    if json:
        title, title_native = json['title'].get(
            'romaji', False,
        ), json['title'].get(
            'native', False,
        )
        start_date, status, score = (
            json['startDate'].get('year', False),
            json.get('status', False),
            json.get('averageScore', False),
        )
        if title:
            ms_g += f'**{title}**'
            if title_native:
                ms_g += f'(`{title_native}`)'
        if start_date:
            ms_g += f'\n**Start Date** - `{start_date}`'
        if status:
            ms_g += f'\n**Status** - `{status}`'
        if score:
            ms_g += f'\n**Score** - `{score}`'
        ms_g += '\n**Genres** - '
        for x in json.get('genres', []):
            ms_g += f'{x}, '
        ms_g = ms_g[:-2]

        image = json.get('bannerImage', False)
        ms_g += f"_{json.get('description', None)}_"
        if image:
            try:
                await message.delete()
                await client.send_photo(
                    message.chat.id,
                    photo=image,
                    caption=ms_g,
                )
            except BaseException:
                ms_g += f' [〽️]({image})'
                await edit_or_reply(message, text=ms_g)
        else:
            await edit_or_reply(message, text=ms_g)


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('favourite', COMMAND_PREFIXES),
)
async def favourite_animelist(client, message):
    x = await client.get_inline_bot_results(f'{BotUsername}', 'favourite')
    await message.delete()
    await client.send_inline_bot_result(
        chat_id=message.chat.id,
        query_id=x.query_id,
        result_id=x.results[0].id,
        reply_to_message_id=ReplyCheck(message),
        hide_via=True,
    )


async def addfav_callback(_, __, query):
    if re.match(r'addfav_', query.data):
        return True


async def remfav_callback(_, __, query):
    if re.match(r'remfav_', query.data):
        return True


@setbot.on_callback_query(filters.create(addfav_callback))
async def add_favorite(_, query):
    if query.from_user.id in AdminSettings:
        match = query.data.split('_')[1]
        add = sql.add_fav(Owner, match)
        if add:
            await query.answer('Added to favourites.', show_alert=True)
        else:
            await query.answer(
                'This anime is already in favourites.',
                show_alert=True,
            )
    else:
        await query.answer(
            'You are not allowed to use this.',
            show_alert=True,
        )


@setbot.on_callback_query(filters.create(remfav_callback))
async def rem_favorite(_, query):
    if query.from_user.id in AdminSettings:
        sql.remove_fav(Owner)
        await setbot.edit_inline_text(
            query.inline_message_id, 'Removed from favourites.',
        )
    else:
        await query.answer(
            'You are not allowed to use this.',
            show_alert=True,
        )
