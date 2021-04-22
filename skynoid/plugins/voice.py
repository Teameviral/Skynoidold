import asyncio
import os
from datetime import datetime

from aiohttp import BasicAuth
from aiohttp import ClientSession
from gtts import gTTS
from pyrogram import filters

from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply
from skynoid import IBM_WATSON_CRED_PASSWORD
from skynoid import IBM_WATSON_CRED_URL
from skynoid.plugins.downloads import download_reply_nocall

__MODULE__ = '
TTS / STT'
__HELP__ = """
Convert text to voice chat.

──「 **Text-To-Speech** 」──
-> `tts (text)`
Convert text to voice by google

──「 **Voice Language** 」──
-> `voicelang (lang_id)`
Set language of your voice, Some Available Voice lang:
`ID| Language  | ID| Language`
`af: Afrikaans | ar: Arabic
cs: Czech     | de: German
el: Greek     | en: English
es: Spanish   | fr: French
hi: Hindi     | id: Indonesian
is: Icelandic | it: Italian
ja: Japanese  | jw: Javanese
ko: Korean    | la: Latin
my: Myanmar   | ne: Nepali
nl: Dutch     | pt: Portuguese
ru: Russian   | su: Sundanese
sv: Swedish   | th: Thai
tl: Filipino  | tr: Turkish
vi: Vietname  |
zh-cn: Chinese (Mandarin/China)
zh-tw: Chinese (Mandarin/Taiwan)`

──「 **Speech-To-Text** 」──
-> `stt`
Reply to a voice message to output trascript
"""

lang = 'en'  # Default Language for voice


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('tts', COMMAND_PREFIXES),
)
async def voice(client, message):
    global lang
    cmd = message.command
    if len(cmd) > 1:
        v_text = ' '.join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        v_text = message.reply_to_message.text
    elif len(cmd) == 1:
        await edit_or_reply(
            message,
            text='Usage: `reply to a message or pass args`',
        )
        await asyncio.sleep(2)
        await message.delete()
        return
    await client.send_chat_action(message.chat.id, 'record_audio')
    # noinspection PyUnboundLocalVariable
    tts = gTTS(v_text, lang=lang)
    tts.save('skynoid/cache/voice.ogg')
    await message.delete()
    if message.reply_to_message:
        await client.send_voice(
            message.chat.id,
            voice='skynoid/cache/voice.ogg',
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_voice(message.chat.id, voice='skynoid/cache/voice.ogg')
    await client.send_chat_action(message.chat.id, action='cancel')
    os.remove('skynoid/cache/voice.ogg')


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('voicelang', COMMAND_PREFIXES),
)
async def voicelang(_, message):
    global lang
    lang = message.text.split(None, 1)[1]
    gTTS('tes', lang=lang)
    await edit_or_reply(
        message,
        text=f'Language Set to {lang}',
    )


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('stt', COMMAND_PREFIXES),
)
async def speach_to_text(client, message):
    start = datetime.now()
    input_str = message.reply_to_message.voice
    if input_str:
        required_file_name = await download_reply_nocall(client, message)
        if IBM_WATSON_CRED_URL is None or IBM_WATSON_CRED_PASSWORD is None:
            await edit_or_reply(
                message, text='`no ibm watson key provided, aborting...`',
            )
            await asyncio.sleep(3)
            await message.delete()
        else:
            headers = {
                'Content-Type': message.reply_to_message.voice.mime_type,
            }
            with open(required_file_name, 'rb') as f:
                data = f.read()
            r = await parse_response(headers, data)
            if 'results' in r:
                results = r['results']
                transcript_response = ''
                transcript_confidence = ''
                for alternative in results:
                    alternatives = alternative['alternatives'][0]
                    transcript_response += ' ' + str(
                        alternatives['transcript'],
                    )
                    transcript_confidence += ' ' + str(
                        alternatives['confidence'],
                    )
                end = datetime.now()
                ms = (end - start).seconds
                if transcript_response != '':
                    string_to_show = f"""
<b>TRANSCRIPT</b>:
<pre>{transcript_response}<pre>

<b>Time Taken</b>: <pre>{ms} seconds<pre>
<b>Confidence</b>: <pre>{transcript_confidence}<pre>
"""
                else:
                    string_to_show = '<pre>No Results Found<pre>'
                await edit_or_reply(
                    message,
                    text=string_to_show,
                    parse_mode='html',
                )
            else:
                await edit_or_reply(message, text=r['error'])
            os.remove(required_file_name)
    else:
        await edit_or_reply(message, text='`Reply to a voice message`')
        await asyncio.sleep(3)
        await message.delete()


async def parse_response(headers, data):
    """[IBM VOICE PARSER]

    Args:
        headers ([mimetype]): [voice file mimetype]
        data ([file]): [the voice file]

    Returns:
        [text]: [the speach to text response]
    """
    async with ClientSession(headers=headers) as ses:
        async with ses.post(
            IBM_WATSON_CRED_URL + '/v1/recognize',
            data=data,
            auth=BasicAuth(
                'apikey',
                IBM_WATSON_CRED_PASSWORD,
            ),
        ) as resp:
            return await resp.json()
