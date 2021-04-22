# Thanks to @Athfan for a Base Plugin.
# Go and Do a star on his repo: https://github.com/athphane/userbot
import time

import timeago
from pyrogram import filters

from skynoid import AdminSettings
from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply

__MODULE__ = '▲ Metrics ▼'
__HELP__ = """
This module can help you do wordcount in the last 1000 messages
in a chat.

──「 **Word Count** 」──
-> `wordcount` or `wc`
Finds the 25 most used words in the last 1000 messages in the chat.

──「 **Inactive Message Count** 」──
-> `msg` or `msg <integer>`
Finds the inactive users according to the last messages in the chat.
"""


class Custom(dict):
    def __missing__(self, key):
        """define missing value"""
        return 0


async def get_inactive(client, message):
    cmd = message.command
    start = time.time()
    limit = int(' '.join(cmd[1:])) if len(cmd) > 1 else 0
    messages = [
        m
        async for member in client.iter_chat_members(
            message.chat.id, limit=limit, filter='recent',
        )
        if not member.user.is_deleted
        async for m in client.search_messages(
            message.chat.id, limit=1, from_user=member.user.id,
        )
    ]

    delta = time.time() - start
    messages.sort(key=lambda k: k['date'])

    return '\n'.join(
        [
            '{} last [message]({}) was {}'.format(
                m.from_user.mention,
                m.link,
                timeago.format(m.date),
            )
            for m in messages
        ]
        + [f'`{int(delta * 1000)}ms`'],
    )


@app.on_message(
    filters.user(AdminSettings) &
    filters.command(
        ['wordcount', 'wc'],
        COMMAND_PREFIXES,
    ),
)
async def word_count(client, message):
    await message.delete()
    words = Custom()
    progress = await client.send_message(
        message.chat.id, '`Processing 1000 messages...`',
    )
    async for ms_g in client.iter_history(message.chat.id, 1000):
        if ms_g.text:
            for word in ms_g.text.split():
                words[word.lower()] += 1
        if ms_g.caption:
            for word in ms_g.caption.split():
                words[word.lower()] += 1
    freq = sorted(words, key=words.get, reverse=True)
    out = 'Word Counter\n'
    for i in range(25):
        out += f'{i + 1}. **{words[freq[i]]}**: {freq[i]}\n'

    await progress.edit_text(out)


@app.on_message(filters.me & filters.command('msg', COMMAND_PREFIXES))
async def inactive_msg(client, message):
    text = await get_inactive(client, message)
    await edit_or_reply(message, text=text)
