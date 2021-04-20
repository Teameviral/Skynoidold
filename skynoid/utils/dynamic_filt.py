from pyrogram import filters


# For callback query button
def dynamic_data_filter(data):
    async def func(flt, _, query):
        return flt.data == query.data

    # "data" kwarg is accessed with "flt.data" above
    return filters.create(func, data=data)
