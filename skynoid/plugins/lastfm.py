from pyrogram import filters

from nana import AdminSettings
from nana import app
from nana import COMMAND_PREFIXES
from nana.utils.Pyroutils import ReplyCheck

__HELP__ = """
──「 **LastFM** 」──
-> `lastfm` or `lf`
Share what you're listening to.

Note: you need to set you username in @lastfmrobot.
"""
__MODULE__ = 'Last.FM'


@app.on_message(
    filters.user(AdminSettings) &
    filters.command(['lastfm', 'lf'], COMMAND_PREFIXES),
)
async def lastfm(client, message):
    x = await client.get_inline_bot_results('lastfmrobot', '')
    await message.delete()
    await message.reply_inline_bot_result(
        x.query_id,
        x.results[0].id,
        reply_to_message_id=ReplyCheck(message),
        hide_via=True,
    )
