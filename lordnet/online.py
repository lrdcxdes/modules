from pyrogram.errors import RPCError

from helper import module, Message, Client, db, escape_html
from pyrogram.raw.functions.account import UpdateStatus
from pyrogram.filters import create, channel


status = db.get("status", {})


@module(commands=["online", "offline"], desc="Включить/Выключить статус в телеграмм")
async def fake_online(client: Client, message: Message):
    now = True if message.command[0] == "online" else False

    await client.send(UpdateStatus(offline=not now))

    await message.edit(
        f"<b>🌚 Теперь ваш статус: <code>{'Онлайн ✅' if now else 'Оффлайн ⛔'}</code></b>"
    )


@module(create(lambda _, __, m: status[m.chat.id]) & ~channel)
async def auto_read(client: Client, message: Message):
    try:
        await client.read_history(message.chat.id)
    except RPCError:
        pass


@module(commands=["read", "autoread"], desc="Авто-прочтение сообщений")
async def autoread_cmd(_, message: Message):
    now = not status
    status[message.chat.id] = now
    db.set("status", status)

    await message.edit(
        f"<b>🌚 Autoread в чате {escape_html(message.chat.title)}: <code>{'Включён ✅' if now else 'Выключен ⛔'}</code></b>"
    )


made_by = "@lord_code"
