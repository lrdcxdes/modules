import os
from hashlib import sha256

from pyrogram import Client, filters
from pyrogram.types import Message

from aiohttp import ClientSession

# noinspection PyUnresolvedReferences
from utils.misc import modules_help, prefix
from utils.scripts import format_exc, restart

BASE_PATH = os.path.abspath(os.getcwd())
session = ClientSession()


# noinspection PyUnusedLocal
@Client.on_message(
    filters.command(["lordload", "lloadall", "lload", "lordloadall"], prefix)
    & filters.me
)
async def lordload_handler(client: Client, message: Message):
    try:
        await message.edit("<b>Processing...</b>")

        async with session.get("https://dragon-modules.cf/all.py") as response:
            if response.ok:
                modules = (await response.text()).split("\r\n")
            else:
                return await message.edit(
                    "<b>Failed to get modules list.</b> (<code>{}</code>)".format(
                        response.status
                    )
                )

        async with session.get(
            "https://raw.githubusercontent.com/Dragon-Userbot/custom_modules/main/modules_hashes.txt"
        ) as response:
            if response.ok:
                modules_hashes = await response.text()
            else:
                return await message.edit(
                    "<b>Failed to get modules hashes list.</b> (<code>{}</code>)".format(
                        response.status
                    )
                )

        if "all" in message.command[0]:
            await message.edit(
                "<b>Loading all modules from dragon-modules.cf</b>",
                disable_web_page_preview=True,
            )
            names = modules
        else:
            names = [
                message.text.lower().split(maxsplit=1)[1].split(".", maxsplit=1)[0]
            ]
            await message.edit(
                f"<b>Loading module <b>{names[0]}</b> from dragon-modules.cf</b>",
                disable_web_page_preview=True,
            )
        if not os.path.exists(f"{BASE_PATH}/modules/custom_modules"):
            os.mkdir(f"{BASE_PATH}/modules/custom_modules")

        result = []

        for name in names:
            if name not in modules:
                return await message.edit(f"Module <b>{name}</b> not found.")
            async with session.get(f"https://dragon-modules.cf/{name}") as response:
                if response.ok:
                    source = await response.read()
                    if sha256(source).hexdigest() not in modules_hashes:
                        continue
                    with open(
                        f"{BASE_PATH}/modules/custom_modules/{name}.py", "wb"
                    ) as f:
                        f.write(source)
                        result.append(name)
                else:
                    return await message.edit(f"Module <b>{name}</b> not found.")

        names = "<i>,</i> ".join(result)
        if not names:
            return await message.edit(
                f"The module <b>{name}</b> has not been verified. Expect a post in @dragon_modules"
            )

        await message.edit(f"Module <b>{names}</b> loaded successfully.")

        restart()
    except Exception as ex:
        return await message.edit(format_exc(ex))


modules_help["lordload"] = {
    "lload [name]": "Loads module from dragon-modules.cf",
    "lloadall": "Loads all the modules from dragon-modules.cf",
}
