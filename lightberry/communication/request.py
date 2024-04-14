from lightberry.consts import HTTPConsts
from lightberry.communication.parsers.request_payload_parser import RequestPayloadParser


class Request:
    def __init__(self):
        self.protocol = None
        self.url = None
        self.method = None
        self.content_length = 0
        self.content_type = None

        self.headers = {}
        self.body = None

        self.cookies = {}

        self.path_parameters = {}
        self.query_params = {}

        self.payload_parser = RequestPayloadParser()

    def parse_header(self, header_string):
        split_request_string = header_string.replace("\r", "").split("\n")

        if len(split_request_string) > 0:
            self.method, self.url, self.protocol = split_request_string[0].split()
            split_request_string.pop(0)

            self.headers = self.__parse_request_string(split_request_string)

            self.__parse_cookies()
            self.__parse_query_params()
            
        self.content_length = int(self.headers[HTTPConsts.CONTENT_LENGTH]) if (HTTPConsts.CONTENT_LENGTH
                                                                               in self.headers.keys()) else 0
        self.content_type = self.headers.get(HTTPConsts.CONTENT_TYPE)

    def __parse_request_string(self, split_request_string):
        request_struct = {}

        if len(split_request_string) > 0:
            for raw_row in split_request_string:
                row = raw_row.split(":")

                if len(row) == 2:
                    request_struct[row[0].upper()] = row[1].strip()

        return request_struct

    def __parse_query_params(self):
        if "?" in self.url:
            split_url = self.url.split("?")

            if len(split_url) == 2:
                for param_string in split_url[1].split("&"):
                    split_string = param_string.split("=")

                    if len(split_string) == 2:
                        self.query_params[split_string[0]] = split_string[1]

    def __parse_cookies(self):
        if HTTPConsts.COOKIE in self.headers.keys():
            split_cookies_data = self.headers[HTTPConsts.COOKIE].split("; ")

            for data_row in split_cookies_data:
                split_data = data_row.split("=")

                name = split_data[0]
                value = split_data[1]

                self.cookies[name] = value

    def parse_body(self, body_string):
        body = body_string.replace("\r", "").replace("\n", "")
        self.body = self.payload_parser.parse_payload(self.content_type, body) if self.content_type else None
