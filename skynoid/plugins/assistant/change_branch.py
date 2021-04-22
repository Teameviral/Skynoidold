import re
from asyncio import create_subprocess_exec
from asyncio import sleep

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup

from skynoid import SKYNOID_IMG
from skynoid import setbot
from skynoid.__main__ import restart_all
from skynoid.utils.dynamic_filt import dynamic_data_filter


try:
    repo = Repo()
except InvalidGitRepositoryError:
    pass


@setbot.on_callback_query(dynamic_data_filter('change_branches'))
async def chng_branch(_, query):
    buttons = [
        [InlineKeyboardButton(r, callback_data=f'chng_branch_{r}')]
        for r in repo.branches
    ]
    if SKYNOID_IMG:
        await query.message.edit_caption(
            '**[#] Which branch would you like to change to?**\n' +
            f' - Currently activated: `[{repo.active_branch}]`\n\n' +
            '__(this might break your userbot ' +
            'if you are not cautious of what you are doing..)__',
        ),
        await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
    else:
        await query.message.edit(
            '**[#] Which branch would you like to change to?**' +
            f' - Currently activated: `[{repo.active_branch}]`',
            reply_markup=InlineKeyboardMarkup(buttons),
        )


async def branch_button_callback(_, __, query):
    if re.match(r'chng_branch_', query.data):
        return True


branch_button_create = filters.create(branch_button_callback)


@setbot.on_callback_query(branch_button_create)
async def change_to_branch(client, query):
    branch_match = re.findall(r'master|dev|translations', query.data)
    if branch_match:
        try:
            repo.git.checkout(branch_match[0])
        except GitCommandError as exc:
            await query.message.edit(f'**ERROR**: {exc}')
            return
        await create_subprocess_exec(
            'pip3',
            'install',
            '-U',
            '-r',
            'requirements.txt',
        )
        await query.message.edit(
            'Branch Changed to {}\nplease consider checking the logs'.format(
                repo.active_branch,
            ),
        )
        await query.answer()
        await sleep(60)
        await restart_all()
    else:
        await query.answer("Doesn't look like an Official Branch, Aborting!")
