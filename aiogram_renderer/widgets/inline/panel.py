from typing import Any
from aiogram.types import InlineKeyboardButton
from aiogram_renderer.widgets.inline.button import Button
from aiogram_renderer.widgets.widget import Widget


class Panel(Widget):
    __slots__ = ("buttons", "width")

    def __init__(self, *buttons: Button, width: int = 1, show_on: str = None):
        # Минимальная ширина 1
        assert width >= 1, ValueError("Ширина группы должна быть не меньше 1")
        # Максимальная ширина inlineKeyboard строки 8 (ограничение Telegram)
        assert width <= 8, ValueError("У Telegram ограничение на длину InlineKeyboard - 8 кнопок")
        # Максимальная высота inlineKeyboard 100 (ограничение Telegram)
        assert len(buttons) / width <= 100, ValueError("У Telegram ограничение на высоту InlineKeyboard - 100 кнопок")
        self.buttons = list(buttons)
        self.width = width
        super().__init__(show_on=show_on)

    async def assemble(self, data: dict[str, Any], **kwargs) -> list[list[InlineKeyboardButton]]:
        if not (await self.is_show_on(data)):
            return [[]]

        # Собираем объект группы кнопок Telegram
        buttons_rows = [[]]
        k = 0
        j = 0
        for button in self.buttons:
            # Если when в ключах data, то делаем проверку
            if button.show_on in data.keys():
                # Если when = False, не собираем кнопку
                if not data[button.show_on]:
                    continue

            button_obj = await button.assemble(data=data, **kwargs)
            if j % self.width == 0 and j != 0:
                buttons_rows.append([button_obj])
                k += 1
            else:
                buttons_rows[k].append(button_obj)
            j += 1

        return buttons_rows


class Row(Panel):
    __slots__ = ()

    def __init__(self, *buttons: Button, show_on: str = None):
        super().__init__(*buttons, width=len(buttons), show_on=show_on)


class Column(Panel):
    __slots__ = ()

    def __init__(self, *buttons: Button, show_on: str = None):
        super().__init__(*buttons, width=1, show_on=show_on)


class DynamicPanel(Widget):
    __slots__ = ("name", "width", "height", "hide_control_buttons", "hide_number_pages")

    # Формат в fsm_data "name": {"page": 1, "text": ["text1", ...], "data": ["data1", ...]}
    def __init__(self, name: str, width: int = 1, height: int = 1,
                 hide_control_buttons: bool = False, hide_number_pages: bool = False, show_on: str = None):
        # Минимальная ширина и высота = 1
        assert width >= 1, ValueError("Ширина группы должна быть не меньше 1")
        assert height >= 1, ValueError("Высота группы должна быть не меньше 1")
        # Максимальная ширина inlineKeyboard строки 8 (ограничение Telegram)
        assert width <= 8, ValueError("У Telegram ограничение на длину InlineKeyboard - 8 кнопок")
        assert height <= 99, ValueError("У Telegram ограничение на высоту InlineKeyboard - 100 кнопок")

        super().__init__(show_on=show_on)

        self.name = name
        self.width = width
        self.height = height
        self.hide_control_buttons = hide_control_buttons
        self.hide_number_pages = hide_number_pages

    async def assemble(self, data: dict[str, Any], **kwargs) -> list[list[Any]]:
        if not (await self.is_show_on(data)):
            return [[]]

        fsm_group: dict[str, Any] = kwargs["dpanels"][self.name]
        page = fsm_group["page"]

        if len(fsm_group["text"]) != len(fsm_group["data"]):
            raise ValueError("В группе должно быть одинаковое количество text и data")

        count_buttons = len(fsm_group["text"])

        # Добавляем дополнительную страницу если при делении на число кнопок есть остатки
        last_page = count_buttons // (self.width * self.height)
        last_page = last_page + 1 if (count_buttons % (self.width * self.height)) > 0 else last_page

        # Проверяем не задали ли страницу больше чем есть
        if last_page < page:
            raise ValueError(f"У группы нет столько страниц, максимальная: {last_page}")

        # Формируем набор кнопок, начиная с заданной страницы и заканчивая срезом по width, height
        start = self.width * self.height * (page - 1)
        trimmed_b_text = fsm_group["text"][start:start + (self.width * self.height)]
        trimmed_b_data = fsm_group["data"][start:start + (self.width * self.height)]

        buttons = [[]]
        row = 0
        for col, text, data in zip(range(count_buttons), trimmed_b_text, trimmed_b_data):
            button = InlineKeyboardButton(text=text, callback_data=data)

            if col % self.width == 0 and col != 0:
                buttons.append([button])
                row += 1
            else:
                buttons[row].append(button)

        # Формируем кнопки управления
        if (count_buttons > (self.width * self.height)) and (not self.hide_control_buttons):
            if self.hide_number_pages:
                if page == 1:
                    buttons.append([
                        InlineKeyboardButton(text=">", callback_data=f"__dpanel__:{page + 1}:{self.name}"),
                    ])
                elif page == last_page:
                    buttons.append([
                        InlineKeyboardButton(text="<", callback_data=f"__dpanel__:{page - 1}:{self.name}"),
                    ])
                else:
                    buttons.append([
                        InlineKeyboardButton(text="<", callback_data=f"__dpanel__:{page - 1}:{self.name}"),
                        InlineKeyboardButton(text=">", callback_data=f"__dpanel__:{page + 1}:{self.name}"),
                    ])
            else:
                if page == 1:
                    buttons.append([
                        InlineKeyboardButton(text="[ 1 ]", callback_data=f"__disable__"),
                        InlineKeyboardButton(text=">", callback_data=f"__dpanel__:{page + 1}:{self.name}"),
                        InlineKeyboardButton(text=str(last_page), callback_data=f"__dpanel__:{last_page}:{self.name}")
                    ])
                elif page == last_page:
                    buttons.append([
                        InlineKeyboardButton(text="1", callback_data=f"__dpanel__:1:{self.name}"),
                        InlineKeyboardButton(text="<", callback_data=f"__dpanel__:{page - 1}:{self.name}"),
                        InlineKeyboardButton(text=f"[ {last_page} ]", callback_data="__disable__"),
                    ])
                else:
                    buttons.append([
                        InlineKeyboardButton(text="1", callback_data=f"__dpanel__:1:{self.name}"),
                        InlineKeyboardButton(text="<", callback_data=f"__dpanel__:{page - 1}:{self.name}"),
                        InlineKeyboardButton(text=f"[ {page} ]", callback_data="__disable__"),
                        InlineKeyboardButton(text=">", callback_data=f"__dpanel__:{page + 1}:{self.name}"),
                        InlineKeyboardButton(text=str(last_page), callback_data=f"__dpanel__:{last_page}:{self.name}")
                    ])

        return buttons
