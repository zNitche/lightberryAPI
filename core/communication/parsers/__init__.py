from lightberry.core.communication.parsers import request_payload_parsers as parsers
import sys


class RequestPayloadParser:
    def __init__(self):
        self.parsers = {
            parsers.JsonParser.get_content_type(): parsers.JsonParser,
        }

    def get_parser(self, content_type):
        return self.parsers.get(content_type)

    def parse_payload(self, content_type, payload):
        parser = self.get_parser(content_type)

        if parser:
            try:
                payload = parser.parse(payload)
            except Exception as e:
                sys.print_exception(e)

        return payload
