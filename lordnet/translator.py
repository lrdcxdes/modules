from helper import module, import_library, Message, prefix

GoogleTranslator = import_library("deep_translator").GoogleTranslator


LANGUAGES = {
    "af": "afrikaans",
    "sq": "albanian",
    "am": "amharic",
    "ar": "arabic",
    "hy": "armenian",
    "az": "azerbaijani",
    "eu": "basque",
    "be": "belarusian",
    "bn": "bengali",
    "bs": "bosnian",
    "bg": "bulgarian",
    "ca": "catalan",
    "ceb": "cebuano",
    "ny": "chichewa",
    "zh-cn": "chinese (simplified)",
    "zh-tw": "chinese (traditional)",
    "co": "corsican",
    "hr": "croatian",
    "cs": "czech",
    "da": "danish",
    "nl": "dutch",
    "en": "english",
    "eo": "esperanto",
    "et": "estonian",
    "tl": "filipino",
    "fi": "finnish",
    "fr": "french",
    "fy": "frisian",
    "gl": "galician",
    "ka": "georgian",
    "de": "german",
    "el": "greek",
    "gu": "gujarati",
    "ht": "haitian creole",
    "ha": "hausa",
    "haw": "hawaiian",
    "iw": "hebrew",
    "he": "hebrew",
    "hi": "hindi",
    "hmn": "hmong",
    "hu": "hungarian",
    "is": "icelandic",
    "ig": "igbo",
    "id": "indonesian",
    "ga": "irish",
    "it": "italian",
    "ja": "japanese",
    "jw": "javanese",
    "kn": "kannada",
    "kk": "kazakh",
    "km": "khmer",
    "ko": "korean",
    "ku": "kurdish (kurmanji)",
    "ky": "kyrgyz",
    "lo": "lao",
    "la": "latin",
    "lv": "latvian",
    "lt": "lithuanian",
    "lb": "luxembourgish",
    "mk": "macedonian",
    "mg": "malagasy",
    "ms": "malay",
    "ml": "malayalam",
    "mt": "maltese",
    "mi": "maori",
    "mr": "marathi",
    "mn": "mongolian",
    "my": "myanmar (burmese)",
    "ne": "nepali",
    "no": "norwegian",
    "or": "odia",
    "ps": "pashto",
    "fa": "persian",
    "pl": "polish",
    "pt": "portuguese",
    "pa": "punjabi",
    "ro": "romanian",
    "ru": "russian",
    "sm": "samoan",
    "gd": "scots gaelic",
    "sr": "serbian",
    "st": "sesotho",
    "sn": "shona",
    "sd": "sindhi",
    "si": "sinhala",
    "sk": "slovak",
    "sl": "slovenian",
    "so": "somali",
    "es": "spanish",
    "su": "sundanese",
    "sw": "swahili",
    "sv": "swedish",
    "tg": "tajik",
    "ta": "tamil",
    "te": "telugu",
    "th": "thai",
    "tr": "turkish",
    "uk": "ukrainian",
    "ur": "urdu",
    "ug": "uyghur",
    "uz": "uzbek",
    "vi": "vietnamese",
    "cy": "welsh",
    "xh": "xhosa",
    "yi": "yiddish",
    "yo": "yoruba",
    "zu": "zulu",
}
LANGUAGES_REVERSED = {i[1]: i[0] for i in LANGUAGES.items()}


flag = import_library("flag", "emoji-country-flag")


def get_emoji(lang: str):
    return flag.flag(lang)


@module(
    commands=["tr", "translate"],
    description="Переводчик Google Translate 🗣️",
    args=["lang_to", "lang_from", "text/reply"],
)
async def translate_cmd(_, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.edit(
            f"<b>⛔ Используйте: <code>{prefix()}tr <b>[lang_to]</b> <i>[lang_from]<i> <b>["
            f"reply/text]*</b></code></b>"
        )
        return
    elif len(message.command) < 1 and not message.reply_to_message:
        await message.edit(
            f"<b>⛔ Используйте: <code>{prefix()}tr <b>[lang_to]</b> <i>[lang_from]<i> <b>["
            f"reply/text]*</b></code></b>"
        )
        return
    x = 1 if len(message.command) >= 2 else 0
    args = message.text.split()[x:]
    if args[0].lower() in LANGUAGES:
        lang_to = args[0].lower()
    elif args[0].lower() in LANGUAGES_REVERSED:
        lang_to = LANGUAGES_REVERSED[args[0].lower()]
    else:
        lang_to = "ru"
    if lang_to != "auto":
        if len(args) > 1:
            if args[1].lower() in LANGUAGES:
                lang_from = args[1].lower()
                text = (
                    " ".join(args[2:])
                    if not message.reply_to_message
                    else message.reply_to_message.text
                )
            elif args[1].lower() in LANGUAGES_REVERSED:
                lang_from = LANGUAGES_REVERSED[args[1].lower()]
                text = (
                    " ".join(args[2:])
                    if not message.reply_to_message
                    else message.reply_to_message.text
                )
            else:
                lang_from = "auto"
                text = (
                    " ".join(args[1:])
                    if not message.reply_to_message
                    else message.reply_to_message.text
                )
        else:
            lang_from = "auto"
            text = (
                " ".join(args)
                if not message.reply_to_message
                else message.reply_to_message.text
            )
    else:
        lang_from = "auto"
        text = (
            " ".join(args)
            if not message.reply_to_message
            else message.reply_to_message.text
        )

    try:
        translator = GoogleTranslator(source=lang_from, target=lang_to)
        translation = translator.translate(text)
        src_emoji, dest_emoji = get_emoji(lang_from), get_emoji(lang_to)
    except Exception as ex:
        await message.edit(f"<b>⛔ Ошибка перевода: <code>{ex}</code></b>")
        return
    await message.edit(
        f"<b>From {src_emoji}:\n<code>{text}</code>\n\nTo {dest_emoji}:\n<code>{translation}</code></b>"
    )


made_by = "@lord_code"
