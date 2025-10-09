from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_renderer.example.windows import alert_mode, main_window
from aiogram_renderer.components.filters import IsMode
from aiogram_renderer.renderer import Renderer
from states import MenuStates
from aiofiles import open as aioopen

router = Router()
router.message.filter(F.chat.type == "private")
router.callback_query.filter(F.message.chat.type == "private")


@router.message(F.text.in_({"/start", "/restart"}))
async def start(message: Message, renderer: Renderer):
    data = {"test_radio": "Radio1", "Panel1": 1}
    await renderer.answer(window=main_window, event=message, data=data)


@router.callback_query(F.data.startswith("__radio__"))
async def press_radio_btn(callback: CallbackQuery, state: FSMContext, renderer: Renderer):
    print(1)
    # group_name = callback.data.split(":")[1]
    # btn_text = callback.data.split(":")[2]
    # has_custom_handler = int(callback.data.split(":")[3])
    #
    # if has_custom_handler:
    #     return
    #
    # fsm_data = await state.get_data()
    # w_state = await state.get_state()
    #
    # # Устанавливаем новую активную страницу в группе
    # fsm_data["__windows__"][w_state][group_name] = btn_text
    # await state.set_data(fsm_data)
    #
    # await renderer.edit(window=w_state, event=callback)

    # data = {"username": f" {message.from_user.username}" if message.from_user else "",
    #         "test_show_on": False,
    #         'test_pr': 0,
    #         "path": "test23225",
    #         'filename': 'test.png',
    #         "test_dg": {
    #             "page": 2,
    #             "text": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"],
    #             "data": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]},
    #         "test_dg2": {
    #             "page": 2,
    #             "text": ["3", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"],
    #             "data": ["3", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]}}
    #
    # async with aioopen(file="test.png", mode="rb") as f:
    #     message2, window = await renderer.answer(
    #         window=MenuStates.main1,
    #         chat_id=message.chat.id,
    #         data=data,
    #         file_bytes={'test_fb': await f.read()}
    #     )

        # for i in range(99):
        #     await renderer.update_progress(window=MenuStates.main1, chat_id=message2.chat.id, interval=0.3,
        #                                    message_id=message2.message_id, name="test_pr", percent=i, data=data)
        #     await sleep(0.3)


# @router.callback_query(IsMode("decoder_h263"))
# async def start2(callback: CallbackQuery, state: FSMContext, renderer: Renderer):
#     print(1)
#     mode_name = callback.data.replace("__mode__:", "")
#     # Переключаем режим
#     await renderer.bot_modes.update_mode(mode=mode_name)
#     # Для InilineButtonMode бот просто отредактирует окно
#     await renderer.edit(window=await state.get_state(),
#                         chat_id=callback.message.chat.id,
#                         message_id=callback.message.message_id)


# @router.message(IsMode("decoder_h2"))
# async def start3(message: Message, state: FSMContext, renderer: Renderer):
#     print(2)
#     mode = await renderer.bot_modes.get_mode_by_value(value=message.text)
#     await renderer.bot_modes.update_mode(mode=mode.name)
#     # Для ReplyButtonMode бот отправит окно с уведомлением
#     await renderer.render(window=alert_mode, chat_id=message.chat.id)
#     await message.delete()
