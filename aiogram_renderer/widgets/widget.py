from abc import ABC, abstractmethod
from typing import Any


class Widget(ABC):
    __slots__ = ("show_on",)

    def __init__(self, show_on: str = None):
        self.show_on = show_on

    @abstractmethod
    async def assemble(self, *args, **kwargs):
        pass

    async def is_show_on(self, data: dict[str, Any]) -> bool:
        if self.show_on is not None:
            clear_show_on = self.show_on.replace("!", "")
            if clear_show_on in data.keys():
                if (self.show_on[0] != "!") and (not data[clear_show_on]):
                    return False
                elif (self.show_on[0] == "!") and (data[clear_show_on]):
                    return False
            else:
                return False
        return True
