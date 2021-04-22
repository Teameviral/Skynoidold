from datetime import datetime

from pyrogram import filters
from pytz import timezone

from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply
from skynoid import time_country

__MODULE__ = 'Time'
__HELP__ = """
Modules that helps a user to get date and time
here are the timezone list:
[link](https://telegra.ph/Time-Zone-list-for-Nana-Remix-07-21)

──「 **Time and Date** 」──
-> `time`
Returns the Date and Time for a selected country

"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('time', COMMAND_PREFIXES),
)
async def grabTime(_, message):
    if not time_country:
        await message.delete()
        return
    tz = time_country.replace('_', ' ')
    tzDateTime = datetime.now(timezone(tz))
    date = tzDateTime.strftime(r'%d %b, %y')
    militaryTime = tzDateTime.strftime('%H:%M')
    time = datetime.strptime(militaryTime, '%H:%M').strftime('%I:%M %p')
    time_string = (
        'Currently it is'
        + f' **{time}** '
        + 'on'
        + f' **{date}** '
        + 'in '
        + f'**{tz}**'
    )
    await edit_or_reply(message, text=time_string)
