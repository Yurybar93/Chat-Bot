from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.texts import get_text
from utils.keyboards import get_language_keyboard
from config import DEFAULT_LANGUAGE
import logging

router = Router()

language_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=get_text("language_english", DEFAULT_LANGUAGE))],
        [types.KeyboardButton(text=get_text("language_german", DEFAULT_LANGUAGE))],
        [types.KeyboardButton(text=get_text("language_russian", DEFAULT_LANGUAGE))]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    logger = logging.getLogger(__name__)
    logger.info(f"Received /start command from user {message.from_user.id}")

    await state.clear()

    await message.answer(
        get_text("start_message", DEFAULT_LANGUAGE),
        reply_markup=get_language_keyboard()
    )
    await message.answer(
        get_text("choose_language", DEFAULT_LANGUAGE),
        reply_markup=get_language_keyboard()
    )
