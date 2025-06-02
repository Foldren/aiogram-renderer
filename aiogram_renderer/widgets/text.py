from typing import Any
from .widget import Widget


class Text(Widget):
    __slots__ = ("content", "end", "end_count")

    def __init__(self, content: str, end: str = "\n", end_count: int = 0, show_on: str = None):
        # Добавляем окончание, в зависимости от end_count
        self.content = content
        self.end = end
        self.end_count = end_count
        super().__init__(show_on=show_on)

    async def assemble(self, data: dict[str, Any]) -> str:
        if not (await self.is_show_on(data)):
            return ""

        text = self.content
        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            if "{" + key + "}" in text:
                text = text.replace("{" + key + "}", str(value))

        return text + "".join([self.end for _ in range(self.end_count)])


class Area(Widget):
    __slots__ = ('texts', 'sep', 'sep_count', 'end', 'end_count')

    def __init__(self, *texts: Text | str, sep: str = "\n", sep_count: int = 1, end: str = "\n",
                 end_count: int = 0, show_on: str = None):
        self.texts = list(texts)
        self.sep = sep
        self.sep_count = sep_count
        self.end = end
        self.end_count = end_count
        super().__init__(show_on=show_on)

    async def assemble(self, data: dict[str, Any]):
        if not (await self.is_show_on(data)):
            return ""

            # Формируем разделители, учитывая их количество и после содержимое
        separators = "".join([self.sep for _ in range(self.sep_count)])

        texts_list = []
        for text in self.texts:
            # Если это виджет
            if isinstance(text, Text):
                # Если when в ключах data, то делаем проверку
                if text.show_on in data.keys():
                    # Если when = False, не собираем text
                    if not data[text.show_on]:
                        continue
                asm_text = await text.assemble(data=data)
                texts_list.append(asm_text + separators)
            # Если это строка
            else:
                # Форматируем по data, если там заданы ключи {key}
                for key, value in data.items():
                    if "{" + key + "}" in text:
                        text = text.replace("{" + key + "}", str(value))

                texts_list.append(text + separators)

        # Если все тексты скрыты выдаем пустую строку
        if len(texts_list) == 0:
            return ""
        # В другом случае разделяем контент сепараторами и добавляем end
        else:
            content = "".join(texts_list)[:-self.sep_count] + "".join([self.end for _ in range(self.end_count)])

        return content


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


class Progress(Widget):
    __slots__ = ('name', 'load', 'no_load', 'add_percent', 'postfix', 'prefix')

    def __init__(self, name: str, load: str = "🟥", no_load: str = "⬜",
                 add_percent: bool = False, prefix: str = "", postfix: str = "", show_on: str = None):
        """
        Текстовый виджет для отображения прогресс бара
        :param name: название прогресс бара
        :param load: символ для загруженной части прогресс бара
        :param no_load: символ для не загруженной части прогресс бара
        :param add_percent: флаг для добавления постфикса с процентами
        :return:
        """
        assert (len(load) == 1) and (len(no_load) == 1), ValueError("Задайте параметры load и no_load")
        self.name = name
        self.load = load
        self.no_load = no_load
        self.add_percent = add_percent
        self.postfix = postfix
        self.prefix = prefix
        super().__init__(show_on=show_on)

    async def assemble(self, data: dict[str, Any]):
        if not (await self.is_show_on(data)):
            return ""

        percent = data[self.name] if self.name in data else 0
        assert 0.0 <= percent <= 100.0, ValueError("Процент должен быть в промежутке от 0 до 100")
        # Форматируем процент убирая 0.0, 100.0 и добавляя постфикс, если он задан
        percent = 0 if percent == 0.0 else 100 if percent == 100.0 else percent
        percents_postfix = f" {percent}%" if self.add_percent else ""

        # Собираем линию загрузки по проценту
        format_percent = 0 if percent == 0 else max(int(percent) // 10, 1)
        list_load = [self.load for i_l in range(format_percent)]
        list_no_load = [self.no_load for i_nl in range(10 - len(list_load))]
        progress_bar = "".join(list_load) + "".join(list_no_load)

        return self.prefix + progress_bar + percents_postfix + self.postfix
