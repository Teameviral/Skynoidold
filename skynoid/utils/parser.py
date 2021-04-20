import html
import re
from skynoid import app


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ''
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        result.append(small_msg)

    return result


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)


def escape_markdown(text):
    """Helper function to escape telegram markup symbols."""
    escape_chars = r'\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def mention_html(user_id, name):
    return '<a href="tg://user?id={}">{}</a>'.format(
        user_id,
        html.escape(name),
    )


def mention_markdown(user_id, name):
    return '[{}](tg://user?id={})'.format(escape_markdown(name), user_id)


async def user_time_and_reason(message):
    if message.reply_to_message:
        return (
            message.reply_to_message.from_user.id,
            message.command[1],
            ' '.join(message.command[2:]),
        )
    u = await app.resolve_peer(message.command[1])
    return u.user_id, message.command[2], ' '.join(message.command[3:])


def time_parser_int(time_end):
    month = time_end // 2678400
    days = time_end // 86400
    hours = time_end // 3600 % 24
    minutes = time_end // 60 % 60
    seconds = time_end % 60
    times = ''
    if month:
        times += f'{month} month, '
    if days:
        times += f'{days} days, '
    if hours:
        times += f'{hours} hours, '
    if minutes:
        times += f'{minutes} minutes, '
    if seconds:
        times += f'{seconds} seconds'
    if times == '':
        times = f'{time_end} miliseconds'
    return times[:-2] if times[-2:] == ', ' else times
