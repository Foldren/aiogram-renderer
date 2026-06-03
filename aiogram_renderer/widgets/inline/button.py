from typing import Any
from aiogram.fsm.state import State
from aiogram.types import InlineKeyboardButton
from pyrogram.types import WebAppInfo

from aiogram_renderer.components.enums import RenderMode
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
    __slots__ = ("mode",)

    def __init__(self, text: str, state: State, mode: RenderMode = RenderMode.EDIT, show_on: str = None):
        super().__init__(text=text, data=f"__cometo__:{state.state}:{mode.value}", show_on=show_on)


class Url(Button):
    __slots__ = ("url", "web_app")

    def __init__(self, text: str, url: str, web_app: bool = False, data: str = None, show_on: str = None):
        self.url = url
        self.web_app = web_app
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

        if self.web_app:
            btn = InlineKeyboardButton(text=text, web_app=WebAppInfo(url=url), callback_data=btn_data)
        else:
            btn = InlineKeyboardButton(text=text, url=url, callback_data=btn_data)

        return btn


class Radio(Button):
    __slots__ = ("group_name", "active_str", "has_custom_handler")

    def __init__(self, text: str, group_name: str, active_str: str = "🔘", has_custom_handler: bool = False,
                 show_on: str = None):
        self.group_name = group_name
        self.active_str = active_str
        super().__init__(text=text, data=f"__radio__:{group_name}:{text}:{int(has_custom_handler)}", show_on=show_on)

    async def assemble(self, data: dict[str, Any], **kwargs) -> Any:
        if not (await self.is_show_on(data)):
            return None

        assert self.group_name in data, ValueError("Нужно задать параметр data[group_name] и указать в нем "
                                                   "активное значение")
        if data[self.group_name] != self.text:
            text = self.text
        else:
            text = self.active_str + " " + self.text

        return InlineKeyboardButton(text=text, callback_data=self.data)
