import asyncio

from pyrogram import filters

from nana import AdminSettings
from nana import app
from nana import COMMAND_PREFIXES
from nana import edit_or_reply
from nana.utils.aiohttp_helper import AioHttp

__MODULE__ = 'Covid'
__HELP__ = """
Get stats of COVID 19.

──「 **Info Covid** 」──
-> `covid - for global stats`
-> `covid (country) - for a specific country's stats`
"""


@app.on_message(
    filters.user(AdminSettings) & filters.command('covid', COMMAND_PREFIXES),
)
async def corona(_, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        try:
            r = await AioHttp().get_json('https://corona.lmao.ninja/v2/all')
            reply_text = f"""**COVID-19 in the world 🦠:**
 - **Cases:** `{r['cases']:,}`
 - **Cases Today:** `{r['todayCases']:,}`
 - **Deaths:** `{r['deaths']:,}`
 - **Deaths Today:** `{r['todayDeaths']:,}`
 - **Recovered:** `{r['recovered']:,}`
 - **Active:** `{r['active']:,}`
 - **Critical:** `{r['critical']:,}`
 - **Cases/Mil:** `{r['casesPerOneMillion']}`
 - **Deaths/Mil:** `{r['deathsPerOneMillion']}``
"""
            await edit_or_reply(message, text=f'{reply_text}')
            return
        except Exception as e:
            await edit_or_reply(
                message,
                text="`Couldn't reach the API.`",
            )
            print(e)
            await asyncio.sleep(3)
            await message.delete()
            return
    country = args[1]
    r = await AioHttp().get_json(
        f'https://corona.lmao.ninja/v2/countries/{country}',
    )
    if 'cases' not in r:
        await edit_or_reply(
            message,
            text='`The country could not be found!`',
        )
        await asyncio.sleep(3)
        await message.delete()
    else:
        try:
            reply_text = f"""**COVID-19 in {r['country']} 🦠:**
 - **Cases:** `{r['cases']:,}`
 - **Cases Today:** `{r['todayCases']:,}`
 - **Deaths:** `{r['deaths']:,}`
 - **Deaths Today:** `{r['todayDeaths']:,}`
 - **Recovered:** `{r['recovered']:,}`
 - **Active:** `{r['active']:,}`
 - **Critical:** `{r['critical']:,}`
 - **Cases/Mil:** `{r['casesPerOneMillion']}`
 - **Deaths/Mil:** `{r['deathsPerOneMillion']}`
"""
            await edit_or_reply(message, text=reply_text)
        except Exception as e:
            await edit_or_reply(
                message,
                text="`Couldn't reach the API.`",
            )
            print(e)
            await asyncio.sleep(3)
            await message.delete()
