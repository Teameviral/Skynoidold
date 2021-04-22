from pyrogram import errors
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup

from skynoid import app
from skynoid import BotUsername
from skynoid import COMMAND_PREFIXES
from skynoid import DB_AVAILABLE
from skynoid import edit_or_reply
from skynoid import Owner
from skynoid import setbot
from skynoid.utils.msg_types import get_note_type
from skynoid.utils.msg_types import Types
from skynoid.utils.Pyroutils import ReplyCheck
from skynoid.utils.string import build_keyboard
from skynoid.utils.string import parse_button

if DB_AVAILABLE:
    from skynoid.plugins.database import notes_db as db

# TODO: Add buttons support in some types
# TODO: Add group notes, but whats for? since only you can get notes

__MODULE__ = '▲ Notes ▼'
__HELP__ = """
Save a note, get it or delete it.
This is available only for yourself only!
Also notes support inlines button powered by inline query assistant bot.

──「 **Saving Notes** 」──
-> `save (note)`
Save a note, you can get or delete that later.

──「 **Getting Notes** 」──
-> `get (note)`
Get the provided note, if saved.

──「 **Deleting Notes** 」──
-> `clear (note)`
Delete the provided note, if saved.

──「 **All Notes** 」──
-> `saved`
-> `notes`
See all of your saved notes.

── **Note Format** ──
-> **Button**
`[Button Text](buttonurl:google.com)`
-> **Bold**
`**Bold**`
-> __Italic__
`__Italic__`
-> `Code`
`Code` (grave accent)
"""

GET_FORMAT = {
    Types.TEXT.value: app.send_message,
    Types.DOCUMENT.value: app.send_document,
    Types.PHOTO.value: app.send_photo,
    Types.VIDEO.value: app.send_video,
    Types.STICKER.value: app.send_sticker,
    Types.AUDIO.value: app.send_audio,
    Types.VOICE.value: app.send_voice,
    Types.VIDEO_NOTE.value: app.send_video_note,
    Types.ANIMATION.value: app.send_animation,
    Types.ANIMATED_STICKER.value: app.send_sticker,
    Types.CONTACT: app.send_contact,
}


@app.on_message(
    filters.user(Owner) &
    filters.command('save', COMMAND_PREFIXES),
)
async def save_note(_, message):
    if not DB_AVAILABLE:
        await message.edit("You haven't set up a database!")
        return
    note_name, text, data_type, content = get_note_type(message)

    if not note_name:
        await message.edit(
            '```'
            + message.text +
            '```\n\nError: you must provide a name for the note!',
        )
        return

    if data_type == Types.TEXT:
        teks, _ = parse_button(text)
        if not teks:
            await message.edit(
                '```'
                + message.text
                + "```\n\nError: the note doesn't have enough content!",
            )
            return

    db.save_selfnote(message.from_user.id, note_name, text, data_type, content)
    await message.edit(f'Saved note `{note_name}`!')


@app.on_message(filters.user(Owner) & filters.command('get', COMMAND_PREFIXES))
async def get_note(client, message):
    if not DB_AVAILABLE:
        await message.edit("You haven't set up a database!")
        return
    if len(message.text.split()) >= 2:
        note = message.text.split()[1]
    else:
        await message.edit('Give me a note tag!')

    getnotes = db.get_selfnote(message.from_user.id, note)
    if not getnotes:
        await message.edit('This note does not exist!')
        return

    if getnotes['type'] == Types.TEXT:
        teks, button = parse_button(getnotes.get('value'))
        button = build_keyboard(button)
        button = InlineKeyboardMarkup(button) if button else None
        if button:
            try:
                inlineresult = await app.get_inline_bot_results(
                    f'@{BotUsername}', f'note {note}',
                )
            except errors.exceptions.bad_request_400.BotInlineDisabled:
                await message.edit(
                    "Your haven't enabled inline for yout bot!",
                )
                await setbot.send_message(
                    Owner,
                    'Hello, looks like a note of yours include a button,'
                    "but I can't display it "
                    'because **inline mode** is not enabled in @BotFather.',
                )
                return
            try:
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
            except IndexError:
                await message.edit(
                    'An error occured!'
                    'Check your assistant for more information!',
                )
                return
        else:
            await message.edit(teks)
    elif getnotes['type'] in (
        Types.STICKER,
        Types.VOICE,
        Types.VIDEO_NOTE,
        Types.CONTACT,
        Types.ANIMATED_STICKER,
    ):
        await message.delete()
        await GET_FORMAT[getnotes['type']](
            message.chat.id, getnotes['file'],
            reply_to_message_id=ReplyCheck(message),
        )
    else:
        if getnotes.get('value'):
            teks, button = parse_button(getnotes.get('value'))
            button = build_keyboard(button)
            button = InlineKeyboardMarkup(button) if button else None
        else:
            teks = None
            button = None
        if button:
            try:
                inlineresult = await app.get_inline_bot_results(
                    f'@{BotUsername}', f'note {note}',
                )
            except errors.exceptions.bad_request_400.BotInlineDisabled:
                await message.edit(
                    "Your haven't enabled inline for yout bot!",
                )
                await setbot.send_message(
                    Owner,
                    'Hello, looks like a note of yours include a button,'
                    "but I can't display it "
                    'because **inline mode** is not enabled in @BotFather.',
                )
                return
            try:
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message),
                )
            except IndexError:
                message.edit(
                    'An error occured!',
                )
                return
        else:
            await GET_FORMAT[getnotes['type']](
                message.chat.id,
                getnotes['file'],
                caption=teks,
                reply_to_message_id=ReplyCheck(message),
            )


@app.on_message(
    filters.user(Owner) & filters.command(
        ['notes', 'saved'], COMMAND_PREFIXES,
    ),
)
async def local_notes(_, message):
    if not DB_AVAILABLE:
        await message.edit("You haven't set up a database!")
        return
    getnotes = db.get_all_selfnotes(message.from_user.id)
    if not getnotes:
        await message.edit('There are no notes in local notes!')
        return
    rply = '**Local Botes:**\n'
    for x in getnotes:
        if len(rply) >= 1800:
            await edit_or_reply(message, text=rply)
            rply = '**Local Botes:**\n'
        rply += f'- `{x}`\n'

    await message.edit(rply)


@app.on_message(
    filters.user(Owner) &
    filters.command('clear', COMMAND_PREFIXES),
)
async def clear_note(_, message):
    if not DB_AVAILABLE:
        await message.edit("You haven't set up a database!")
        return
    if len(message.text.split()) <= 1:
        await message.edit('What do you want to clear?')
        return

    note = message.text.split()[1]
    getnote = db.rm_selfnote(message.from_user.id, note)
    if not getnote:
        await message.edit('This note does not exist!')
        return

    await message.edit(f'Deleted note `{note}`!')
