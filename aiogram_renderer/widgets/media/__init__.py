__all__ = [
    "FileBytes",
    "VideoBytes",
    "PhotoBytes",
    "AudioBytes",
    "File",
    "Video",
    "Photo",
    "Audio",
    "FileUrl",
    "VideoUrl",
    "PhotoUrl",
    "AudioUrl",
    "FileID",
    "VideoID",
    "PhotoID",
    "AudioID",
]

from .bytes import FileBytes, VideoBytes, PhotoBytes, AudioBytes
from .path import File, Video, Photo, Audio
from .url import FileUrl, VideoUrl, PhotoUrl, AudioUrl
from .file_id import FileID, VideoID, PhotoID, AudioID

