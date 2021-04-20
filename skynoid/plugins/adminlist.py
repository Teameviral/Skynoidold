import html

from pyrogram import filters

from skynoid import app
from skynoid import COMMAND_PREFIXES
from skynoid import edit_or_reply
from skynoid.languages.strings import tld
from skynoid.utils import capture_err
from skynoid.utils.parser import mention_html
from skynoid.utils.parser import mention_markdown

__MODULE__ = '▲ Admin List ▼'
__HELP__ = """
This module is for checking admins/bots or report someone in a group,
and not for spamming.
Please note that spamming these commands
might lead to annoying admins or even banning you.
──「 **Admin list** 」──
-> `admins`
-> `adminlist`
Get a list of admins in a specific chat or the chat you send it in
──「 **Report admin** 」──
-> `reportadmin`
-> `reportadmins`
Tag all admins in a message
──「 **Bot list** 」──
-> `botlist`
Get a list of bots in a specific chat or the chat you send it in
"""


@app.on_message(
    filters.me &
    filters.command(
        ['admins', 'adminlist'],
        COMMAND_PREFIXES,
    ),
)
@capture_err
async def adminlist(client, message):
    creator = []
    admin = []
    badmin = []
    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
    else:
        chat = message.chat.id
    grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.message_id
    alladmins = client.iter_chat_members(chat, filter='administrators')
    async for a in alladmins:
        try:
            nama = a.user.first_name + ' ' + a.user.last_name
        except BaseException:
            nama = a.user.first_name
        if nama is None:
            nama = '☠️ Deleted Account'
        if a.status == 'administrator':
            if a.user.is_bot:
                badmin.append(mention_markdown(a.user.id, nama))
            else:
                admin.append(mention_markdown(a.user.id, nama))
        elif a.status == 'creator':
            creator.append(mention_markdown(a.user.id, nama))
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    teks = tld('adminlist_one').format(grup.title)
    for x in creator:
        teks += f'│ • {x}\n'
        if len(teks) >= 4096:
            await message.reply(
                message.chat.id,
                teks,
                reply_to_message_id=replyid,
            )
            teks = ''
            toolong = True
    teks += tld('adminlist_two').format(len(admin))
    for x in admin:
        teks += f'│ • {x}\n'
        if len(teks) >= 4096:
            await message.reply(teks)
            teks = ''
            toolong = True
    teks += tld('adminlist_three').format(len(badmin))
    for x in badmin:
        teks += f'│ • {x}\n'
        if len(teks) >= 4096:
            await message.reply(
                message.chat.id,
                teks,
                reply_to_message_id=replyid,
            )
            teks = ''
            toolong = True
    teks += tld('adminlist_four').format(totaladmins)
    if toolong:
        await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await edit_or_reply(message, text=teks)


@app.on_message(filters.me & filters.command('reportadmins', COMMAND_PREFIXES))
async def report_admin(client, message):
    await message.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = None
    grup = await client.get_chat(message.chat.id)
    alladmins = client.iter_chat_members(
        message.chat.id,
        filter='administrators',
    )
    admin = [
        mention_html(a.user.id, '\u200b')
        async for a in alladmins
        if a.status in ['administrator', 'creator'] and not a.user.is_bot
    ]

    if message.reply_to_message:
        if text:
            teks = f'{text}'
        else:
            user = message.reply_to_message.from_user
            teks = tld('reportadmins_one').format(
                mention_html(user.id, user.first_name),
            )
    else:
        if text:
            teks = '{}'.format(html.escape(text))
        else:
            teks = tld('reportadmins_two').format(grup.title)
    teks += ''.join(admin)
    if message.reply_to_message:
        await client.send_message(
            message.chat.id,
            teks,
            reply_to_message_id=message.reply_to_message.message_id,
            parse_mode='html',
        )
    else:
        await client.send_message(message.chat.id, teks, parse_mode='html')


@app.on_message(filters.me & filters.command('tagall', COMMAND_PREFIXES))
async def tag_all_users(client, message):
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = tld('tagall')
    kek = client.iter_chat_members(message.chat.id)
    async for a in kek:
        if not a.user.is_bot:
            text += mention_html(a.user.id, '\u200b')
    if message.reply_to_message:
        await client.send_message(
            message.chat.id,
            text,
            reply_to_message_id=message.reply_to_message.message_id,
            parse_mode='html',
        )
    else:
        await client.send_message(message.chat.id, text, parse_mode='html')
    await message.delete()


@app.on_message(filters.me & filters.command('botlist', COMMAND_PREFIXES))
async def get_list_bots(client, message):
    replyid = None
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
    else:
        chat = message.chat.id
    grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.message_id
    getbots = client.iter_chat_members(chat)
    bots = []
    async for a in getbots:
        try:
            nama = a.user.first_name + ' ' + a.user.last_name
        except BaseException:
            nama = a.user.first_name
        if nama is None:
            nama = tld('botlist_one')
        if a.user.is_bot:
            bots.append(mention_markdown(a.user.id, nama))
    teks = tld('botlist_two').format(grup.title)
    teks += tld('botlist_three')
    for x in bots:
        teks += f'│ • {x}\n'
    teks += tld('botlist_four').format(len(bots))
    if replyid:
        await client.send_message(
            message.chat.id,
            teks,
            reply_to_message_id=replyid,
        )
    else:
        await edit_or_reply(message, text=teks)
