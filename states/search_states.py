from aiogram.fsm.state import StatesGroup, State


class SearchGenreYear(StatesGroup):
    choosing_genre = State()
    choosing_year = State()


class SearchByTitle(StatesGroup):
    waiting_for_title = State()

class SearchByKeyword(StatesGroup):
    waiting_for_keyword = State()