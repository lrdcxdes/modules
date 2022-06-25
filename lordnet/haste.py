from helper import module, Message, session


link = "https://hastebin.com"


@module(commands=["haste", "paste"], args="reply/text", desc="Upload code to hastebin")
async def haste_cmd(_, message: Message):
	if message.reply_to_message and message.reply_to_message.text:
		text = message.reply_to_message.text
	elif len(message.command) > 1:
		text = message.text.split(maxsplit=1)[1]
	else:
		return await message.edit('<b>🧑‍💻 Пожалуйста укажите код (reply/text)')
		
	async with session.post(
        "{}/documents".format(link),
        data=text.encode("utf-8")
    ) as res:
		result = await res.json()
	
	url = "{}/{}.py".format(link, result["key"])

	await message.reply(
        url,
        reply_to_message_id=message.reply_to_message.id
    ) if message.reply_to_message else await message.edit(url)
