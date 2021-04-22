from datetime import datetime

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.raw import functions
from pyrogram.types import User

from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply

__MODULE__ = '▲ Whois ▼'
__HELP__ = """
──「 **Whois** 」──
-> `info` `@username`, `user_id` or reply
To get information about someone.
"""


def LastOnline(user: User):
    if user.is_bot:
        return ''
    elif user.status == 'recently':
        return 'Recently'
    elif user.status == 'within_week':
        return 'Within the last week'
    elif user.status == 'within_month':
        return 'Within the last month'
    elif user.status == 'long_time_ago':
        return 'A long time ago :('
    elif user.status == 'online':
        return 'Currently Online'
    elif user.status == 'offline':
        return datetime.fromtimestamp(user.status.date).strftime(
            '%a, %d %b %Y, %H:%M:%S',
        )


async def GetCommon(client, get_user):
    common = await client.send(
        functions.messages.GetCommonChats(
            user_id=await client.resolve_peer(get_user),
            max_id=0,
            limit=0,
        ),
    )
    return common


def ProfilePicUpdate(user_pic):
    return datetime.fromtimestamp(
        user_pic[0].date,
    ).strftime('%d.%m.%Y, %H:%M:%S')


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('info', COMMAND_PREFIXES),
)
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        if message.reply_to_message.forward_from:
            get_user = message.reply_to_message.forward_from.id
        else:
            get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        info = await app.get_users(get_user)
    except PeerIdInvalid:
        await message.delete()
        return
    user_info = await parse_info(client, info)
    await edit_or_reply(message, text=user_info)


async def parse_info(client, info):
    user_info = '╒═══「 ✨ **User Info** 」\n'
    user_info += f'│ • **First Name:** {info.mention}\n'
    if info.last_name:
        user_info += f'│ • **Last Name:** {info.last_name}\n'
    if info.dc_id:
        user_info += f'│ • **DC:** `{info.dc_id}`\n'
    
    if info.username:
        user_info += f'│ • **Username:** @{info.username}\n'
    if not info.is_self:
        user_info += '│ • **Last Online:** `{}`\n'.format(LastOnline(info))
        user_info += '│ • **Common Chats:** `{}`\n'.format(
            len(
                (
                    await GetCommon(
                        client, info.id,
                    )
                ).chats,
            ),
        )
    user_info += f'╘══「 **ID:** `{info.id}` 」'
    return user_info
