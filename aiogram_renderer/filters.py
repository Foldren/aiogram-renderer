from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from .callback_data import ModeCD
from .renderer import Renderer


class IsModeWithNotCustomHandler(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery, renderer: Renderer) -> bool:
        bot_modes = renderer.bot_modes
        if not bot_modes: # Если режимы не заданы
            return False

        mode = None
        # Для CallbackQuery проверяем правильно ли задан callback_data по системному префиксу
        if isinstance(event, CallbackQuery):
            try:
                callback_data = ModeCD.unpack(event.data)
                mode = await bot_modes.get_mode_by_name(name=callback_data.name) if callback_data else None
            except (TypeError, ValueError):
                pass
        elif isinstance(event, Message): # Ищем его среди списков значений модов и выводим по найденному названию мода
            modes_values = await bot_modes.get_modes_values()
            if event.text in modes_values:
                mode = await bot_modes.get_mode_by_value(value=event.text)

        return bool(mode and not mode.has_custom_handler)


class IsMode(BaseFilter):
    def __init__(self, name: str):
        self.name = name

    async def __call__(self, event: Message | CallbackQuery, renderer: Renderer) -> bool:
        bot_modes = renderer.bot_modes
        if not bot_modes: # Если режимы не заданы
            return False

        dict_modes = await bot_modes.get_dict_modes()
        if self.name not in dict_modes:
            raise ValueError("Такого режима нет")

        mode = await bot_modes.get_mode_by_name(name=self.name)
        if not mode:
            return False

        if isinstance(event, CallbackQuery):
            # Проверяем равен ли сallback заданному режиму
            return event.data == ModeCD(name=self.name).pack()
        elif isinstance(event, Message):
            # Проверяем есть ли значение Reply text в values режима
            return event.text in mode.values

        return False
