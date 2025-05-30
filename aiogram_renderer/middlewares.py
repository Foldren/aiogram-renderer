from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .bot_mode import BotModes, BotMode
from .renderer import Renderer
from .window import Window


class RendererMiddleware(BaseMiddleware):
    def __init__(self, windows: list[Window] = None, modes: list[BotMode] = None):
        self.windows = windows
        self.modes = modes

    async def __call__(self, handler: Callable, event: Message, data: dict[str, Any]) -> Any:
        # Если есть FSMContext, то передаем его в renderer и bot_modes
        if (fsm := data.get('state')) is not None:
            data["renderer"] = Renderer(
                bot=event.bot,
                fsm=fsm,
                windows=self.windows,
                bot_modes=BotModes(*self.modes, fsm=fsm) if (self.modes is not None) else None)

        return await handler(event, data)
