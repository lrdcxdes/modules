from io import BytesIO
from helper import session, module, Message, prefix, exception_str


@module(cmds="readqr", args=["реплай/фото"], desc="Читает значение из qr-кода")
async def readqrcode_handler(_, message: Message):
    try:
        if message.photo:
            filename = await message.download("downloads/temp.png")
        elif message.text:
            if not message.reply_to_message:
                return await message.edit(
                    f"<b>📵 Используйте: <code>{prefix()}readqr [реплай/фото]</code></b>"
                )
            filename = await message.reply_to_message.download("downloads/temp.png")
        else:
            return await message.edit(
                f"<b>📵 Используйте: <code>{prefix()}readqr [реплай/фото]</code></b>"
            )

        async with session.post(
            url2, data={"file": open(filename, "rb").read()}
        ) as response:
            json = await response.json()
            text = json[0]["symbol"][0]["data"]
            if not text:
                return await message.reply("<b>⛔ Не удалось распознать QR-код!</b>")
            return await message.reply(
                f"<b>📸 Расшифрованый текст</b>:\n<code>{text}</code>"
            )
    except Exception as e:
        return await message.reply(exception_str(e))


url = (
    "https://api.qrserver.com/v1/create-qr-code/?data="
    "{}&size=512x512&charset-source=UTF-8&charset-target=UTF-8&ecc=L&color=0-0-0&bgcolor=255-255-255&margin=1"
    "&qzone=1&format=png"
)
url2 = "https://api.qrserver.com/v1/read-qr-code/?outputformat=json"


@module(cmds="makeqr", args=["текст/ссылка"], desc="Создает qr-код")
async def makeqrcode_handler(_, message: Message):
    if len(message.text.split()) < 2:
        return await message.edit(f"📵 Используйте: <code>{prefix}makeqr [текст]</code>")
    await message.edit("<b>🔨 Делаю qrcode...</b>")
    data = message.text.split(maxsplit=1)[1]
    try:
        async with session.get(url.format(data)) as response:
            qrcode = BytesIO(await response.read())
            qrcode.name = "qrcode.png"
            qrcode.seek(0)
            await message.reply_photo(qrcode)
            return await message.delete()
    except Exception as e:
        return await message.edit(exception_str(e))

made_by = '@lord_code'
