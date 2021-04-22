import os
import re
import subprocess
import sys
import traceback
from io import StringIO

from pyrogram import filters

from skynoid import Owner
from skynoid import setbot
from skynoid.utils import filt
from skynoid.plugins.devs import aexec


@setbot.on_message(filters.user(Owner) & filt.command(['eval']))
async def eval(client, message):
    status_message = await message.reply_text('`Running ...`')
    try:
        cmd = message.text.split(' ', maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ''
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = 'Success'
    final_output = f'**OUTPUT**:\n```{evaluation.strip()}```'
    if len(final_output) > 4096:
        filename = 'output.txt'
        with open(filename, 'w+', encoding='utf8') as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove(filename)
        await status_message.delete()
    else:
        await status_message.edit(final_output)


@setbot.on_message(filters.user(Owner) & filt.command(['sh']))
async def terminal(client, message):
    if len(message.text.split()) == 1:
        await message.reply('Usage: `/sh ping -c 5 google.com`')
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if '\n' in teks:
        code = teks.split('\n')
        output = ''
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                )
            except Exception as err:
                print(err)
                await message.reply(
                    """
**Error:**
```{}```
""".format(err),
                )
            output += f'**{code}**\n'
            output += process.stdout.read()[:-1].decode('utf-8')
            output += '\n'
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', '')
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb,
            )
            await message.reply('**Error:**\n```{}```'.format(''.join(errors)))
            return
        output = process.stdout.read()[:-1].decode('utf-8')
    if str(output) == '\n':
        output = None
    if output:
        if len(output) > 4096:
            with open('skynoid/cache/output.txt', 'w+') as file:
                file.write(output)
                file.close()
            await client.send_document(
                message.chat.id,
                'skynoid/cache/output.txt',
                reply_to_message_id=message.message_id,
                caption='`Output file`',
            )
            os.remove('skynoid/cache/output.txt')
            return
        await message.reply(
            f'**Output:**\n```{output}```',
            parse_mode='markdown',
        )
    else:
        await message.reply('**Output:**\n`No Output`')
