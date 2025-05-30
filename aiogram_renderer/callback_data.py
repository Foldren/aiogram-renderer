from aiogram.filters.callback_data import CallbackData


class DPanelCD(CallbackData, prefix="__dpanel__"):
    page: int
    panel_name: str

class ModeCD(CallbackData, prefix="__mode__"):
    name: str

class ComeToCD(CallbackData, prefix="__cometo__"):
    group: str
    state: str
