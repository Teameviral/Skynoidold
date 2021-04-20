import shlex
from typing import List
import re

from pyrogram.filters import create
from pyrogram.types import Message

from skynoid import BotUsername

COMMAND_PREFIXES = ['/', '!']


def command(
    commands: str or List[str],
    prefixes: str or List[str] = '/',
    case_sensitive: bool = False,
):
    async def func(flt, _, message: Message):
        text: str = message.text or message.caption
        message.command = None

        if not text:
            return False

        regex = '^({prefix})+\\b({regex})\\b(\\b@{bot_name}\\b)?(.*)'.format(
            prefix='|'.join(re.escape(x) for x in COMMAND_PREFIXES),
            regex='|'.join(flt.commands).lower(),
            bot_name=BotUsername,
        )

        matches = re.search(re.compile(regex), text.lower())
        if not matches:
            return False
        message.command = [matches.group(2)]
        try:
            for arg in shlex.split(matches.group(4).strip()):
                if arg == BotUsername:
                    continue
                message.command.append(arg)
        except ValueError:
            return True
        return True

    commands = commands if type(commands) is list else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if type(prefixes) is list else [prefixes]
    prefixes = set(prefixes) if prefixes else {''}

    return create(
        func,
        'CustomCommandFilter',
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive,
    )
