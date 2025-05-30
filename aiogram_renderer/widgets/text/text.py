from typing import Any
from aiogram_renderer.widgets import Widget


class Text(Widget):
    __slots__ = ("content", "end", "end_count")

    def __init__(self, content: str, end: str = "\n", end_count: int = 0, show_on: str = None):
        # Добавляем окончание, в зависимости от end_count
        self.content = content
        self.end = end
        self.end_count = end_count
        super().__init__(show_on=show_on)

    async def assemble(self, data: dict[str, Any]) -> str:
        if self.show_on in data.keys():
            # Если show_on = False, не собираем текст и возвращаем пустую строку
            if not data[self.show_on]:
                return ""

        text = self.content
        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            if "{" + key + "}" in text:
                text = text.replace("{" + key + "}", str(value))

        return text + "".join([self.end for _ in range(self.end_count)])


class Bold(Text):
    __slots__ = ()

    def __init__(self, content: str, end: str = "\n", end_count: int = 0, show_on: str = None):
        super().__init__(content=f"<b>{content}</b>", end=end, end_count=end_count, show_on=show_on)


class Italic(Text):
    __slots__ = ()

    def __init__(self, content: str, end: str = "\n", end_count: int = 0, show_on: str = None):
        super().__init__(content=f"<i>{content}</i>", end=end, end_count=end_count, show_on=show_on)


class Code(Text):
    __slots__ = ()

    def __init__(self, content: str, end: str = "\n", end_count: int = 0, show_on: str = None):
        super().__init__(content=f"<code>{content}</code>", end=end, end_count=end_count, show_on=show_on)


class Underline(Text):
    __slots__ = ()

    def __init__(self, content: str, end: str = "\n", end_count: int = 0, show_on: str = None):
        super().__init__(content=f"<u>{content}</u>", end=end, end_count=end_count, show_on=show_on)


class Blockquote(Text):
    __slots__ = ()

    def __init__(self, content: str, end: str = "\n", end_count: int = 0, show_on: str = None):
        super().__init__(content=f"<blockquote>{content}</blockquote>", end=end, end_count=end_count, show_on=show_on)
