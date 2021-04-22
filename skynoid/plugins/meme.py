import asyncio
import os
import random
import re
import subprocess

import aiohttp
from pyrogram import filters
from pyrogram.raw import functions

import skynoid.plugins.meme_strings as meme_strings
from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply
from skynoid.utils.Pyroutils import ReplyCheck

__MODULE__ = '▲ Memes ▼'
__HELP__ = """
This module can help you generate memes and stylish text.

──「 **Stretch Text** 」──
-> `str`
__stretch text__

──「 **Copy Pasta** 」──
-> `cp`
__add randoms emoji to text__

──「 **Scam** 」──
-> `scam <action>`
__chat input action__

**scame types**:
`typing` `upload_photo`
`record_video` `upload_video`
`record_audio` `upload_audio`
`upload_document` `find_location`
`record_video_note` `upload_video_note`
`playing`

──「 **Mock text** 」──
-> `mocktxt`
__mock someone with text__

──「 **Vaporwave/Aestethic** 」──
-> `aes`
__convert your text to vaporwave__

──「 **Spam** 」──
-> `spam` (times) (phrase)
__spams a phrase multiple times__

-> `spamstk` (times)
__reply a sticker to spam it__

──「 **Shrugs** 」──
-> `shg`
__free shrugs?__

──「 **Pat** 」──
-> `pat`
__pat gifs__

——「 **The F Sign** 」──
-> `f`
__press **f** to show some respect__

──「 **Fake Screenshot** 」──
-> `fakess`
__fake screenshot notification toasts__
"""


async def mocking_text(text):
    teks = list(text)
    for i, ele in enumerate(teks):
        teks[i] = ele.upper() if i % 2 != 0 else ele.lower()
    return ''.join(teks)


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('pat', COMMAND_PREFIXES),
)
async def pat(client, message):
    async with aiohttp.ClientSession() as session:
        URL = 'https://some-random-api.ml/animu/pat'
        async with session.get(URL) as request:
            if request.status == 404:
                return await edit_or_reply(
                    message,
                    text='**no Pats for u :c**',
                )
            result = await request.json()
            url = result.get('link', None)
            await message.delete()
            await client.send_video(
                message.chat.id, url, reply_to_message_id=ReplyCheck(message),
            )


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('scam', COMMAND_PREFIXES),
)
async def scam(client, message):
    input_str = message.command
    if len(input_str) == 1:
        scam_action = random.choice(meme_strings.options)
        scam_time = random.randint(30, 60)
    # User decides time/action, bot decides the other.
    elif len(input_str) == 2:
        try:
            scam_action = str(input_str[1]).lower()
            scam_time = random.randint(30, 60)
        except ValueError:
            scam_action = random.choice(meme_strings.options)
            scam_time = int(input_str[1])
    elif len(input_str) == 3:  # User decides both action and time
        scam_action = str(input_str[1]).lower()
        scam_time = int(input_str[2])
    else:
        await edit_or_reply(message, text='**Invalid Syntax!**')
        return
    try:
        if scam_time > 0:
            chat_id = message.chat.id
            await message.delete()
            count = 0
            while count <= scam_time:
                await client.send_chat_action(chat_id, scam_action)
                await asyncio.sleep(5)
                count += 5
    except Exception:
        return


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('shg', COMMAND_PREFIXES),
)
async def shg(_, message):
    await edit_or_reply(message, text=random.choice(meme_strings.shgs))


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('spam', COMMAND_PREFIXES),
)
async def spam(client, message):
    await message.delete()
    times = message.command[1]
    to_spam = ' '.join(message.command[2:])
    if message.chat.type in ['supergroup', 'group']:
        for _ in range(int(times)):
            await client.send_message(
                message.chat.id,
                to_spam,
                reply_to_message_id=ReplyCheck(message),
            )
            await asyncio.sleep(0.20)

    if message.chat.type == 'private':
        for _ in range(int(times)):
            await client.send_message(message.chat.id, to_spam)
            await asyncio.sleep(0.20)


