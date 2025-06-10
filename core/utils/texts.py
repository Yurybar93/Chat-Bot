from locales import en, de, ru

LANGUAGE_MAP = {
    "en": en.texts,
    "de": de.texts,
    "ru": ru.texts
}

DEFAULT_LANGUAGE = "en"

def get_text(key: str, lang: str = DEFAULT_LANGUAGE) -> str:
    return LANGUAGE_MAP.get(lang, LANGUAGE_MAP[DEFAULT_LANGUAGE]).get(
        key, f"[missing: {key}]"
    )
