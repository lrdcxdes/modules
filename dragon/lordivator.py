from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message

# noinspection PyUnresolvedReferences
from utils.misc import modules_help, prefix

# noinspection PyUnresolvedReferences
from utils.scripts import format_exc

from moviepy.editor import VideoFileClip, ImageClip
from moviepy.video.tools.drawing import blit
from PIL import Image, ImageDraw, ImageFont, ImageOps
import cv2


@Client.on_message(filters.command(["dem", "lordivate"], prefix) & filters.me)
async def lordivator_cmd(_: Client, message: Message):
    try:
        if len(message.command) == 1:
            return await message.edit("<b>Usage:</b>\n<code>{}dem [text]*</code>".format(prefix))
        text = message.text.split(maxsplit=1)[1]
        if message.reply_to_message:
            reply = message.reply_to_message
            if reply.photo:
                file = "preload.jpg"
                video = False
            elif reply.video:
                file = "preload.mp4"
                video = True
                audio = True
            elif reply.video_note:
                file = "preload.mp4"
                video = True
                audio = False
            elif reply.document:
                if not reply.document.file_name.endswith(
                    (".mp4", ".gif", ".webm", ".webp", ".jpg", ".jpeg", ".png")
                ):
                    return await message.edit(f'<b>Please reply to photo/video/sticker</b>')
                file = f'preload.{reply.document.file_name.split(".")[-1]}'
                if file.endswith((".mp4", ".gif", ".webm")):
                    video = True
                    if file.endswith('.mp4'):
                        audio = True
                    else:
                        audio = False
                else:
                    video = False
            elif reply.sticker:
                if reply.sticker.is_video:
                    file = "preload.webm"
                    video = True
                    audio = False
                elif reply.sticker.is_animated:
                    file = "preload.tgs"
                    video = True
                    audio = False
                else:
                    file = 'preload.webp'
                    video = False
            elif reply.animation:
                file = "preload.gif"
                video = True
                audio = False
            else:
                return await message.edit(f'<b>Please reply to photo/video/sticker/file</b>')
        else:
            return await message.edit(f'<b>Please reply to photo/video/sticker</b>')

        if video:
            # noinspection PyUnboundLocalVariable
            coro = process_video(message, file, audio, text)
        else:
            coro = process_image(message, file, text)

        return await coro

    except Exception as ex:
        return await message.edit(text=format_exc(ex))


async def create_img(file: str, text: str, text2: str = '', result=None):
    img = Image.new('RGB', (1280, 1024), color='black')
    img_border = Image.new('RGB', (1060, 720), color='#000000')
    # noinspection PyTypeChecker
    border = ImageOps.expand(img_border, border=2, fill='#ffffff')
    user_img = Image.open(file).convert("RGBA").resize((1050, 710))
    (width, height) = user_img.size
    img.paste(border, (111, 96))
    img.paste(user_img, (118, 103))
    drawer = ImageDraw.Draw(img)

    top_size, bottom_size = 80, 60

    font_1 = ImageFont.load_default()  # ImageFont.truetype(font='times.ttf', size=top_size, encoding='UTF-8')
    text_width = font_1.getsize(text)[0]
    if text_width >= (width + 250) - 20:
        print(text_width)

    # while text_width >= (width + 250) - 20:
    #     font_1 = ImageFont.truetype(font='times.ttf', size=top_size, encoding='UTF-8')
    #     text_width = font_1.getsize(text)[0]
    #     top_size -= 1

    size_1 = drawer.textsize(text, font=font_1)
    drawer.text(((1280 - size_1[0]) / 2, 840), text, fill='white', font=font_1)

    if text2:
        font_2 = ImageFont.truetype(font='times.ttf', size=bottom_size, encoding='UTF-8')
        text_width = font_2.getsize(text2)[0]

        if text_width >= (width + 250) - 20:
            print(text_width)

        # while text_width >= (width + 250) - 20:
        #     font_2 = ImageFont.truetype(font=font_name, size=bottom_size, encoding='UTF-8')
        #     text_width = font_2.getsize(self._bottom_text)[0]
        #     bottom_size -= 1

        size_2 = drawer.textsize(text2, font=font_2)
        drawer.text(((1280 - size_2[0]) / 2, 930), text2, fill='white', font=font_2)

    img.save(result)

    return result


async def process_video(message: Message, file: str, audio: bool, text: str):
    await message.edit('<b>📽️ Processing video...</b>')
    await message.reply_chat_action("record_video")

    file = await message.reply_to_message.download(f'downloads/{file}')

    vidcap = cv2.VideoCapture(file)
    _, image = vidcap.read()
    cv2.imwrite(f'downloads/demotivated.jpg', image)
    vidcap.release()

    byt = BytesIO()
    byt.name = 'demotivator.jpg'

    img = await create_img(file=f'downloads/demotivated.jpg', text=text,
                           result=byt)

    byt.seek(0)

    await message.reply_photo(photo=img, reply_to_message_id=message.reply_to_message.message_id)

    return await message.delete()

    # video = VideoFileClip(file, audio=audio)


async def process_image(message: Message, file: str, text: str):
    await message.edit('<b>🖼️ Processing image...</b>')
    await message.reply_chat_action("upload_photo")

    file = await message.reply_to_message.download(f'downloads/{file}')

    byt = BytesIO()
    byt.name = 'demotivator.jpg'

    img = await create_img(file=file, text=text,
                           result=byt)

    byt.seek(0)

    await message.reply_photo(photo=img, reply_to_message_id=message.reply_to_message.message_id)
    return await message.delete()


modules_help['lordivator'] = {
    'dem': 'Demotivate a replied message',
}
