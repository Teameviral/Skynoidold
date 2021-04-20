"""The initial start of Skynoid."""
import logging
import os
import platform
import sys
import time
from inspect import getfullargspec

from pydrive.auth import GoogleAuth
from pyrogram import Client
from pyrogram import errors
from pyrogram.types import Message
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from .src.variable import get_var

StartTime = time.time()


# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logging.error('Python version Lower than 3.6! Abort!')
    sys.exit()

USERBOT_VERSION = '3.2.5'
ASSISTANT_VERSION = '3.2.5'

OFFICIAL_BRANCH = ['master', 'translations']
RANDOM_STICKERS = [
    'CAADAgAD6EoAAuCjggf4LTFlHEcvNAI',
    'CAADAgADf1AAAuCjggfqE-GQnopqyAI',
    'CAADAgADaV0AAuCjggfi51NV8GUiRwI',
]

ENV = get_var('ENV', False)
logger = get_var('LOGGER', False)
# Version
LANG_CODE = get_var('lang_code', 'en')
DEVICE_MODEL = platform.machine()
SYSTEM_VERSION = platform.platform()
time_country = get_var('time_country', None)

# Must be filled
API_ID = int(get_var('api_id', None))
API_HASH = get_var('api_hash', None)

# Session
USERBOT_SESSION = get_var('USERBOT_SESSION', None)
ASSISTANT_BOT_TOKEN = get_var('ASSISTANT_BOT_TOKEN', None)

# From config
COMMAND_PREFIXES = get_var('Command', '! . - ^').split()
# APIs
SCREENSHOTLAYER_API = get_var('screenshotlayer_API', None)
GDRIVE_CREDENTIALS = get_var('gdrive_credentials', None)
LYDIA_API = get_var('lydia_api', None)
REMOVE_BG_API = get_var('remove_bg_api', None)
SPAMWATCH_API = get_var('sw_api', None)
IBM_WATSON_CRED_URL = get_var('IBM_WATSON_CRED_URL', None)
IBM_WATSON_CRED_PASSWORD = get_var('IBM_WATSON_CRED_PASSWORD', None)

# LOADER
USERBOT_LOAD = get_var('USERBOT_LOAD', '').split()
USERBOT_NOLOAD = get_var('USERBOT_NOLOAD', '').split()
ASSISTANT_LOAD = get_var('ASSISTANT_LOAD', '').split()
ASSISTANT_NOLOAD = get_var('ASSISTANT_NOLOAD', '').split()

# Git Repository for Pulling Updates
REPOSITORY = get_var('REPOSITORY', False)

# Postgresql Database
DB_URI = get_var(
    'DB_URI', 'postgres://username:password@localhost:5432/database',
)

AdminSettings = [int(x) for x in get_var('AdminSettings', '').split()]
REMINDER_UPDATE = bool(get_var('REMINDER_UPDATE', True))
SKYNOID_IMG = get_var('SKYNOID_IMG', False)
PM_PERMIT = bool(get_var('PM_PERMIT', False))

OwnerName = ''
app_version = f'💝 Skynoid (v{USERBOT_VERSION})'
BotUsername = ''
BotID = 0
# Required for some features
# Set temp var for load later
Owner = 0
BotName = ''
OwnerUsername = ''

if os.path.exists('skynoid/logs/error.txt'):
    with open('skynoid/logs/error.txt', 'a') as f:
        f.write('PEEK OF LOG FILE')
LOG_FORMAT = (
    '%(filename)s:%(lineno)s %(levelname)s: %(message)s'
)
logging.basicConfig(
    level=logging.ERROR,
    format=LOG_FORMAT,
    datefmt='%m-%d %H:%M',
    filename='skynoid/logs/error.txt',
    filemode='w',
)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

log = logging.getLogger()

gauth = GoogleAuth()

DB_AVAILABLE = False
BOTINLINE_AVAIABLE = False


# Postgresql
def mulaisql() -> scoped_session:
    global DB_AVAILABLE
    engine = create_engine(DB_URI, client_encoding='utf8')
    BASE.metadata.bind = engine
    try:
        BASE.metadata.create_all(engine)
    except exc.OperationalError:
        DB_AVAILABLE = False
        return False
    DB_AVAILABLE = True
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


async def get_bot_inline(bot):
    global BOTINLINE_AVAIABLE
    if setbot:
        try:
            await app.get_inline_bot_results(
                f'@{bot.username}', 'test',
            )
            BOTINLINE_AVAIABLE = True
        except errors.exceptions.bad_request_400.BotInlineDisabled:
            BOTINLINE_AVAIABLE = False


async def get_self():
    global Owner, OwnerName, OwnerUsername, AdminSettings
    getself = await app.get_me()
    Owner = getself.id
    if getself.last_name:
        OwnerName = getself.first_name + ' ' + getself.last_name
    else:
        OwnerName = getself.first_name
    OwnerUsername = getself.username
    if Owner not in AdminSettings:
        AdminSettings.append(Owner)


async def get_bot():
    global BotID, BotName, BotUsername
    getbot = await setbot.get_me()
    BotID = getbot.id
    BotName = getbot.first_name
    BotUsername = getbot.username


BASE = declarative_base()
SESSION = mulaisql()

setbot = Client(
    ':memory:',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=ASSISTANT_BOT_TOKEN,
    workers=2,
)

app = Client(
    USERBOT_SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=app_version,
    device_model=DEVICE_MODEL,
    system_version=SYSTEM_VERSION,
    lang_code=LANG_CODE,
    workers=8,
)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})
