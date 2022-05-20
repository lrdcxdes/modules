from helper import import_library, module, Message, escape_html
from asyncio import sleep


trashguy_lib = import_library("trashguy")
TrashGuy = trashguy_lib.TrashGuy
Symbols = trashguy_lib.Symbols


@module(
    cmds=["trashguy", "trash", "ftrash", "fastguy", "strash", "superguy"],
    desc="Анимация кота который несёт ваш текст в мусорку (super может вызывать флудвейт)",
)
async def trashguy(_, message: Message):
    """
    Анимация кота который несёт ваш текст в мусорку
    """
    text = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else "амокдев"
    parts = TrashGuy(text, spacer=Symbols.SPACER_WIDE)

    if message.command[0].startswith("f"):
        delay = 0.3
    elif message.command[0].startswith("s"):
        delay = 0.1
    else:
        delay = 1

    for part in parts:
        await message.edit(escape_html(part), disable_web_page_preview=True)
        await sleep(delay)


made_by = "@lord_code"
