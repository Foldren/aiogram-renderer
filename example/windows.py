from states import MenuStates
from widgets.keyboard.inline.button import Mode, ComeTo
from widgets.keyboard.inline.panel import DynamicPanel
from widgets.keyboard.reply.button import ReplyMode
from widgets.text import Area, Bold, Text
from window import Window, Alert

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
    ComeTo(text="Перейти в меню 2", state=MenuStates.main2),
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
