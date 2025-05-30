from typing import Any
from aiogram.types import KeyboardButton
from aiogram_renderer.widgets import Widget


class ReplyButton(Widget):
    __slots__ = ("text",)

    def __init__(self, text: str, show_on: str = None):
        self.text = text
        super().__init__(show_on=show_on)

    async def assemble(self, data: dict[str, Any], **kwargs) -> KeyboardButton | None:
        if self.show_on in data.keys():
            # Если when = False, не собираем кнопку и возвращаем None
            if not data[self.show_on]:
                return None

        text = self.text

        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            if "{" + key + "}" in text:
                text = text.replace("{" + key + "}", str(value))

        return KeyboardButton(text=text)


class ReplyMode(ReplyButton):
    __slots__ = ("name",)

    def __init__(self, name: str, show_on: str = None):
        """
        Виджет режима бота на ReplyKeyboard, на вход задаем название режима, который хоти видеть,
        стоит учесть что при переключении режима Mode - ReplyMode не будет меняться,
        для этого вам нужно писать свой хендлер и доп. логику
        :param name: название режима
        :param show_on: фильтр видимости виджета
        """
        self.name = name
        # Для обработки используется системный хендлер с bot.modes.values
        super().__init__(text=name, show_on=show_on)

    async def assemble(self, data: dict[str, Any], **kwargs):
        """
        Берем активное [0] значение режима из fsm
        :param data: данные окна
        """
        if self.show_on in data.keys():
            # Если when = False, не собираем кнопку и возвращаем None
            if not data[self.show_on]:
                return None

        text = kwargs["modes"][self.name][0]
        return KeyboardButton(text=text)
