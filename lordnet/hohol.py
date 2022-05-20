from helper import module, Message
from pyrogram import filters, Client, ContinuePropagation
import re

words = ["хохол", "хохл", '❌⭕❌⭕л', '❌⭕❌л']


async def hohol_func(_, __, m: Message): 
    lower = m.text.lower() if m.text else m.caption.lower()
    if any(i in lower for i in words[2:]):
    	return True
    lower = re.sub('[^a-zа-я]', '', lower)
    lower = lower.replace('h', 'х').replace('o', 'о').replace('x', 'х').replace('l', 'л').replace('i', 'л')
    return any(i in lower for i in words[:2])


hohol_filter = filters.create(hohol_func)


@module((filters.me | filters.private) & (filters.text | filters.caption) & hohol_filter, desc="\n🐷 Анти-Хохол модуль, создан чтобы сдержаться от таких слов в сообщениях")
async def global_filter(client: Client, message: Message):
    if not bool(message.from_user and message.from_user.is_self or message.outgoing):
    	await message.delete()
    	await message.reply("<b>🐷 Анти-Хохол!</b>\nОбнаружено запрещенное слово в сообщении!")
    	return
    	
    if message.text:
    	func = message.edit
    else:
    	func = message.edit_caption

    await func("<b>🐷 Анти-Хохол!</b>\nОбнаружено запрещенное слово в сообщении!")
    
    raise ContinuePropagation


made_by = "@lord_code"
