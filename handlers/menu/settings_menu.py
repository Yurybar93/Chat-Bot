from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from core.utils.texts import get_text
from core.utils.keyboards import get_language_keyboard
from config import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES

router = Router()

def get_settings_menu(language: str) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=get_text("change_language", language))],
            [types.KeyboardButton(text=get_text("back_to_main_menu", language))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

@router.message(F.text.in_([
    get_text("change_language", lang_code) for lang_code in AVAILABLE_LANGUAGES
]))
async def handle_change_language(message: types.Message, state: FSMContext):
    language = (await state.get_data()).get("language", DEFAULT_LANGUAGE)
    await message.answer(
        get_text("choose_language", language),
        reply_markup=get_language_keyboard()
    )
