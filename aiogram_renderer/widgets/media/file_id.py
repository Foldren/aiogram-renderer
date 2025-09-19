from typing import Any
from aiogram_renderer.thumbnail import Thumbnail
from aiogram_renderer.widgets.text import Text, Area
from aiogram_renderer.widgets.widget import Widget


class FileID(Widget):
    __slots__ = ("file_id", "thumbnail", "media_caption")

    # Укажите caption если хотите видеть в MediaGroup под каждым фото описание
    # В случае отправки File отдельно используйте виджеты Text или Multi
    def __init__(self, file_id: str, thumbnail: Thumbnail = None, media_caption: str | Text | Area = "", show_on: str = None):
        """
        Виджет с файлом
        :param file_id: id файла
        :param thumbnail: объект превью Thumbnail
        :param media_caption: описание файла для MediaGroup
        :param show_on: фильтр видимости
        """
        super().__init__(show_on=show_on)
        self.file_id = file_id
        self.thumbnail = thumbnail
        self.media_caption = media_caption

    async def assemble(self, data: dict[str, Any], **kwargs) -> tuple[str, str, Any]:
        if not (await self.is_show_on(data)):
            return "", "", None

        file_id = self.file_id

        if isinstance(self.media_caption, (Text, Area)):
            caption_text = await self.media_caption.assemble(data)
        else:
            caption_text = self.media_caption

        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            # Подставляем значения в id файла
            if '{' + key + '}' in file_id:
                file_id = file_id.replace('{' + key + '}', str(value))
            # Подставляем значения в описание файла
            if isinstance(caption_text, str) and (caption_text != ""):
                if '{' + key + '}' in caption_text:
                    caption_text = caption_text.replace('{' + key + '}', str(value))

        if self.thumbnail is not None:
            thumbnail_obj = await self.thumbnail.assemble(data=data, kwargs=kwargs)
        else:
            thumbnail_obj = None

        return file_id, caption_text, thumbnail_obj


class VideoID(FileID):
    __slots__ = ()

    def __init__(self, file_id: str, thumbnail: Thumbnail = None, media_caption: str | Text | Area = "",
                 show_on: str = None):
        super().__init__(file_id=file_id, thumbnail=thumbnail, media_caption=media_caption, show_on=show_on)


class PhotoID(FileID):
    __slots__ = ()

    def __init__(self, file_id: str, thumbnail: Thumbnail = None, media_caption: str | Text | Area = "",
                 show_on: str = None):
        super().__init__(file_id=file_id, thumbnail=thumbnail, media_caption=media_caption, show_on=show_on)


class AudioID(FileID):
    __slots__ = ()

    def __init__(self, file_id: str, thumbnail: Thumbnail = None, media_caption: str | Text | Area = "",
                 show_on: str = None):
        super().__init__(file_id=file_id, thumbnail=thumbnail, media_caption=media_caption, show_on=show_on)
