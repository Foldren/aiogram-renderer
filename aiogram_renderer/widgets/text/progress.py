from typing import Any
from aiogram_renderer.widgets import Widget

class Progress(Widget):
    __slots__ = ('name', 'load', 'no_load', 'add_percent', 'postfix', 'prefix', 'bar_length')

    def __init__(
        self,
        name: str,
        load: str = "🟥",
        no_load: str = "⬜",
        add_percent: bool = False,
        prefix: str = "",
        postfix: str = "",
        bar_length: int = 10,
        show_on: str = None
    ):
        if len(load) != 1 or len(no_load) != 1:
            raise ValueError("Параметры load и no_load должны быть длиной 1 символ")
        if bar_length < 1:
            raise ValueError("bar_length должен быть положительным целым числом")
        self.name = name
        self.load = load
        self.no_load = no_load
        self.add_percent = add_percent
        self.prefix = prefix
        self.postfix = postfix
        self.bar_length = bar_length
        super().__init__(show_on=show_on)

    async def assemble(self, data: dict[str, Any]) -> str:
        if self.show_on and not data.get(self.show_on, True):
            return ""

        percent = float(data.get(self.name, 0))
        if not (0.0 <= percent <= 100.0):
            raise ValueError("Процент должен быть в промежутке от 0 до 100")

        percent_int = int(round(percent))
        filled_length = int(self.bar_length * percent_int / 100)
        progress_bar = self.load * filled_length + self.no_load * (self.bar_length - filled_length)

        percents_postfix = f" {percent_int}%" if self.add_percent else ""

        return f"{self.prefix}{progress_bar}{percents_postfix}{self.postfix}"
