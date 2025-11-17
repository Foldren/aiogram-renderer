# aiogram-renderer
[![](https://raw.githubusercontent.com/Foldren/aiogram-renderer/refs/heads/master/aiogram_renderer/badges/python.svg)](https://github.com/Foldren/aiogram-renderer)
[![](https://raw.githubusercontent.com/Foldren/aiogram-renderer/refs/heads/master/aiogram_renderer/badges/license.svg)](https://github.com/Foldren/aiogram-renderer/blob/master/LICENSE)
[![](https://raw.githubusercontent.com/Foldren/aiogram-renderer/refs/heads/master/aiogram_renderer/badges/pypl.svg)](https://pypi.org/project/aiogram-renderer)
[![](https://raw.githubusercontent.com/Foldren/aiogram-renderer/refs/heads/master/aiogram_renderer/badges/donate.svg)](https://t.me/tribute/app?startapp=dzwH)

## О проекте
Библиотека создана для того чтобы ее можно было использовать вместе с aiogram, а не вместо aiogram. Реализованы
основные текстовые и клавиатурные виджеты, чтобы ускорить и упростить создание telegram ботов.

#### Поддержка разработчика

[<img src="https://i2.wp.com/miro.medium.com/1*D-JJemrcn63kKj3lPBwZ5w.png" width=200>](https://t.me/tribute/app?startapp=dzwH)

## Функции
aiogram-renderer включает в себя:
- 100% асинхронность
- гибкую структуру, позволяющую без проблем использовать библиотеку совместно с aiogram
- поддержку как Reply так и Inline клавиатур
- удобный виджет Progress для управления загрузками
- режимы бота, доступные из разных окон
- работу с файлами
- организованную логику для управления FSM данными окон
- окна-уведомления, которые можно отправлять без использования данных в FSM
- управление видимостью виджетов через параметр show_on
- динамические наборы кнопок доступные из разных окон

## Установка
Для установки, выполните команду
```
pip install aiogram-renderer
```
## Начало
Для подключения библиотеки к проекту надо выполнить функцию configure_renderer, в
ней вам нужно передать окна, которые будут использоваться в проекте и настроить при необходимости режимы.
```python
async def main():
    logging.basicConfig(level=logging.INFO)

    await configure_renderer(
        dp=dp,
        # Подключаем окна
        windows=[window],
        # Задаем режимы бота (первый активный по умолчанию)
        modes=[
            BotMode(
                name="mode1",
                values=["off 🟥⬜️  Режим 1", "on ⬜️🟩  Режим 1"],
                alert_window=alert,
            ),
            BotMode(
                name="mode2",
                values=["off 🟥⬜️  Режим 2", "on ⬜️🟩  Режим 2"],
                alert_window=alert,
                has_custom_handler=False
            )
        ]
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
```

## Типы окон
Для работы можно использовать 2 типа окон:
1. Window - окно с состоянием State, данные хранятся в памяти FSM. 
Рендерятся окна с установкой стейта автоматически.
Мапятся по state, подробнее в разделе.
```python
window = Window(
    Text("Тест окна"),
    Panel(
        Button(text="Кнопка", data="button"),
        Button(text="Тоже кнопка", data="button_too"),
        Mode(name="mode1"),
        width=2
    ),
    state=MainSteps.step1
)
```
2. Alert - окно-уведомление, его данные не хранятся в FSM, соответственно на alert есть ограничения по использованию некоторых виджетов (Mode, DynamicPanel)
```python
alert = Alert(
    Area(
        Bold("Тест окна", end_count=3),
        "все хорошо",
        sep_count=2
    )
```
## Отправка
Для отправки сообщений из собранных окон с виджетами, используйте функции render из встроенного аргумента renderer с mode=RenderMode.ANSWER и др. или
более быстрые answer, edit, delete_and_send, reply. Вы можете использовать chat_id, message_id или event по желанию,
по умолчанию renderer подхватывает event в хендлере.
```python
@dp.message(F.text=="/start")
async def start(message: Message, renderer: Renderer):
    message, window = await renderer.render(window=window, chat_id=message.chat_id, message_id=message.message_id, mode=RenderMode.EDIT)
```
> [!NOTE]
> Вы можете использовать renderer вместе с обычными методами update
```python
@dp.message(F.text=="use1")
async def use1(message: Message, renderer: Renderer):
    # Использование хендлера с Renderer
    message, window = await renderer.delete_and_send(window=window)

@dp.message(F.text=="use2")
async def use2(message: Message):
    # Использование встроенных методов окна для генерации исключельно клавиатуры или текста
    text = await window.gen_text(data={"username": message.from_user.username})
    await message.answer(text=text)

@dp.message(F.text=="use3")
async def use3(message: Message):
    # Использование хендлера без Renderer
    await message.answer(text="Все ок!")
```


## Хранение данных
Данные собранные через библиотеку хранятся в fsm для каждого пользователя в следующем формате:

```json
{
    "__modes__": {
      "mode1": ["off 🟥⬜️  Режим 1", "on ⬜️🟩  Режим 1"],
      "mode2": ["off 🟥⬜️  Режим 2", "on ⬜️🟩  Режим 2"]
    },
    "__dpanels__": {
      "test_dp": {
        "page": 2,
        "text": ["1","2","3"],
        "data": ["d1","d2","d3"]
      }
    },
    "__windows__": {
        "MainSteps.step1": {
            "username": "Коля",
            "visible": true
        },
        "MainSteps.step2": {
            "username": "Маша",
            "surname": "Сечинова",
            "visible": false
        }
    }
}
```
Все окна хранятся в порядке открытия и могут перезаписываться если указывать новые параметры data при их рендере:
```python
@dp.message(F.text=="/start")
async def start(message: Message, renderer: Renderer):
    await renderer.delete_and_send(window=window, data={"username": message.from_user.username})
```
> [!TIP]
> Сами поля содержат в себе данные которые вы можете подставить в окно, использовав фигурные скобки в некоторых параметрах виджетов:
```python
window = Window(
    Text("Привет {username}, Тест окна"),
    Panel(
        Button(text="Кнопка", data="button{username}"),
        Button(text="Тоже кнопка", data="button_too"),
        Mode(name="mode1"),
        width=2
    ),
    state=MainSteps.step1
)
```
## Видимость виджетов
Для управления отображением виджетами используйте параметр show_on, значение берется из параметра data функции render и в дальнейшем хранится в памяти, учитывайте это и обновляйте параметр при необходимости.
```python
window = Window(
    Text("Привет {username}, Тест окна"),
    Panel(
        Button(text="Кнопка", data="button{username}", show_on="is_admin"),
        Button(text="Тоже кнопка", data="button_too", show_on="is_admin"),
        Mode(name="mode1"),
        width=2
    ),
    state=MainSteps.step1
)

@dp.message(F.text=="/start")
async def start(message: Message, renderer: Renderer):
    await renderer.delete_and_send(window=window, data={"is_admin": True})
```
## Режимы
Частенько требовалась кнопка которая бы обновляла и хранила свое активное состояние в разных сообщениях. Режимы позволяют реализовать это, укажите их в configure_renderer
и потом передавайте в окна через Mode, ReplyMode виджеты. У каждого режима есть alert_window, это нужно чтобы работал системный хендлер ReplyMode, также вы можете указать has_custom_handler и настроить свою хендлер для обработки апдейта режима.
```python
window = Window(
    Text("Привет {username}, Тест окна"),
    ReplyPanel(
        ReplyButton(text="Кнопка", data="button{username}"),
        ReplyButton(text="Тоже кнопка", data="button_too", show_on="is_admin"),
        ReplyMode(name="mode2"),
        width=2
    ),
    state=MainSteps.step1
)

async def main():
    logging.basicConfig(level=logging.INFO)

    await configure_renderer(
        dp=dp,
        # Подключаем окна
        windows=[window],
        # Задаем режимы бота (первый активный по умолчанию)
        modes=[
            BotMode(
                name="mode1",
                values=["off 🟥⬜️  Режим 1", "on ⬜️🟩  Режим 1"],
            ),
            BotMode(
                name="mode2",
                values=["Админ", "Юзер", "Продавец"],
                alert_window=alert,
                has_custom_handler=True
            )
        ]
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

@dp.message(IsMode("mode2"))
async def update_mode(message: Message, renderer: Renderer):
    # Получаем режим с помощью функции get_mode_by_value (также есть get_mode_by_name)
    mode = await renderer.bot_modes.get_mode_by_value(value=message.text)
    # Обновляем режим
    await renderer.bot_modes.update_mode(mode=mode.name)
    # Обновляем окно
    await renderer.edit(window=MenuStates.step1)
```
## Прогресс бар
Для управления полосой загрузки используйте виджет Progress и функцию update_progress, задайте нужный интервал обновления.
```python
window = Window(
    Text("Привет {username}, Тест окна", end_count=2),
    Progress(name="test_pr")
    Panel(
        Button(text="Кнопка", data="button{username}"),
        Button(text="Тоже кнопка", data="button_too", show_on="is_admin"),
        Mode(name="mode1"),
        width=2
    ),
    state=MainSteps.step1
)

@dp.message(F.text=="/start")
async def start(message: Message, renderer: Renderer):
    data = {"username": message,from_user.username, "test_pr": 0}
    
    # Сначала будет установлен процент 0
    pr_message, window = await renderer.answer(window=MenuStates.step1, data=data)
    
    for i in range(99):
        await renderer.update_progress(window=MenuStates.step1, event=pr_message, interval=0.3,
                                       name="test_pr", percent=i, data=data)
        await sleep(0.3)
```
## Динамические наборы
Для отображения кнопок со своими данными используется виджет DynamicPanel. Нужно указать text, data и первую активную
страницу, данные сохранятся в FSM и будут доступны для всех окон.
```python
window = Window(
    Text("Привет {username}, Тест окна", end_count=2),
    DynamicPanel(name="dpanel", hide_number_pages=True),
    state=MainSteps.step1
)

@dp.message(F.text=="/start")
async def start(message: Message, renderer: Renderer):
    data = {
        "dpanel": {
            "page": 2,
            "text": ["1", "2", "3", "4", "5"],
            "data": ["d1", "d2", "d3", "d4", "d5"]
        },
    }
    await renderer.answer(window=MenuStates.step1, data=data)

@dp.callback_query(F.data.startswith("d"))
async def dpanel_opt(callback: CallbackQuery, renderer: Renderer):
    # Тут ваши действия для обработки кнопок из DynamicPanel
    pass
```
## Файлы
Для работы с файлами реализовано 2 виджета, первый это виджет File и его дочерние Photo, Video, Audio. В нем мы указываем путь к файлу и его название.
```python
window = Window(
    Text("Привет {username}, Тест окна", end_count=2),
    Audio(file_name="audio.mp3", path="audio.mp3"),
    state=MainSteps.step1
)
```
Второй это FileBytes, он используется для передачи файла в байтах, данные не хранятся в памяти и отображаются
только тогда когда вы передаете параметр file_bytes в функции render.
```python
window = Window(
    Text("Привет {username}, Тест окна", end_count=2),
    AudioBytes(file_name="audio.mp3", bytes_name="bytes_a"),
    state=MainSteps.step1
)

@dp.message(F.text=="/start")
async def start(message: Message, renderer: Renderer):
    async with aiofiles.open(file="audio.mp3", mode="rb") as f:
        await renderer.answer(window=MenuStates.step1, file_bytes={"bytes_a": await f.read()})
```
Медиа группа имеет специфичную логику работы, так что пока она в разработке, нужно понять как ее правильно добавить в экосистему библиотеки.

## Будущее проекта

В документации указаны не все виджеты, с остальными предлагаю ознакомиться самостоятельно 😉
По мере поддержки или при необходимости в работе буду добавлять новые виджеты и совершенствовать библиотеку, кому интересно. Так в планах MediaGroup, ReplyDynamicPanel, поддержка виджетов в Alert,
виджет Calendar и поддержка доп. полей для кнопок, которые задаются в aiogram. Также возможно сделаю виджет DynamicMediaGroup. Все по мере возможностей, спасибо что прочитали.


