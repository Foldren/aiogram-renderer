from states import MenuStates
from widgets.keyboard.inline.button import Button, Mode
from widgets.keyboard.inline.group import Group, Column, DynamicGroup
from widgets.keyboard.reply.button import ReplyButton, ReplyMode
from widgets.keyboard.reply.group import ReplyGroup, ReplyColumn
from window import Window, Alert
from widgets.text import Multi, Bold, Text

main_window = Window(
    Bold("Главное меню", end_count=2),
    Text("👋 Привет<b>{username}</b>, я бот 🔴🎬 <b>YouTube Video Loader Beta 3.0</b> "
         " на данный момент нахожусь в активной стадии разработки, умею скачивать видео/шортсы с платформы "
         "YouTube в качестве до 4К 2160p, в формате MP4, также извлекаю аудио из видео в формате MP3.)", end_count=2),
    Multi("<u>Рабочие кнопки бота ⚙️</u>",
          "🔸 <b>Загрузка видео</b> - кнопка с доп. информацией о боте.",
          "🔸 <b>Поддержка</b> - нажмите кнопку чтобы внести предложение по функциональности "
          "или создать тикет для обращения в поддержку, интеграции.", end_count=2),
    Multi(Bold("2342525{path}255", end_count=1), end_count=2),
    Bold("Прогресс 1", end_count=1),
    Bold("\nПрогресс 2", end_count=1),
    # Column(
    #     Button(text="1", when="test_when", data="1"),
    #     Mode(name="h200"),
    #     Button(text="3", data="2")
    # ),
    # Button(text="{path}", data="123", when="test_when"),
    ReplyButton(text="{path}"),
    ReplyMode(name="h200"),
    # MediaGroup(
    #     VideoBytes(file_name="{filename}", file_bytes_name="bytes_f", media_caption=Underline("test2")),
    #     PhotoBytes(file_name="{filename}", file_bytes_name="bytes_f", media_caption=Underline("test")),
    # ),
    # Button(text="Группа 1", data="123"),
    # DynamicGroup(
    #     name="test_dg",
    #     width=2,
    #     height=2,
    #     hide_number_pages=True
    # ),
    # Button(text="Группа 2", data="123"),
    # DynamicGroup(
    #     fsm_name="test_dg2",
    #     width=3,
    #     height=2,
    # ),
    # File(file_name="{filename}", path="{filename}"),
    # Audio(file_name="{filename}", path="{filename}"),
    state=MenuStates.main,
)

alert_mode = Alert(
    Text("Nice"),
    Mode(name="h200"),
    DynamicGroup(
            name="test_dg",
            width=2,
            height=2,
            hide_number_pages=True
        ),
)
