from states import MenuStates
from aiogram_renderer.widgets.keyboard.inline import Mode, ComeTo, DynamicPanel
from aiogram_renderer.widgets.keyboard.reply import ReplyMode
from aiogram_renderer.widgets.text import Area, Bold, Text, Progress
from aiogram_renderer.window import Window, Alert

main_window = Window(
    Bold("Главное меню", end_count=2),
    Text("👋 Привет<b>{username}</b>, я тест", end_count=2),
    Area("Рабочие кнопки бота",
          "🔸 <b>тест 1</b> - получить больше тестов",
          "🔸 <b>тест 2</b> - получить еще больше тестов", end_count=2),
    Area(Bold("2342525{path}255", end_count=1), end_count=2),
    Bold("Прогресс 1", end_count=1),
    Bold("\nПрогресс 2", end_count=1),
    Mode(name="h200"),
    DynamicPanel(
        name="test_dg",
        width=2,
        height=2,
        hide_number_pages=True
    ),
    ComeTo(text="Перейти в меню 2", state=MenuStates.main2, show_on="test_show_on"),
    Progress(name="test_pr", add_percent=True, prefix="\n"),
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
