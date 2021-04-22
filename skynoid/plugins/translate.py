from gpytranslate import Translator
from pyrogram import filters

from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply

trl = Translator()

__MODULE__ = 'Translate'
__HELP__ = """
Translate some text by give a text or reply that text/caption.
Translate by Google Translate

──「 **Translate** 」──
-> `tr (lang) (*text)`
Give a target language and text as args for translate to that target.
Reply a message to translate that.

* = Not used when reply a message!
"""


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('tr', COMMAND_PREFIXES),
)
async def translate(_, message):
    trl = Translator()
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        if len(message.text.split()) == 1:
            await message.delete()
            return
        target = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await edit_or_reply(
                message, text=f'Error: `{str(err)}`', parse_mode='Markdown',
            )
            return
    else:
        if len(message.text.split()) <= 2:
            await message.delete()
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await edit_or_reply(
                message,
                text='Error: `{}`'.format(
                    str(err),
                ),
                parse_mode='Markdown',
            )
            return

    await edit_or_reply(
        message,
        text='**Translated:**\n```{}```\n\n**Detected Language:** `{}`'.format(
            tekstr.text,
            (await trl.detect(text)),
        ),
        parse_mode='Markdown',
    )
