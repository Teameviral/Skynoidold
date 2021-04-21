import asyncio
import random
import re
from time import time

from coffeehouse.api import API
from coffeehouse.exception import CoffeeHouseError as CFError
from coffeehouse.lydia import LydiaAI
from pyrogram import filters

import nana.plugins.meme_strings as meme_strings
from nana import AdminSettings
from nana import BotID
from nana import BotUsername
from nana import LYDIA_API
from nana import Owner
from nana import setbot
from nana.utils import filt
from nana.plugins.assistant.database import lydia_db as sql

CoffeeHouseAPI = API(LYDIA_API)
api_ = LydiaAI(CoffeeHouseAPI)


@setbot.on_message(filters.user(AdminSettings) & filt.command(['addchat']))
async def add_chat(_, message):
    global api_
    chat_id = message.chat.id
    is_chat = sql.is_chat(chat_id)
    if not is_chat:
        ses = api_.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        sql.set_ses(chat_id, ses_id, expires)
        await message.reply('AI successfully enabled for this chat!')
    else:
        await message.reply('AI is already enabled for this chat!')


@setbot.on_message(filters.user(AdminSettings) & filt.command(['rmchat']))
async def remove_chat(_, message):
    chat_id = message.chat.id
    is_chat = sql.is_chat(chat_id)
    if not is_chat:
        await message.reply("AI isn't enabled here in the first place!")
    else:
        sql.rem_chat(chat_id)
        await message.reply('AI disabled successfully!')


@setbot.on_message(
    ~filters.me & ~filters.edited & (filters.group | filters.private), group=2,
)
async def chat_bot(client, message):
    global api_
    chat_id = message.chat.id
    is_chat = sql.is_chat(chat_id)
    if not is_chat:
        return
    if message.text and not message.document:
        if not await check_message(client, message):
            return
        sesh, exp = sql.get_ses(chat_id)
        query = message.text
        try:
            if int(exp) < time():
                ses = api_.create_session()
                ses_id = str(ses.id)
                expires = str(ses.expires)
                sql.set_ses(chat_id, ses_id, expires)
                sesh, exp = sql.get_ses(chat_id)
        except ValueError:
            pass
        try:
            await client.send_chat_action(chat_id, action='typing')
            rep = api_.think_thought(sesh, query)
            reply_text = re.sub(r'[rl]', 'w', rep)
            reply_text = re.sub(r'[ｒｌ]', 'ｗ', rep)
            reply_text = re.sub(r'[RL]', 'W', reply_text)
            reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
            reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
            reply_text = re.sub(r'r([aeiouａｅｉｏｕ])', r'w\1', reply_text)
            reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
            reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
            reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
            reply_text = re.sub(
                r'\!+', ' ' + random.choice(meme_strings.faces), reply_text,
            )
            reply_text = re.sub(
                r'！+', ' ' + random.choice(meme_strings.faces), reply_text,
            )
            reply_text = reply_text.replace('ove', 'uv')
            reply_text = reply_text.replace('ｏｖｅ', 'ｕｖ')
            reply_text = reply_text.replace('.', ',,.')
            reply_text += ' ' + random.choice(meme_strings.faces)
            await asyncio.sleep(0.3)
            await message.reply_text(reply_text.lower(), quote=True)
        except CFError as e:
            await client.send_message(
                Owner, f'Chatbot error: {e} occurred in {chat_id}!',
            )


async def check_message(_, message):
    reply_msg = message.reply_to_message
    if message.text.lower() == f'{BotUsername}':
        return True
    if reply_msg:
        if reply_msg.from_user.id == BotID:
            return True
    else:
        return False
