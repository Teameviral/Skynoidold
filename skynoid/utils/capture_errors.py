import sys
import traceback
from functools import wraps

from pyrogram.types import InlineKeyboardButton

from pykeyboard import InlineKeyboard

from skynoid import Owner
from skynoid import setbot
from skynoid.utils.parser import split_limits


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb,
            )
            error_feedback = split_limits(
                '**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n'.format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    ''.join(errors),
                ),
            )
            button = InlineKeyboard(row_width=1)
            button.add(
                InlineKeyboardButton(
                    '🐞 Report bugs',
                    callback_data='report_errors',
                ),
            )
            for x in error_feedback:
                await setbot.send_message(
                    Owner,
                    x,
                    reply_markup=button,
                )
            raise err
    return capture
