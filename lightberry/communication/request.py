from lightberry.consts import HTTPConsts
from lightberry.communication.parsers.request_payload_parser import RequestPayloadParser


class Request:
    def __init__(self):
        self.protocol = None
        self.target = None
        self.method = None

        self.header = {}
        self.body = ""

        self.cookies = {}

        self.path_parameters = {}
        self.query_params = {}

        self.payload_parser = RequestPayloadParser()

    def parse_header(self, header_string):
        splitted_request_string = self.split_request_string(header_string)

        if len(splitted_request_string) > 0:
            self.method, self.target, self.protocol = splitted_request_string[0].split()
            splitted_request_string.pop(0)

            self.header = self.parse_request_string(splitted_request_string)

            self.parse_cookies()
            self.parse_query_params()

    def parse_query_params(self):
        if "?" in self.target:
            splitted_url = self.target.split("?")

            if len(splitted_url) == 2:
                for param_string in splitted_url[1].split("&"):
                    splitted_string = param_string.split("=")

                    if len(splitted_string) == 2:
                        self.query_params[splitted_string[0]] = splitted_string[1]

    def parse_cookies(self):
        if "COOKIE" in self.header.keys():
            splitted_cookies_data = self.header["COOKIE"].split("; ")

            for data_row in splitted_cookies_data:
                splitted_data = data_row.split("=")

                name = splitted_data[0]
                value = splitted_data[1]

                self.cookies[name] = value

    def parse_body(self, body_string):
        body = body_string.replace("\r", "").replace("\n", "")
        self.body = self.payload_parser.parse_payload(self.header.get(HTTPConsts.CONTENT_TYPE), body)

    def parse_request_string(self, splitted_request_string):
        request_struct = {}

        if len(splitted_request_string) > 0:
            for raw_row in splitted_request_string:
                row = raw_row.split(":")

                if len(row) == 2:
                    request_struct[row[0].upper()] = row[1].strip()

        return request_struct

    def split_request_string(self, string):
        return string.replace("\r", "").split("\n")