@app.on_message(
    filters.user(AdminSettings) & filters.command('spamstk', COMMAND_PREFIXES),
)
async def spam_stick(client, message):
    if not message.reply_to_message:
        await edit_or_reply(
            message,
            text='**Reply to a sticker with the amount.**',
        )
        return
    if not message.reply_to_message.sticker:
        await edit_or_reply(
            message,
            text='**Reply to a sticker with the amount.**',
        )
        return
    else:
        times = message.command[1]
        if message.chat.type in ['supergroup', 'group']:
            for _ in range(int(times)):
                await client.send_sticker(
                    message.chat.id,
                    sticker=message.reply_to_message.sticker.file_id,
                    reply_to_message_id=ReplyCheck(message),
                )
                await asyncio.sleep(0.20)

        if message.chat.type == 'private':
            for _ in range(int(times)):
                await client.send_message(
                    message.chat.id,
                    sticker=message.reply_to_message.sticker.file_id,
                )
                await asyncio.sleep(0.20)


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('owo', COMMAND_PREFIXES),
)
async def owo(_, message):
    cmd = message.command
    text = ''
    if len(cmd) > 1:
        text = ' '.join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        text = message.reply_to_message.text
    elif len(cmd) == 1:
        await edit_or_reply(message, text='**cant uwu the void.**')
        await asyncio.sleep(2)
        await message.delete()
        return
    reply_text = re.sub(r'[rl]', 'w', text)
    reply_text = re.sub(r'[ｒｌ]', 'ｗ', text)
    reply_text = re.sub(r'[RL]', 'W', reply_text)
    reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
    reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
    reply_text = re.sub(r'r([aeiouａｅｉｏｕ])', r'w\1', reply_text)
    reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
    reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
    reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
    reply_text = re.sub(
        r'\!+', ' ' + random.choice(meme_strings.faces),
        reply_text,
    )
    reply_text = re.sub(
        r'！+', ' ' + random.choice(meme_strings.faces),
        reply_text,
    )
    reply_text = reply_text.replace('ove', 'uv')
    reply_text = reply_text.replace('ｏｖｅ', 'ｕｖ')
    reply_text += ' ' + random.choice(meme_strings.faces)
    await edit_or_reply(message, text=reply_text)


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('str', COMMAND_PREFIXES),
)
async def stretch(_, message):
    cmd = message.command
    stretch_text = ''
    if len(cmd) > 1:
        stretch_text = ' '.join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        stretch_text = message.reply_to_message.text
    elif len(cmd) == 1:
        await edit_or_reply(
            message,
            text='`Giiiiiiiv sooooooomeeeeeee teeeeeeext!`',
        )
        await asyncio.sleep(2)
        await message.delete()
        return
    count = random.randint(3, 10)
    reply_text = re.sub(
        r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])', (r'\1' * count), stretch_text,
    )
    await edit_or_reply(message, text=reply_text)


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('cp', COMMAND_PREFIXES),
)
async def haha_emojis(_, message):
    if not message.reply_to_message.message_id:
        return

    teks = message.reply_to_message.text
    reply_text = random.choice(meme_strings.emojis)
    b_char = random.choice(teks).lower()
    for c in teks:
        if c == ' ':
            reply_text += random.choice(meme_strings.emojis)
        elif c in meme_strings.emojis:
            reply_text += c
            reply_text += random.choice(meme_strings.emojis)
        elif c.lower() == b_char:
            reply_text += '🅱️'
        else:
            reply_text += c.upper() if bool(
                random.getrandbits(1),
            ) else c.lower()
    reply_text += random.choice(meme_strings.emojis)
    await edit_or_reply(message, text=reply_text)


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('mocktxt', COMMAND_PREFIXES),
)
async def mock_text(_, message):
    if message.reply_to_message:
        teks = message.reply_to_message.text
        if teks is None:
            teks = message.reply_to_message.caption
        if teks is None:
            return
        await message.edit(await mocking_text(teks))


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('fakess', COMMAND_PREFIXES),
)
async def fake_ss(client, message):
    await asyncio.gather(
        message.delete(),
        client.send(
            functions.messages.SendScreenshotNotification(
                peer=await client.resolve_peer(message.chat.id),
                reply_to_msg_id=0,
                random_id=client.rnd_id(),
            ),
        ),
    )


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('g', COMMAND_PREFIXES),
)
async def glitch(client, message):
    cmd = message.command
    amount = ''
    if len(cmd) > 1:
        amount = ' '.join(cmd[1:])
    elif len(cmd) == 1:
        amount = '2'
    profile_photo = 'skynoid/downloads/pfp.jpg'
    glitched_gif = 'skynoid/downloads/glitched_pfp.gif'
    replied = message.reply_to_message
    if not replied:
        await message.delete()
        return
    user = await client.get_users(replied.from_user.id)
    await client.download_media(
        user.photo.big_file_id,
        file_name=profile_photo,
    )
    subprocess.run(
        ['glitch_this', profile_photo, f'{amount}', '--gif'],
        capture_output=True,
        text=True,
    )
    await client.send_animation(
        message.chat.id, glitched_gif, reply_to_message_id=ReplyCheck(message),
    )
    await message.delete()
    os.remove(profile_photo)
    os.remove(glitched_gif)
