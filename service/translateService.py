from deep_translator import GoogleTranslator, constants

# this is the dictionary of discord emojis to languages in Google Translate
langs = {
    "🇦🇫": ["ps"],
    "🇦🇽": ["sw"],
    "🇦🇱": ["sq"],
    "🇩🇿": ["ar"],
    "🇦🇸": ["sm", "en"],
    "🇦🇩": ["ca"],
    "🇦🇴": ["pt"],
    "🇦🇮": ["en"],
    "🇦🇶": "Yes Rico, Kaboom!",
    "🇦🇬": ["en"],
    "🇦🇷": ["es"],
    "🇦🇲": ["hy"],
    "🇦🇼": ["nl", "en", "es"],
    "🇦🇺": ["en"],
    "🇦🇹": ["de"],
    "🇦🇿": ["az"],
    "🇧🇸": ["en"],
    "🇧🇭": ["ar"],
    "🇧🇩": ["bn"],
    "🇧🇧": ["en"],
    "🇧🇾": ["be"],
    "🇧🇪": ["nl", "fr", "de"],
    "🇧🇿": ["kr"],
    "🇧🇯": ["yo"],
    "🇧🇲": ["en"],
    "🇧🇹": ["ne"],
    "🇧🇴": ["es"],
    "🇧🇦": ["bs"],
    "🇧🇼": ["en"],
    "🇧🇷": ["pt"],
    "🇮🇴": ["en"],
    "🇻🇬":["en"],
    "🇧🇳": ["ms"],
    "🇧🇬": ["bg"],
    "🇧🇫": ["fr"],
    "🇧🇮": ["fr", "en"],
    "🇰🇭": ["km"],
    "🇨🇲": ["fr", "en"],
    "🇨🇦": ["fr", "en"],
    "🇮🇨": ["fr", "en"],
    "🇨🇻": ["pg"],
    "🇧🇶": ["en"],
    "🇰🇾": ["en"],
    "🇨🇫": ["fr"],
    "🇹🇩": ["ar", "fr"],
    "🇨🇱": ["es"],
    "🇨🇳": ["zh-CN", "zh-TW"],
    "🇨🇽": ["en"],
    "🇨🇨": ["ma"],
    "🇨🇴": ["es"],
    "🇰🇲": ["en", "ar"],
    "🇨🇬": ["ln", "sw"],
    "🇨🇩": ["ln", "sw"],
    "🇨🇰": ["en"],
    "🇨🇷": ["es"],
    "🇨🇮": ["fr"],
    "🇭🇷": ["hr"],
    "🇨🇺": ["es", "ht"],
    "🇨🇼": ["en"],
    "🇨🇾": ["el", "tr"],
    "🇨🇿": ["cs"],
    "🇩🇰": ["da"],
    "🇩🇯": ["fr", "ar"],
    "🇩🇲": ["en"],
    "🇩🇴": ["es"],
    "🇪🇨": ["es", "qu"],
    "🇪🇬": ["ar"],
    "🇸🇻": ["es"],
    "🇬🇶": ["es", "pt", "fr"],
    "🇪🇷": ["ti"],
    "🇪🇪": ["et"],
    "🇪🇹": ["am", "om", "so", "ti"],
    "🇫🇰": ["en"],
    "🇫🇴": ["da"],
    "🇫🇯": ["en"],
    "🇫🇮": ["fi"],
    "🇫🇷": ["fr"],
    "🇬🇫": ["fr"],
    "🇵🇫": ["fr"],
    "🇹🇫": ["fr"],
    "🇬🇦": ["fr"],
    "🇬🇲": ["en"],
    "🇬🇪": ["ka"],
    "🇩🇪": ["de"],
    "🇬🇭": ["en"],
    "🇬🇮": ["en", "es"],
    "🇬🇷": ["el"],
    "🇬🇱": ["da"],
    "🇬🇩": ["en"],
    "🇬🇵": ["fr"],
    "🇬🇺": ["en", "tl"],
    "🇬🇹": ["es"],
    "🇬🇬": ["en"],
    "🇬🇳": ["fr"],
    "🇬🇼": ["pt"],
    "🇬🇾": ["en"],
    "🇭🇹": ["ht"],
    "🇭🇳": ["es"],
    "🇭🇰": ["zh-CN", "zh-TW", "en"],
    "🇭🇺": ["hu"],
    "🇮🇸": ["is"],
    "🇮🇳": ["hi", "lus"],
    "🇮🇩": ["id"],
    "🇮🇷": ["fa"],
    "🇮🇶": ["ar", "ku"],
    "🇮🇪": ["ga"],
    "🇮🇲": ["en"],
    "🇮🇱": ["iw"],
    "🇮🇹": ["it"],
    "🇯🇲": ["en"],
    "🇯🇵": ["ja"],
    "🇯🇪": ["en", "fr"],
    "🇯🇴": ["ar"],
    "🇰🇿": ["kk"],
    "🇰🇪": ["sw"],
    "🇰🇮": ["en"],
    "🇽🇰": ["sq", "sr"],
    "🇰🇼": ["ar"],
    "🇰🇬": ["ky"],
    "🇱🇦": ["lo"],
    "🇱🇻": ["lv"],
    "🇱🇧": ["ar"],
    "🇱🇸": ["st", "zu"],
    "🇱🇷": ["en"],
    "🇱🇾": ["ar"],
    "🇱🇮": ["de"],
    "🇱🇹": ["lt"],
    "🇱🇺": ["lb"],
    "🇲🇴": ["zh-CN", "zh-TW", "pt"],
    "🇲🇰": ["mk"],
    "🇲🇬": ["mg"],
    "🇲🇼": ["en", "ny"],
    "🇲🇾": ["ms"],
    "🇲🇻": ["dv"],
    "🇲🇱": ["bm"],
    "🇲🇹": ["mt"],
    "🇲🇭": ["en"],
    "🇲🇶": ["fr"],
    "🇲🇷": ["ar"],
    "🇲🇺": ["fr", "bho"],
    "🇾🇹": ["fr"],
    "🇲🇽": ["es"],
    "🇫🇲": ["en"],
    "🇲🇩": ["ro"],
    "🇲🇨": ["fr"],
    "🇲🇳": ["mn"],
    "🇲🇪": ["sr", "hr", "bs", "sq"],
    "🇲🇸": ["en"],
    "🇲🇦": ["ar"],
    "🇲🇿": ["pt"],
    "🇲🇲": ["my"],
    "🇳🇦": ["en"],
    "🇳🇷": ["en"],
    "🇳🇵": ["ne"],
    "🇳🇱": ["nl"],
    "🇳🇨": ["fr"],
    "🇳🇿": ["mr"],
    "🇳🇮": ["es"],
    "🇳🇪": ["fr"],
    "🇳🇬": ["en"],
    "🇳🇺": ["en"],
    "🇳🇫": ["en"],
    "🇰🇵": ["ko"],
    "🇲🇵": ["en"],
    "🇳🇴": ["no"],
    "🇴🇲": ["ar"],
    "🇵🇰": ["ps", "sd", "ur", "fa"],
    "🇵🇼": ["en"],
    "🇵🇸": ["ar"],
    "🇵🇦": ["es"],
    "🇵🇬": ["en"],
    "🇵🇾": ["gn"],
    "🇵🇪": ["es", "ay"],
    "🇵🇭": ["tl"],
    "🇵🇳": ["en"],
    "🇵🇱": ["pl"],
    "🇵🇹": ["pt"],
    "🇵🇷": ["es", "en"],
    "🇶🇦": ["ar"],
    "🇷🇪": ["fr"],
    "🇷🇴": ["ro"],
    "🇷🇺": ["ru"],
    "🇷🇼": ["rw"],
    "🇼🇸": ["sm"],
    "🇸🇲": ["it"],
    "🇸🇹": ["pt"],
    "🇸🇦": ["ar"],
    "🇸🇳": ["fr", "ar"],
    "🇷🇸": ["sr"],
    "🇸🇨": ["fr", "en"],
    "🇸🇱": ["en"],
    "🇸🇬": ["en", "ta"],
    "🇸🇽": ["en"],
    "🇸🇰": ["sk"],
    "🇸🇮": ["sl"],
    "🇬🇸": ["en"],
    "🇸🇧": ["en"],
    "🇸🇴": ["so"],
    "🇿🇦": ["en", "af"],
    "🇰🇷": ["ko"],
    "🇸🇸": ["en"],
    "🇪🇸": ["es"],
    "🇱🇰": ["si", "ta"],
    "🇧🇱": ["fr"],
    "🇸🇭": ["en"],
    "🇰🇳": ["en"],
    "🇱🇨": ["en"],
    "🇵🇲": ["fr"],
    "🇻🇨": ["en"],
    "🇸🇩": ["ar", "en"],
    "🇸🇷": ["nl"],
    "🇸🇿": ["en"],
    "🇸🇪": ["sv"],
    "🇨🇭": ["de", "fr", "it"],
    "🇸🇾": ["ar", "ku", "tr"],
    "🇹🇼": ["zh-CN", "zh-TW"],
    "🇹🇯": ["tg"],
    "🇹🇿": ["en"],
    "🇹🇭": ["th"],
    "🇹🇱": ["pt"],
    "🇹🇬": ["fr"],
    "🇹🇰": ["en"],
    "🇹🇴": ["en"],
    "🇹🇹": ["en"],
    "🇹🇳": ["ar"],
    "🇹🇷": ["tr"],
    "🇹🇲": ["tk"],
    "🇹🇨": ["en"],
    "🇻🇮": ["en"],
    "🇹🇻": ["en"],
    "🇺🇬": ["en"],
    "🇺🇦": ["uk"],
    "🇦🇪": ["ar"],
    "🇬🇧": ["en"],
    "🇺🇸": ["en"],
    "🇺🇾": ["es"],
    "🇺🇿": ["uz"],
    "🇻🇺": ["en", "fr"],
    "🇻🇦": ["la"],
    "🇻🇪": ["es"],
    "🇻🇳": ["vi"],
    "🇼🇫": ["fr"],
    "🇪🇭": ["ar", "es"],
    "🇾🇪": ["ar"],
    "🇿🇲": ["ts"],
    "🇿🇼": ["ny"],
    "🇦🇨": ["en"],
    "🇧🇻": "Bouvet Island is uninhabited",
    "🇨🇵": ["fr"],
    "🇪🇦": ["es"],
    "🇩🇬": ["en"],
    "🇭🇲": ["en"],
    "🇲🇫": ["fr"],
    "🇸🇯": ["no"],
    "🇹🇦": ["en"],
    "🇺🇲": ["en"],
}


def translateToEmoji(text, emoji):
    if langs[emoji] is not None:
        if isinstance(langs[emoji], str):
            return langs[emoji]
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
