# dashezup inspired
import os
from pytgcalls import GroupCall
import ffmpeg

from pyrogram import filters

from skynoid import app, edit_or_reply, AdminSettings, COMMAND_PREFIXES

VOICE_CHATS = {}
DEFAULT_DOWNLOAD_DIR = 'skynoid/downloads/'

__MODULE__ = '▲ Radio ▼'
__HELP__ = """
──「 **Radio (BETA)** 」──
-> `play`
Reply to an audio file to play in the Group Voice Chat

-> `stopvc`
to stop playing audio in a group Chat

-> `joinvc`
to Join a voice Chat

-> `leavevc`
to Leave a voice Chat


**Note:**
You might face issues with not playing the audio on time or having delay.
since pytgcalls is still on it's early stage
"""


@app.on_message(
    filters.user(AdminSettings)
    & filters.command('play', COMMAND_PREFIXES),
)
async def play_track(client, message):
    if not message.reply_to_message or not message.reply_to_message.audio:
        return
    input_filename = os.path.join(
        client.workdir, DEFAULT_DOWNLOAD_DIR,
        'input.raw',
    )
    audio = message.reply_to_message.audio
    audio_original = await message.reply_to_message.download()
    await edit_or_reply(message, text='Transcoding...')
    ffmpeg.input(audio_original).output(
        input_filename,
        format='s16le',
        acodec='pcm_s16le',
        ac=2, ar='48k',
    ).overwrite_output().run()
    os.remove(audio_original)
    if VOICE_CHATS and message.chat.id in VOICE_CHATS:
        text = f'Playing **{audio.title}**...'
    else:
        try:
            group_call = GroupCall(client, input_filename)
            await group_call.start(message.chat.id, False)
        except RuntimeError:
            await edit_or_reply(message, text='Group Call doesnt exist')
            return
        VOICE_CHATS[message.chat.id] = group_call
    await edit_or_reply(message, text=text)


@app.on_message(
    filters.user(AdminSettings)
    & filters.command('stopvc', COMMAND_PREFIXES),
)
async def stop_playing(_, message):
    group_call = VOICE_CHATS[message.chat.id]
    group_call.stop_playout()
    os.remove('skynoid/downloads/input.raw')
    await edit_or_reply(
        message,
        text='Stopped Playing...',
    )


@app.on_message(
    filters.user(AdminSettings)
    & filters.command('joinvc', COMMAND_PREFIXES),
)
async def join_voice_chat(client, message):
    input_filename = os.path.join(
        client.workdir, DEFAULT_DOWNLOAD_DIR,
        'input.raw',
    )
    if message.chat.id in VOICE_CHATS:
        await edit_or_reply(message, text='Already joined to Voice Chat')
        return
    chat_id = message.chat.id
    try:
        group_call = GroupCall(client, input_filename)
        await group_call.start(chat_id, False)
    except RuntimeError:
        await edit_or_reply(
            message,
            text='@Eviral please update the strings',
        )
        return
    VOICE_CHATS[chat_id] = group_call
    await edit_or_reply(
        message,
        text='Joined the Voice Chat',
    )


@app.on_message(
    filters.user(AdminSettings) & filters.command('leavevc', COMMAND_PREFIXES),
)
async def leave_voice_chat(client, message):
    chat_id = message.chat.id
    group_call = VOICE_CHATS[chat_id]
    await group_call.stop()
    VOICE_CHATS.pop(chat_id, None)
    await edit_or_reply(
        message,
        text='Left Voice Chat',
    )
