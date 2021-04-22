from asyncio import sleep

from pyrogram import filters

from nana import AdminSettings
from nana import app
from nana import COMMAND_PREFIXES
from nana import edit_or_reply
from nana.utils.aiohttp_helper import AioHttp
from nana.utils.string import replace_text

__MODULE__ = 'Urban'
__HELP__ = """
Search for urban dictionary

──「 **Urban Dictionary** 」──
-> `ud (text or reply to a word)`
Search urban for dictionary
"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('ud', COMMAND_PREFIXES),
)
async def urban_dictionary(_, message):
    if len(message.text.split()) == 1:
        await edit_or_reply(message, text='Usage: `ud example`')
        return
    try:
        text = message.text.split(None, 1)[1]
        response = await AioHttp().get_json(
            f'http://api.urbandictionary.com/v0/define?term={text}',
        )
        word = response['list'][0]['word']
        definition = response['list'][0]['definition']
        example = response['list'][0]['example']
        teks = '**Text: {}**\n**Meaning:**\n`{}`\n\n**Example:**\n`{}`'.format(
            replace_text(word),
            replace_text(definition),
            replace_text(example),
        )
        await edit_or_reply(message, text=teks)
        return
    except Exception as e:
        await edit_or_reply(
            message, text='`The Unban Dictionary API could not be reached`',
        )
        print(e)
        await sleep(3)
        await message.delete()
