from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from aiogram_renderer.callback_data import DPanelCD, ModeCD, ComeToCD
from aiogram_renderer.filters import IsModeWithNotCustomHandler
from aiogram_renderer.renderer import Renderer

router = Router()

# Можно использовать __disable__, __delete__
# А вот эти не стоит использовать
RESERVED_CONTAIN_CALLBACKS = ("__mode__", "__dpanel__", "__cometo__")


@router.callback_query(ComeToCD.filter())
async def come_to_window(callback: CallbackQuery, callback_data: ComeToCD, renderer: Renderer):
    await renderer.edit(window=f"{callback_data.group}:{callback_data.state}", chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@router.callback_query(F.data == "__disable__")
async def answer_disable_button(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == "__delete__")
async def delete_callback_message(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(IsModeWithNotCustomHandler())
async def update_mode(callback: CallbackQuery, callback_data: ModeCD, state: FSMContext, renderer: Renderer):
    # Переключаем режим
    await renderer.bot_modes.update_mode(mode=callback_data.name)
    # Для InilineButtonMode бот просто отредактирует окно
    await renderer.edit(window=await state.get_state(),
                        chat_id=callback.message.chat.id,
                        message_id=callback.message.message_id)


@router.callback_query(DPanelCD.filter())
async def switch_dynamic_panel_page(callback: CallbackQuery, callback_data: DPanelCD, state: FSMContext, renderer: Renderer):
    message = callback.message
    w_state = await state.get_state()

    await renderer._switch_dynamic_panel_page(name=callback_data.panel_name, page=callback_data.page)
    await renderer.edit(window=w_state, chat_id=message.chat.id, message_id=message.message_id)
