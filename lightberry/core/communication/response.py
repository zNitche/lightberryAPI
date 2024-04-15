from lightberry.consts import HTTPConsts


class Response:
    def __init__(self, status_code=200, content_type=HTTPConsts.CONTENT_TYPE_JSON, payload=None):
        self.headers = {}
        self.status_code = status_code
        self.content_type = content_type

        self.is_payload_streamed = False

        self.payload = payload
        self.cookies = {}

    def get_content_length(self):
        return len(self.payload) if self.payload else 0

    def get_headers(self):
        header_rows = [f"HTTP/1.1 {self.status_code}",
                       f"CONTENT-TYPE: {self.content_type}",
                       f"CONTENT-LENGTH: {self.get_content_length()}"]

        for header, value in self.headers.items():
            header_rows.append(f"{header}: {value}")

        header_string = "\r\n".join(header_rows)

        return header_string

    def get_body(self):
        return self.payload if self.payload else ""

    def get_response_string(self):
        headers = self.get_headers()
        body = self.get_body()

        return f"{headers}\r\n\r\n{body}"
