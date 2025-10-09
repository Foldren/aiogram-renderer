from states import MenuStates
from aiogram_renderer.widgets.inline.button import Mode, ComeTo, Url, Radio, Button
from aiogram_renderer.widgets.inline.panel import DynamicPanel, Panel
from aiogram_renderer.widgets.reply.button import ReplyMode
from aiogram_renderer.widgets.text import Area, Bold, Text, Progress
from aiogram_renderer.window import Window, Alert

main_window = Window(
    Text("👋 Привет<b>{username}</b>, я тест", end_count=2),
    Radio(text="Radio1", group_name="test_radio", has_custom_handler=True),
    Radio(text="Radio2", group_name="test_radio", has_custom_handler=True),
    Radio(text="Radio3", group_name="test_radio", has_custom_handler=True),
    Panel(
        Button("test1", "test"),
        Button("test2", "test"),
        Button("test3", "test"),
        Button("test4", "test"),
        Button("test5", "test"),
        lift_control_buttons=True,
        name="Panel1",
        width=2
    ),
    state=MenuStates.main1,
)

main_window2 = Window(
    Bold("Главное меню 2", end_count=2),
    ComeTo(text="Перейти в меню 1", state=MenuStates.main1),
    state=MenuStates.main2,
)

alert_mode = Alert(
    Text("Nice"),
    # FileBytes(file_name="{filename}", bytes_name="test_fb", when='test_when'),
    ReplyMode(name="h200"),
)
