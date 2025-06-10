from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.utils.texts import get_text
from core.utils.keyboards import get_language_keyboard
from config import DEFAULT_LANGUAGE
import logging

router = Router()

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

