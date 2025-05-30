from typing import Any
from aiogram.fsm.context import FSMContext
from .widgets.media import FileBytes
from .window import Alert


class BotMode:
    __slots__ = ('name', 'values', 'alert_window', 'has_custom_handler')

    # Вы можете использовать свой хендлер с фильтром IsMode(name=mode_name)
    # или использовать системный хендлер по умолчанию
    # has_custom_handler блокирует обработку системного хендлера
    # alert_window используется для ReplyMode

    def __init__(self, name: str, values: list[str], alert_window: Alert, has_custom_handler: bool = False):
        for widget in alert_window._widgets:
            if isinstance(widget, FileBytes):
                raise ValueError("В alert_window не может быть файл с байтами")

        self.name = name
        self.values = values
        self.has_custom_handler = has_custom_handler
        self.alert_window = alert_window


class BotModes:
    __slots__ = ('modes', 'fsm')

    def __init__(self, *modes: BotMode, fsm: FSMContext) -> None:
        self.modes = list(modes)
        self.fsm = fsm

    async def sync_modes(self, fsm_data: dict[str, Any]) -> dict[str, Any]:
        # Словарь с режимами бота, имеет следующий формат:
        # '__modes__': {'name1': ['value1_1', 'value2_2'...], 'name2: ['value2_1', 'value2_2'...]...}
        dict_modes = await self.get_dict_modes()

        if "__modes__" in fsm_data.keys():
            # Если число режимов изменилось, обновляем список режимов в fsm
            if len(dict_modes) != len(fsm_data["__modes__"]):
                fsm_data["__modes__"] = dict_modes

            # Дополнительно проверяем ключи и значения режимов на изменения
            for name, values in fsm_data["__modes__"].items():
                if name not in dict_modes.keys():
                    fsm_data["__modes__"] = dict_modes
                    break
                for value in dict_modes[name]:
                    if value not in values:
                        fsm_data["__modes__"] = dict_modes
                        break
        # Если режимы не заданы в fsm, то записываем словарь __modes__ в него
        else:
            fsm_data["__modes__"] = dict_modes

        return fsm_data

    async def get_dict_modes(self) -> dict[str, Any]:
        return {mode.name: mode.values for mode in self.modes}

    async def get_modes_values(self) -> list[str]:
        values = []
        for mode in self.modes:
            values += mode.values
        return values

    async def get_mode_by_name(self, name: str) -> BotMode | None:
        for mode in self.modes:
            if mode.name == name:
                return mode
        return None

    async def get_mode_by_value(self, value: str) -> BotMode | None:
        for mode in self.modes:
            for mode_value in mode.values:
                if mode_value == value:
                    return mode
        return None

    async def get_fsm_modes(self):
        fsm_data = await self.fsm.get_data()
        # Если режимов нет в fsm, то записываем их из self.bot.modes
        if "__modes__" not in fsm_data:
            fsm_data["__modes__"] = await self.get_dict_modes()
        # Если они есть, то проверяем верно ли они заданы
        else:
            fsm_data = await self.sync_modes(fsm_data)

        await self.fsm.set_data(fsm_data)
        return fsm_data["__modes__"]

    async def update_mode(self, mode: str) -> str:
        """
        Обновляем режим, для этого передаем в него название режима либо значение в нем.
        :param mode: название или одно из значений режима
        :return:
        """
        dict_modes = await self.get_dict_modes()

        # Ищем режим по значению (ReplyMode)
        if mode in dict_modes.values():
            name = list(dict_modes.keys())[list(dict_modes.values()).index(mode)]
        # Ищем режим по ключу (Mode)
        elif mode in dict_modes.keys():
            name = mode
        # Если режим нигде не найти
        else:
            raise ValueError("У бота нет данного режима")

        fsm_modes = await self.get_fsm_modes()
        # Переносим активный режим в конец списка
        last_active_mode = fsm_modes[name].pop(0)
        fsm_modes[name].append(last_active_mode)
        # Записываем данные с новым режимом
        await self.fsm.update_data({"__modes__": fsm_modes})
        return name

    async def get_active_value(self, name: str) -> None:
        dict_modes = await self.get_dict_modes()
        if not dict_modes.get(name):
            raise ValueError("У бота нет данного режима")
        fsm_modes = await self.get_fsm_modes()
        # Активным считается первое значение режима
        return fsm_modes[name][0]

