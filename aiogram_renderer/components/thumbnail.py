from abc import abstractmethod, ABC
from typing import Any
from aiogram.types import BufferedInputFile, URLInputFile, FSInputFile


class Thumbnail(ABC):
    __slots__ = ()

    @abstractmethod
    async def assemble(self, *args, **kwargs):
        pass


class ThumbnailPath:
    __slots__ = ("file_name", "path")

    def __init__(self, file_name: str, path: str):
        self.file_name = file_name
        self.path = path

    async def assemble(self, data: dict[str, Any], **kwargs) -> FSInputFile | None:
        file_name = self.file_name
        path = self.path

        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            # Подставляем значения в имя файла
            if '{' + key + '}' in file_name:
                file_name = file_name.replace('{' + key + '}', str(value))
            # Подставляем значения в пути файла
            if '{' + key + '}' in path:
                path = path.replace('{' + key + '}', str(value))

        return FSInputFile(path=path, filename=file_name)


class ThumbnailUrl:
    __slots__ = ("file_name", "url")

    def __init__(self, file_name: str, url: str):
        self.file_name = file_name
        self.url = url

    async def assemble(self, data: dict[str, Any], **kwargs) -> URLInputFile | None:
        file_name = self.file_name
        url = self.url

        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            # Подставляем значения в имя файла
            if '{' + key + '}' in file_name:
                file_name = file_name.replace('{' + key + '}', str(value))
            # Подставляем значения в ссылку файла
            if '{' + key + '}' in url:
                url = url.replace('{' + key + '}', str(value))

        return URLInputFile(url=url, filename=file_name)


class ThumbnailBytes:
    __slots__ = ("file_name", "bytes_name")

    def __init__(self, file_name: str, bytes_name: str):
        self.file_name = file_name
        self.bytes_name = bytes_name

    async def assemble(self, data: dict[str, Any], **kwargs) -> BufferedInputFile | None:
        file_name = self.file_name

        # Форматируем по data, если там заданы ключи {key}
        for key, value in data.items():
            # Подставляем значения в имя файла
            if '{' + key + '}' in file_name:
                file_name = file_name.replace('{' + key + '}', str(value))

        return BufferedInputFile(file=kwargs["file_bytes"][self.bytes_name], filename=file_name)
