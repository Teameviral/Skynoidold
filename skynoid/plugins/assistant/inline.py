from .inline_mod import alive_func
from .inline_mod import anime_func
from .inline_mod import fav_func
from .inline_mod import note_func
from .inline_mod import pmpermit_func
from .inline_mod import speedtest_func
from .inline_mod import stylish_func
from .inline_mod import inline_search
from skynoid import AdminSettings
from skynoid import DB_AVAILABLE
from skynoid import Owner
from skynoid import OwnerName
from skynoid import setbot
from skynoid.plugins.database import anime_db as sql


@setbot.on_inline_query()
async def inline_query_handler(client, query):
    string = query.query.lower()
    answers = []

    if query.from_user.id not in AdminSettings:
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text=f'Sorry, this bot only for {OwnerName}',
            switch_pm_parameter='createown',
        )
        return
    if string == '':
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text='Need help? Click here',
            switch_pm_parameter='help_inline',
        )
        return

    # Notes
    if string.split()[0] == 'note':
        if not DB_AVAILABLE:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text="Your database isn't avaiable!",
                switch_pm_parameter='help_inline',
            )
            return
        await note_func(string, client, query, answers)

    # Stylish converter
    elif string.split()[0] == 'stylish':
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Insert any text to convert it!',
                switch_pm_parameter='help_inline',
            )
            return
        text = string.split(None, 1)[1]
        await stylish_func(text, answers)
    # PM_PERMIT
    elif string.split()[0] == 'engine_pm':
        await pmpermit_func(answers)

    elif string.split()[0] == 'speedtest':
        await speedtest_func(answers)

    elif string.split()[0] == 'alive':
        await alive_func(answers)

    elif string.split()[0] == 'anime':
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Search an Anime',
                switch_pm_parameter='help_inline',
            )
            return
        await anime_func(string, answers)

    elif string.split()[0] == 'favourite':
        fav = sql.get_fav(Owner)
        await fav_func(fav, answers)

    elif string.split()[0] == 'search':
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Search messages Globally',
                switch_pm_parameter='help_inline',
            )
            return
        await inline_search(string, answers)

    await client.answer_inline_query(
        query.id,
        results=answers,
        cache_time=0,
    )
