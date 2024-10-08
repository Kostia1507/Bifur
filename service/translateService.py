from deep_translator import GoogleTranslator, constants

# this is the dictionary of discord emojis to languages in Google Translate
langs = {
    "🇦🇫": None,
    "🇦🇽": None,
    "🇦🇱": ["sq"],
    "🇩🇿": None,
    "🇦🇸": None,
    "🇦🇩": None,
    "🇦🇴": None,
    "🇦🇮": None,
    "🇦🇶": None,
    "🇦🇬": None,
    "🇦🇷": ["es"],
    "🇦🇲": ["hy"],
    "🇦🇼": None,
    "🇦🇺": ["en"],
    "🇦🇹": ["de"],
    "🇦🇿": ["az"],
    "🇧🇸": None,
    "🇧🇭": None,
    "🇧🇩": None,
    "🇧🇧": None,
    "🇧🇾": ["be"],
    "🇧🇪": ["nl", "fr", "de"],
    "🇧🇿": None,
    "🇧🇯": None,
    "🇧🇲": None,
    "🇧🇹": None,
    "🇧🇴": None,
    "🇧🇦": None,
    "🇧🇼": None,
    "🇧🇷": ["pt"],
    "🇮🇴": None,
    "🇻🇬": None,
    "🇧🇳": None,
    "🇧🇬": ["bg"],
    "🇧🇫": None,
    "🇧🇮": None,
    "🇰🇭": None,
    "🇨🇲": None,
    "🇨🇦": ["en", "fr"],
    "🇮🇨": None,
    "🇨🇻": None,
    "🇧🇶": None,
    "🇰🇾": None,
    "🇨🇫": None,
    "🇹🇩": ["ar", "fr"],
    "🇨🇱": ["es"],
    "🇨🇳": ["zh-CN", "zh-TW"],
    "🇨🇽": None,
    "🇨🇨": None,
    "🇨🇴": ["es"],
    "🇰🇲": None,
    "🇨🇬": None,
    "🇨🇩": None,
    "🇨🇰": None,
    "🇨🇷": None,
    "🇨🇮": None,
    "🇭🇷": ["hr"],
    "🇨🇺": None,
    "🇨🇼": None,
    "🇨🇾": ["el", "tr"],
    "🇨🇿": ["cs"],
    "🇩🇰": ["da"],
    "🇩🇯": None,
    "🇩🇲": None,
    "🇩🇴": None,
    "🇪🇨": None,
    "🇪🇬": ["ar"],
    "🇸🇻": None,
    "🇬🇶": None,
    "🇪🇷": None,
    "🇪🇪": "et",
    "🇪🇹": None,
    "🇫🇰": None,
    "🇫🇴": None,
    "🇫🇯": None,
    "🇫🇮": ["fi"],
    "🇫🇷": ["fr"],
    "🇬🇫": None,
    "🇵🇫": None,
    "🇹🇫": None,
    "🇬🇦": None,
    "🇬🇲": None,
    "🇬🇪": ["ka"],
    "🇩🇪": ["de"],
    "🇬🇭": None,
    "🇬🇮": None,
    "🇬🇷": ["el"],
    "🇬🇱": None,
    "🇬🇩": None,
    "🇬🇵": None,
    "🇬🇺": None,
    "🇬🇹": None,
    "🇬🇬": None,
    "🇬🇳": None,
    "🇬🇼": None,
    "🇬🇾": None,
    "🇭🇹": None,
    "🇭🇳": None,
    "🇭🇰": None,
    "🇭🇺": ["hu"],
    "🇮🇸": ["is"],
    "🇮🇳": ["hi", "lus"],
    "🇮🇩": ["id"],
    "🇮🇷": None,
    "🇮🇶": None,
    "🇮🇪": ["ga"],
    "🇮🇲": None,
    "🇮🇱": ["iw"],
    "🇮🇹": ["it"],
    "🇯🇲": None,
    "🇯🇵": ["ja"],
    "🇯🇪": None,
    "🇯🇴": None,
    "🇰🇿": ["kk"],
    "🇰🇪": None,
    "🇰🇮": None,
    "🇽🇰": None,
    "🇰🇼": None,
    "🇰🇬": None,
    "🇱🇦": None,
    "🇱🇻": ["lv"],
    "🇱🇧": None,
    "🇱🇸": None,
    "🇱🇷": None,
    "🇱🇾": None,
    "🇱🇮": None,
    "🇱🇹": ["lt"],
    "🇱🇺": ["lb"],
    "🇲🇴": None,
    "🇲🇰": ["mk"],
    "🇲🇬": None,
    "🇲🇼": None,
    "🇲🇾": None,
    "🇲🇻": None,
    "🇲🇱": None,
    "🇲🇹": None,
    "🇲🇭": None,
    "🇲🇶": None,
    "🇲🇷": None,
    "🇲🇺": None,
    "🇾🇹": None,
    "🇲🇽": ["es"],
    "🇫🇲": None,
    "🇲🇩": ["ro"],
    "🇲🇨": None,
    "🇲🇳": None,
    "🇲🇪": None,
    "🇲🇸": None,
    "🇲🇦": None,
    "🇲🇿": None,
    "🇲🇲": None,
    "🇳🇦": None,
    "🇳🇷": None,
    "🇳🇵": None,
    "🇳🇱": "nl",
    "🇳🇨": None,
    "🇳🇿": None,
    "🇳🇮": None,
    "🇳🇪": None,
    "🇳🇬": None,
    "🇳🇺": None,
    "🇳🇫": None,
    "🇰🇵": ["ko"],
    "🇲🇵": None,
    "🇳🇴": ["no"],
    "🇴🇲": None,
    "🇵🇰": None,
    "🇵🇼": None,
    "🇵🇸": None,
    "🇵🇦": None,
    "🇵🇬": None,
    "🇵🇾": None,
    "🇵🇪": None,
    "🇵🇭": None,
    "🇵🇳": None,
    "🇵🇱": ["pl"],
    "🇵🇹": ["pt"],
    "🇵🇷": None,
    "🇶🇦": None,
    "🇷🇪": None,
    "🇷🇴": ["ro"],
    "🇷🇺": ["ru"],
    "🇷🇼": None,
    "🇼🇸": None,
    "🇸🇲": None,
    "🇸🇹": None,
    "🇸🇦": None,
    "🇸🇳": None,
    "🇷🇸": ["sr"],
    "🇸🇨": None,
    "🇸🇱": None,
    "🇸🇬": None,
    "🇸🇽": None,
    "🇸🇰": ["sk"],
    "🇸🇮": None,
    "🇬🇸": None,
    "🇸🇧": None,
    "🇸🇴": None,
    "🇿🇦": None,
    "🇰🇷": ["ko"],
    "🇸🇸": None,
    "🇪🇸": ["es"],
    "🇱🇰": None,
    "🇧🇱": None,
    "🇸🇭": None,
    "🇰🇳": None,
    "🇱🇨": None,
    "🇵🇲": None,
    "🇻🇨": None,
    "🇸🇩": None,
    "🇸🇷": None,
    "🇸🇿": None,
    "🇸🇪": ["sv"],
    "🇨🇭": ["de", "fr", "it"],
    "🇸🇾": None,
    "🇹🇼": None,
    "🇹🇯": None,
    "🇹🇿": None,
    "🇹🇭": None,
    "🇹🇱": None,
    "🇹🇬": None,
    "🇹🇰": None,
    "🇹🇴": None,
    "🇹🇹": None,
    "🇹🇳": None,
    "🇹🇷": None,
    "🇹🇲": None,
    "🇹🇨": None,
    "🇻🇮": None,
    "🇹🇻": None,
    "🇺🇬": None,
    "🇺🇦": ["uk"],
    "🇦🇪": None,
    "🇬🇧": ["en"],
    "🇺🇸": ["en"],
    "🇺🇾": ["es"],
    "🇺🇿": ["uz"],
    "🇻🇺": None,
    "🇻🇦": None,
    "🇻🇪": None,
    "🇻🇳": ["vi"],
    "🇼🇫": None,
    "🇪🇭": None,
    "🇾🇪": None,
    "🇿🇲": None,
    "🇿🇼": None,
    "🇦🇨": None,
    "🇧🇻": None,
    "🇨🇵": None,
    "🇪🇦": None,
    "🇩🇬": None,
    "🇭🇲": None,
    "🇲🇫": None,
    "🇸🇯": None,
    "🇹🇦": None,
    "🇺🇲": None,
}


def translateToEmoji(text, emoji):
    if langs[emoji] is not None:
        if len(langs[emoji]) == 1 or len(text) > 1000:
            return GoogleTranslator(source='auto', target=langs[emoji][0]).translate(text)
        else:
            translated = ""
            for language in langs[emoji]:
                response = GoogleTranslator(source='auto', target=language).translate(text)
                key = list(filter(lambda x: constants.GOOGLE_LANGUAGES_TO_CODES[x] == language,
                                  constants.GOOGLE_LANGUAGES_TO_CODES))[0]
                response = f'`{key.capitalize()}` ' + response
                if len(response) + len(translated) >= 1990:
                    continue
                else:
                    translated += "\n" + response
            return translated
    else:
        return f'I can\'t from this language yet!'


def translateToLang(text, lang):
    return GoogleTranslator(source='auto', target=lang).translate(text)
