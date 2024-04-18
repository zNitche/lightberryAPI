from lightberry.consts import HTTPConsts
import json


class ParserBase:
    @staticmethod
    def get_content_type():
        return None

    @staticmethod
    def parse(data):
        return data


class JsonParser(ParserBase):
    @staticmethod
    def get_content_type():
        return HTTPConsts.CONTENT_TYPE_JSON

    @staticmethod
    def parse(data):
        return json.loads(data)
