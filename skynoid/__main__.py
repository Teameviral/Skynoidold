import asyncio
import importlib
import sys
import traceback

from pyrogram import idle
from pyrogram.types import InlineKeyboardButton

from pykeyboard import InlineKeyboard

from skynoid import app
from skynoid import Owner
from skynoid import log
from skynoid import setbot
from skynoid import get_self
from skynoid  import get_bot
from skynoid.plugins.assistant import ALL_SETTINGS
from skynoid.plugins import ALL_MODULES

try:
    from skynoid import TEST_DEVELOP
except ImportError:
    TEST_DEVELOP = False

BOT_RUNTIME = 0
HELP_COMMANDS = {}

loop = asyncio.get_event_loop()


async def get_runtime():
    return BOT_RUNTIME


async def reload_userbot():
    await app.start()
    for modul in ALL_MODULES:
        imported_module = importlib.import_module('skynoid.plugins.' + modul)
        importlib.reload(imported_module)


async def reinitial_restart():
    await get_bot()
    await get_self()


async def reboot():
    global BOT_RUNTIME, HELP_COMMANDS
    importlib.reload(importlib.import_module('skynoid.plugins'))
    importlib.reload(importlib.import_module('skynoid.plugins.assistant'))
    await setbot.restart()
    await app.restart()
    await reinitial_restart()
    BOT_RUNTIME = 0
    HELP_COMMANDS = {}
    # Assistant bot
    for setting in ALL_SETTINGS:
        imported_module = importlib.import_module(
            'skynoid.plugins.assistant.' + setting,
        )
        importlib.reload(imported_module)
    # Skynoid userbot
    for modul in ALL_MODULES:
        imported_module = importlib.import_module('skynoid.plugins.' + modul)
        if hasattr(
            imported_module,
            '__MODULE__',
        ) and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(
            imported_module,
            '__MODULE__',
        ) and imported_module.__MODULE__:
            if imported_module.__MODULE__.lower() not in HELP_COMMANDS:
                HELP_COMMANDS[
                    imported_module.__MODULE__.lower()
                ] = imported_module
            else:
                raise Exception(
                    "Can't have two modules with the same name!",
                )
        if hasattr(imported_module, '__HELP__') and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
        importlib.reload(imported_module)


# await setbot.send_message(Owner, "Restart successfully!")


async def restart_all():
    # Restarting and load all plugins
    asyncio.get_event_loop().create_task(reboot())


async def except_hook(errtype, value, tback):
    sys.__excepthook__(errtype, value, tback)
    errors = traceback.format_exception(etype=errtype, value=value, tb=tback)
    keyboard = InlineKeyboard(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            '🐞 Report bugs',
            callback_data='report_errors',
        ),
    )
    text = 'An error has accured!\n\n```{}```\n'.format(''.join(errors))
    if errtype == ModuleNotFoundError:
        text += '\nHint: `pip install -r requirements.txt`'
    await setbot.send_message(Owner, text, reply_markup=keyboard)


async def reinitial():
    await app.start()
    await setbot.start()
    await get_self()
    await get_bot()
    await app.stop()
    await setbot.stop()


async def start_bot():
    # sys.excepthook = await except_hook
    print('----- Checking user and bot... -----')
    await reinitial()
    print('----------- Check done! ------------')
    # Assistant bot
    await setbot.start()
    for setting in ALL_SETTINGS:
        imported_module = importlib.import_module(
            'skynoid.plugins.assistant.' + setting,
        )
    # Skynoid userbot
    await app.start()
    for modul in ALL_MODULES:
        imported_module = importlib.import_module('skynoid.plugins.' + modul)
        if hasattr(
            imported_module,
            '__MODULE__',
        ) and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(
            imported_module,
            '__MODULE__',
        ) and imported_module.__MODULE__:
            if imported_module.__MODULE__.lower() not in HELP_COMMANDS:
                HELP_COMMANDS[
                    imported_module.__MODULE__.lower()
                ] = imported_module
            else:
                raise Exception(
                    "Can't have two modules with the same name!",
                )
        if hasattr(imported_module, '__HELP__') and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
    userbot_modules = ''
    assistant_modules = ''
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            userbot_modules += f'|{i:<15}|\n'
            j = 0
        else:
            userbot_modules += f'|{i:<15}'
        j += 1
    j = 1
    for i in ALL_SETTINGS:
        if j == 4:
            assistant_modules += f'|{i:<15}|\n'
            j = 0
        else:
            assistant_modules += f'|{i:<15}'
        j += 1
    print('+===============================================================+')
    print('|                     Userbot Modules                           |')
    print('+=============+===============+================+===============+')
    print(userbot_modules)
    print('+=============+===================+=============+===============+')
    print('+===============================================================+')
    print('|                     Assistant Modules                         |')
    print('+=============+=================+===============+===============+')
    print(assistant_modules)
    print('+===============+=============+===============+=================+')
    print('Logged in User: {}'.format((await app.get_me()).first_name))
    print('Logged in Bot: {}'.format((await setbot.get_me()).first_name))
    if TEST_DEVELOP:
        log.warning('Test is passed!')
    else:
        await idle()


if __name__ == '__main__':
    loop.run_until_complete(start_bot())
