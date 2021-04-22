from skynoid.utils.msg_types import Types
from skynoid import DB_AVAILABLE, Owner, setbot
from skynoid.utils.string import parse_button
from skynoid.utils.string import build_keyboard

from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineQueryResultArticle
from pyrogram.types import InputTextMessageContent
from pykeyboard import InlineKeyboard

from pyrogram import errors

import sys
import traceback


if DB_AVAILABLE:
    from skynoid.plugins.database import notes_db


async def note_func(string, client, query, answers):
    if len(string.split()) == 1:
        allnotes = notes_db.get_all_selfnotes_inline(query.from_user.id)
        if not allnotes:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='You dont have any notes!',
                switch_pm_parameter='help_inline',
            )
            return
        rng = min(len(list(allnotes)), 30)
        for x in range(rng):
            note = allnotes[list(allnotes)[x]]
            noteval = note['value']
            notetype = note['type']
            # notefile = note["file"]
            if notetype != Types.TEXT:
                continue
            note, button = parse_button(noteval)
            button = build_keyboard(button)
            answers.append(
                InlineQueryResultArticle(
                    title='Note #{}'.format(list(allnotes)[x]),
                    description=note,
                    input_message_content=InputTextMessageContent(note),
                    reply_markup=InlineKeyboardMarkup(button),
                ),
            )
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text='Yourself notes',
            switch_pm_parameter='help_inline',
        )
        return
    q = string.split(None, 1)
    notetag = q[1]
    noteval = notes_db.get_selfnote(query.from_user.id, notetag)
    if not noteval:
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text='Note not found!',
            switch_pm_parameter='help_inline',
        )
        return
    note, button = parse_button(noteval.get('value'))
    button = build_keyboard(button)
    answers.append(
        InlineQueryResultArticle(
            title=f'Note #{notetag}',
            description=note,
            input_message_content=InputTextMessageContent(note),
            reply_markup=InlineKeyboardMarkup(button),
        ),
    )
    try:
        await client.answer_inline_query(
            query.id,
            results=answers,
            cache_time=5,
        )
    except errors.exceptions.bad_request_400.MessageEmpty:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log_errors = traceback.format_exception(
            etype=exc_type, value=exc_obj, tb=exc_tb,
        )
        button = InlineKeyboard(row_width=1)
        button.add(
            InlineKeyboardButton(
                '🐞 Report bugs',
                callback_data='report_errors',
            ),
        )
        text = 'An error has accured!\n\n```{}```\n'.format(
            ''.join(log_errors),
        )
        await setbot.send_message(Owner, text, reply_markup=button)
