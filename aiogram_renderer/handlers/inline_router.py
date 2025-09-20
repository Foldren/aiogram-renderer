from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_renderer.components.filters import IsModeWithNotCustomHandler
from aiogram_renderer.renderer import Renderer

router = Router()

# Можно использовать __disable__, __delete__
# А вот эти не стоит использовать
RESERVED_CONTAIN_CALLBACKS = ("__mode__", "__dpanel__", "__cometo__")


@router.callback_query(F.data.startswith("__cometo__"))
async def come_to_window(callback: CallbackQuery, renderer: Renderer):
    open_state = callback.data.split(":")[1] + ":" + callback.data.split(":")[2]
    mode = callback.data.split(":")[3]
    await renderer.render(window=open_state, mode=mode, event=callback)


@router.callback_query(F.data == "__disable__")
async def answer_disable_button(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == "__delete__")
async def delete_callback_message(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(IsModeWithNotCustomHandler())
async def update_mode(callback: CallbackQuery, state: FSMContext, renderer: Renderer):
    mode_name = callback.data.replace("__mode__:", "")
    # Переключаем режим
    await renderer.bot_modes.update_mode(mode=mode_name)
    # Для InilineButtonMode бот просто отредактирует окно
    await renderer.edit(window=await state.get_state(), event=callback)


@router.callback_query(F.data.startswith("__dpanel__"))
async def switch_dynamic_panel_page(callback: CallbackQuery, state: FSMContext, renderer: Renderer):
    page = int(callback.data.split(":")[1])
    panel_name = callback.data.split(":")[2]
    w_state = await state.get_state()

    await renderer._switch_dynamic_panel_page(name=panel_name, page=page)
    await renderer.edit(window=w_state, event=callback)


@router.callback_query(F.data.endswith("0"), F.data.startswith("__radio__"))
async def press_radio_btn(callback: CallbackQuery, state: FSMContext, renderer: Renderer):
    group_name = callback.data.split(":")[1]
    btn_text = callback.data.split(":")[2]

    fsm_data = await state.get_data()
    w_state = await state.get_state()

    # Проверяем не равно ли значение уже текущему, если да отвечаем, выходим
    if fsm_data["__windows__"][w_state][group_name] == btn_text:
        await callback.answer()
        return

    # Устанавливаем новую активную страницу в группе
    fsm_data["__windows__"][w_state][group_name] = btn_text
    await state.set_data(fsm_data)

    await renderer.edit(window=w_state, event=callback)
