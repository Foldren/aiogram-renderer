from typing import Any
from aiogram.types import FSInputFile
from aiogram_renderer.widgets.text import Text, Area
from aiogram_renderer.widgets.widget import Widget


class File(Widget):
    __slots__ = ("file_name", "path", "thumbnail_url", "media_caption")

    # Укажите caption если хотите видеть в MediaGroup под каждым фото описание
    # В случае отправки File отдельно используйте виджеты Text или Multi
    def __init__(self, file_name: str, path: str, thumbnail_url: str = "",
                 media_caption: str | Text | Area = "", show_on: str = None):
        """
        Виджет с файлом
        :param file_name: имя файла
        :param path: путь к файлу
        :param thumbnail_url: ссылка на превью
        :param media_caption: описание файла для MediaGroup
        :param show_on: фильтр видимости
        """
        super().__init__(show_on=show_on)
        self.file_name = file_name
        self.path = path
        self.thumbnail_url = thumbnail_url
        self.media_caption = media_caption

    async def assemble(self, data: dict[str, Any], **kwargs) -> tuple[FSInputFile | None, str, str]:
        if not (await self.is_show_on(data)):
            return None, "", ""

        file_name = self.file_name
        path = self.path
        thumbnail_url = self.thumbnail_url

        if isinstance(self.media_caption, (Text, Area)):
            caption_text = await self.media_caption.assemble(data)
        else:
            caption_text = self.media_caption

        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            # Подставляем значения в имя файла
            if '{' + key + '}' in file_name:
                file_name = file_name.replace('{' + key + '}', str(value))
            # Подставляем значения в путь файла
            if '{' + key + '}' in path:
                path = path.replace('{' + key + '}', str(value))
            # Подставляем значения в ссылку превью
            if '{' + key + '}' in thumbnail_url:
                thumbnail_url = thumbnail_url.replace('{' + key + '}', str(value))
            # Подставляем значения в описание файла
            if isinstance(caption_text, str) and (caption_text != ""):
                if '{' + key + '}' in caption_text:
                    caption_text = caption_text.replace('{' + key + '}', str(value))

        return FSInputFile(path=path, filename=file_name), caption_text, thumbnail_url


class Video(File):
    __slots__ = ()

    def __init__(self, file_name: str, path: str, thumbnail_url: str = "",
                 media_caption: str | Text = None, show_on: str = None):
        super().__init__(file_name=file_name, path=path, thumbnail_url=thumbnail_url,
                         media_caption=media_caption, show_on=show_on)


class Photo(File):
    __slots__ = ()

    def __init__(self, file_name: str, path: str, media_caption: str | Text = None, show_on: str = None):
        super().__init__(file_name=file_name, path=path, media_caption=media_caption, show_on=show_on)


class Audio(File):
    __slots__ = ()

    def __init__(self, file_name: str, path: str, thumbnail_url: str = "", media_caption: str | Text = None,
                 show_on: str = None):
        super().__init__(file_name=file_name, path=path, media_caption=media_caption, thumbnail_url=thumbnail_url,
                         show_on=show_on)
