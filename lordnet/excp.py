from helper import module


@module(commands="raise", desc="Raise an exception")
async def raise_excp(_, __):
    raise Exception("Test exception")
