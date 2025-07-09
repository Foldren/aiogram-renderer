from aiogram import Router
from aiogram.types import Message
from aiogram_renderer.components.filters import IsModeWithNotCustomHandler
from aiogram_renderer.renderer import Renderer

router = Router()


@router.message(IsModeWithNotCustomHandler())
async def update_mode(event: Message, renderer: Renderer):
    mode = await renderer.bot_modes.get_mode_by_value(value=event.text)
    await renderer.bot_modes.update_mode(mode=mode.name)
    # Для ReplyButtonMode бот отправит окно с уведомлением
    await renderer.render(window=mode.alert_window, chat_id=event.chat.id)
    await event.delete()
