from lightberry.consts import HTTPConsts
from lightberry.core.communication.response import Response
from lightberry.utils import files_utils, common_utils

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterator


class FileResponse(Response):
    def __init__(self, file_path: str = "", content_type: str | None = None, status_code: int = 200):
        self.file_path: str = file_path

        super().__init__()

        self.is_payload_streamed: bool = True

        self.status_code: int = status_code

        self.content_type = self.__get_content_type() if content_type is None else content_type
        self.__file_check()

    def __file_check(self):
        if not files_utils.file_exists(self.file_path):
            self.is_payload_streamed = False
            self.status_code = 404
            self.content_type = None

    def get_content_length(self) -> float:
        return files_utils.get_file_size(self.file_path)

    def __get_content_type(self) -> str:
        content_type = HTTPConsts.CONTENT_TYPE_TEXT

        for key, value in HTTPConsts.FILES_TYPES_BY_EXTENSION.items():
            if self.file_path.endswith(key):
                content_type = value
                break

        if common_utils.endswith(self.file_path, HTTPConsts.GZIP_COMPRESSED_CONTENT_EXTENSIONS):
            self.add_header(HTTPConsts.CONTENT_ENCODING, "gzip")

        return content_type

    def get_body(self) -> Iterator[str] | str:
        return self.payload_streamer() if self.is_payload_streamed and self.content_type else ""

    def payload_streamer(self) -> Iterator[str]:
        with open(self.file_path, "rb") as file:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break

                yield chunk
