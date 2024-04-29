from lightberry.consts import HTTPConsts


class Response:
    def __init__(self, status_code: int = 200, content_type: str = HTTPConsts.CONTENT_TYPE_JSON, payload: str = None):
        self.headers: dict[str, ...] = {}
        self.status_code: int = status_code
        self.content_type: str = content_type

        self.is_payload_streamed: bool = False

        self.payload: str | None = payload

    def get_content_length(self) -> int:
        return len(self.payload) if self.payload else 0

    def get_headers(self) -> str:
        header_rows = [f"HTTP/1.1 {self.status_code}",
                       f"CONTENT-LENGTH: {self.get_content_length()}"]

        for header, value in self.headers.items():
            header_rows.append(f"{header}: {value}")

        if HTTPConsts.CONTENT_TYPE not in header_rows:
            header_rows.append(f"{HTTPConsts.CONTENT_TYPE}: {self.content_type}")

        header_string = "\r\n".join(header_rows)

        return header_string

    def add_header(self, name: str, value):
        normalized_name = name.upper()

        if normalized_name not in self.headers.keys():
            self.headers[normalized_name] = value

    def get_body(self) -> str:
        return self.payload if self.payload else ""

    def get_response_string(self) -> str:
        headers = self.get_headers()
        body = self.get_body()

        return f"{headers}\r\n\r\n{body}"
