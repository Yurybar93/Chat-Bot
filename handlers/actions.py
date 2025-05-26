from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
import logging
from utils.texts import get_text
from config import DEFAULT_LANGUAGE

router = Router()

LANGUAGES = {
    "en": get_text("language_english", DEFAULT_LANGUAGE),
    "de": get_text("language_german", DEFAULT_LANGUAGE),
    "ru": get_text("language_russian", DEFAULT_LANGUAGE)
}


@router.message(F.text.in_(list(LANGUAGES.values())))
async def set_language(message: types.Message, state: FSMContext):
    logger = logging.getLogger(__name__)
    logger.info(f"User {message.from_user.id} selected language: {message.text}")

    selected_language = message.text
    language_code = next((code for code, lang in LANGUAGES.items() if lang == selected_language), None)

    if language_code:
        await state.update_data(language=language_code)
        await message.answer(get_text("language_set", language_code))
    else:
        await message.answer(get_text("language_not_supported", DEFAULT_LANGUAGE))

    await state.clear()

