from aiogram import BaseMiddleware
from typing import Any, Callable
from aiogram.fsm.context import FSMContext
from aiogram.types import Update
from aiogram_renderer.bot_mode import BotModes, BotMode
from aiogram_renderer.renderer import Renderer
from aiogram_renderer.window import Window


class RendererMiddleware(BaseMiddleware):
    def __init__(self, windows: list[Window] = None, modes: list[BotMode] = None):
        self.windows = windows
        self.modes = modes

    async def __call__(self, handler: Callable, event: Update, data: dict[str, Any]) -> Any:
        # Если есть FSMContext, то передаем его в renderer и bot_modes
        for key, value in data.items():
            if isinstance(value, FSMContext):
                bot_modes = BotModes(*self.modes, fsm=value) if (self.modes is not None) else None
                renderer = Renderer(event=event, fsm=value, windows=self.windows, bot_modes=bot_modes)
                data["renderer"] = renderer
                result = await handler(event, data)
                del renderer
                return result

        result = await handler(event, data)
        return result
