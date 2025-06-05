from typing import Any
from aiogram.fsm.state import State
from aiogram.types import InlineKeyboardButton
from aiogram_renderer.widgets.widget import Widget


class Button(Widget):
    __slots__ = ("text", "data")

    def __init__(self, text: str, data: str, show_on: str = None):
        self.text = text
        self.data = data
        super().__init__(show_on=show_on)

    async def assemble(self, data: dict[str, Any], **kwargs) -> InlineKeyboardButton | None:
        if not (await self.is_show_on(data)):
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
        super().__init__(text=name, data=f"__mode__:{name}", show_on=show_on)

    async def assemble(self, data: dict[str, Any], **kwargs) -> Any:
        """
        Берем активное [0] значение режима из fsm
        :param data: данные окна
        """
        if not (await self.is_show_on(data)):
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
        super().__init__(text=text, data=f"__cometo__:{state.state}", show_on=show_on)


class Url(Button):
    __slots__ = ("url",)

    def __init__(self, text: str, url: str, data: str = None, show_on: str = None):
        self.url = url
        super().__init__(text=text, data=data, show_on=show_on)

    async def assemble(self, data: dict[str, Any], **kwargs) -> InlineKeyboardButton | None:
        if not (await self.is_show_on(data)):
            return None

        text = self.text
        btn_data = self.data
        url = self.url

        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            if "{" + key + "}" in text:
                text = text.replace("{" + key + "}", str(value))
            if btn_data is not None:
                if "{" + key + "}" in btn_data:
                    btn_data = btn_data.replace("{" + key + "}", str(value))
            if "{" + key + "}" in url:
                url = url.replace("{" + key + "}", str(value))

        return InlineKeyboardButton(text=text, url=url, callback_data=btn_data)
