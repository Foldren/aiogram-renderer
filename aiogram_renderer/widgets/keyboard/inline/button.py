from typing import Any
from aiogram.fsm.state import State
from aiogram.types import InlineKeyboardButton

from aiogram_renderer.callback_data import ComeToCD, ModeCD
from aiogram_renderer.widgets import Widget


class Button(Widget):
    __slots__ = ("text", "data")

    def __init__(self, text: str, data: str, show_on: str = None):
        self.text = text
        self.data = data
        super().__init__(show_on=show_on)

    async def assemble(self, data: dict[str, Any], **kwargs) -> InlineKeyboardButton | None:
        if self.show_on in data.keys():
            # Если when = False, не собираем кнопку и возвращаем None
            if not data[self.show_on]:
                return None

        text = self.text
        btn_data = self.data

        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            if "{" + key + "}" in text:
                text = text.replace("{" + key + "}", str(value))
            if "{" + key + "}" in btn_data:
                btn_data = btn_data.replace("{" + key + "}", str(value))

        return InlineKeyboardButton(text=text, callback_data=btn_data)


class Mode(Button):
    __slots__ = ("name",)

    def __init__(self, name: str, show_on: str = None):
        self.name = name
        super().__init__(text=name, data=ModeCD(name=name).pack(), show_on=show_on)

    async def assemble(self, data: dict[str, Any], **kwargs) -> Any:
        """
        Берем активное [0] значение режима из fsm
        :param data: данные окна
        """
        if self.show_on in data.keys():
            # Если when = False, не собираем кнопку и возвращаем None
            if not data[self.show_on]:
                return None

        text = kwargs["modes"][self.name][0]
        return InlineKeyboardButton(text=text, callback_data=self.data)


class Delete(Button):
    __slots__ = ()

    def __init__(self, text: str, show_on: str = None):
        super().__init__(text=text, data=f"__delete__", show_on=show_on)


class Disable(Button):
    __slots__ = ()

    def __init__(self, text: str, show_on: str = None):
        super().__init__(text=text, data=f"__disable__", show_on=show_on)


class ComeTo(Button):
    __slots__ = ()

    def __init__(self, text: str, state: State, show_on: str = None):
        super().__init__(text=text, data=ComeToCD(group=state.group.__name__, state=state._state).pack(), show_on=show_on)
