from typing import Any
from aiogram_renderer.widgets import Widget
from aiogram_renderer.widgets.text import Text

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
        if self.show_on in data.keys():
            if not data[self.show_on]:
                return ""

        separators = "".join([self.sep for _ in range(self.sep_count)])

        texts_list = []
        for text in self.texts:
            if isinstance(text, Text):
                if text.show_on in data.keys():
                    if not data[text.show_on]:
                        continue
                asm_text = await text.assemble(data=data)
                texts_list.append(asm_text + separators)
            else:
                for key, value in data.items():
                    if "{" + key + "}" in text:
                        text = text.replace("{" + key + "}", str(value))
                texts_list.append(text + separators)

        if len(texts_list) == 0:
            return ""
        else:
            content = "".join(texts_list)[:-self.sep_count] + "".join([self.end for _ in range(self.end_count)])

        return content
