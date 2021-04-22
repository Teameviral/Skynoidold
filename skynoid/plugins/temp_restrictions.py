from skynoid import AdminSettings, COMMAND_PREFIXES, edit_or_reply, app
from pyrogram import filters, errors
from pyrogram.types import ChatPermissions
from skynoid.utils.capture_errors import capture_err
from skynoid.utils.string import extract_time
from skynoid.utils.parser import user_time_and_reason, time_parser_int
from skynoid.languages.strings import tld


import time


__MODULE__ = 'Temp-Restrict'
__HELP__ = """
Temporarily Restrict Users (Requires Admin Rights)

──「 **Temporary Ban** 」──
-> `tban`
Temporarily ban a user with given time: `tban @username 69m`

"""


@app.on_message(
    filters.command('tmute', COMMAND_PREFIXES)
    & filters.user(AdminSettings),
)
@capture_err
async def tempmute(client, message):
    if message.chat.type == 'private':
        await message.delete()
        return
    if not message.reply_to_message and len(message.command) == 1:
        await edit_or_reply(
            message,
            text='You must reply to a user, or pass a username/user_id',
        )
        return

    if not message.reply_to_message and len(message.command) == 2:
        await edit_or_reply(
            message,
            text='@Eviral please fix this string asap.',
        )
        return

    user_id, set_time, reason = await user_time_and_reason(message)
    parsed_time = extract_time(set_time)
    reas = parsed_time - int(time.time())
    if not parsed_time:
        await edit_or_reply(message, text='Invalid Time')
        return

    try:
        await client.restrict_chat_member(
            message.chat.id,
            user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=parsed_time,
        )
    except errors.ChatAdminRequired:
        await edit_or_reply(message, text=tld('denied_permission'))
        return

    # Must send a sticker
    await edit_or_reply(
        message,
        text='**Temporary muted** for {time}'.format(
            time=time_parser_int(reas),
        ) + '\nReason: ' + reason if reason else '',
    )


@app.on_message(
    filters.command('tban', COMMAND_PREFIXES)
    & filters.user(AdminSettings),
)
@capture_err
async def temp_ban(_, message):
    if not message.reply_to_message and len(message.command) == 1:
        await edit_or_reply(
            message,
            text='Reply to a user, or pass username/user_id',
        )
        return

    if not message.reply_to_message and len(message.command) == 2:
        await edit_or_reply(
            message,
            text='`@Eviral please fix this string`',
        )
        return

    user_id, set_time, _ = await user_time_and_reason(message)
    parsed_time = extract_time(set_time)
    if not parsed_time:
        await edit_or_reply(message, text='`Parsed time is wrong.`')
        return

    try:
        await app.kick_chat_member(message.chat.id, user_id, parsed_time)
    except errors.ChatAdminRequired:
        await edit_or_reply(message, text=tld('denied_permission'))
        return
