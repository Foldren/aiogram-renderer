from typing import Any
from aiogram.types import URLInputFile
from aiogram_renderer.widgets.text import Text, Area
from aiogram_renderer.widgets.widget import Widget


class FileUrl(Widget):
    __slots__ = ("url", "file_name", "headers", "thumbnail_url", "media_caption")

    # Укажите caption если хотите видеть в MediaGroup под каждым фото описание
    # В случае отправки File отдельно используйте виджеты Text или Multi
    def __init__(self, url: str, file_name: str = "", headers: dict[str, Any] = None,
                 thumbnail_url: str = "", media_caption: str | Text | Area = "", show_on: str = None):
        """
        Виджет с файлом
        :param url: ссылка на файл
        :param file_name: имя файла
        :param headers: заголовки
        :param thumbnail_url: ссылка на превью
        :param media_caption: описание файла для MediaGroup
        :param show_on: фильтр видимости
        """
        super().__init__(show_on=show_on)
        self.url = url
        self.file_name = file_name
        self.headers = headers
        self.thumbnail_url = thumbnail_url
        self.media_caption = media_caption

    async def assemble(self, data: dict[str, Any], **kwargs) -> tuple[URLInputFile | None, str, str]:
        if not (await self.is_show_on(data)):
            return None, "", ""

        file_name = self.file_name
        url = self.url
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
            # Подставляем значения в ссылку файла
            if '{' + key + '}' in url:
                url = url.replace('{' + key + '}', str(value))
            # Подставляем значения в ссылку превью
            if '{' + key + '}' in thumbnail_url:
                thumbnail_url = url.replace('{' + key + '}', str(value))
            # Подставляем значения в описание файла
            if isinstance(caption_text, str) and (caption_text != ""):
                if '{' + key + '}' in caption_text:
                    caption_text = caption_text.replace('{' + key + '}', str(value))

        if not file_name:
            file_name = None

        return URLInputFile(url=url, filename=file_name, headers=self.headers), caption_text, thumbnail_url


class VideoUrl(FileUrl):
    __slots__ = ()

    def __init__(self, url: str, file_name: str = "", headers: dict[str, Any] = None,
                 media_caption: str | Text | Area = "", thumbnail_url: str = "", show_on: str = None):
        super().__init__(file_name=file_name, url=url, headers=headers, thumbnail_url=thumbnail_url,
                         media_caption=media_caption, show_on=show_on)


class PhotoUrl(FileUrl):
    __slots__ = ()

    def __init__(self, url: str, file_name: str = "", headers: dict[str, Any] = None,
                 media_caption: str | Text | Area = "", show_on: str = None):
        super().__init__(file_name=file_name, url=url, headers=headers, media_caption=media_caption, show_on=show_on)


class AudioUrl(FileUrl):
    __slots__ = ()

    def __init__(self, url: str, file_name: str = "", headers: dict[str, Any] = None,
                 media_caption: str | Text | Area = "", show_on: str = None):
        super().__init__(file_name=file_name, url=url, headers=headers, media_caption=media_caption, show_on=show_on)
