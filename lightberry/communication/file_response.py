from lightberry.consts import HTTPConsts
from lightberry.communication.response import Response
from lightberry.utils import files_utils


class FileResponse(Response):
    def __init__(self, file_path="", content_type=None, status_code=200):

        self.file_path = file_path

        super().__init__()

        self.is_payload_streamed = True

        self.content_type = self.get_content_type_by_extension() if content_type is None else content_type
        self.status_code = status_code

    def get_content_length(self):
        return files_utils.get_file_size(self.file_path)

    def get_content_type_by_extension(self):
        file_extension = f".{self.file_path.split('.')[-1]}"
        content_type_from_consts = HTTPConsts.FILES_TYPES_BY_EXTENSION.get(file_extension)

        return content_type_from_consts if content_type_from_consts is not None else HTTPConsts.CONTENT_TYPE_HTML

    def get_body(self):
        return self.payload_streamer()

    def payload_streamer(self):
        with open(self.file_path, "rb") as file:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break

                yield chunk
