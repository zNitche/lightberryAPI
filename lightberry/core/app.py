from lightberry.communication.response import Response
from lightberry.utils import common_utils
from lightberry.config import AppConfig
import json


class App:
    def __init__(self, debug_mode=AppConfig.DEBUG):

        self.debug_mode = debug_mode
        self.__print_debug("App created...")

    async def requests_handler(self, request):
        response = Response(500)

        try:
            if request:
                self.__print_debug(f"request header: {request.headers}")
                self.__print_debug(f"request body from: {request.body} | {type(request.body)}")

                response = Response(status_code=200, payload=json.dumps({"test": 1}))

                self.__print_debug(f"response header for: '{response.get_headers()}'")

        except Exception as e:
            self.__print_debug(f"error occurred: {str(e)}", exception=e)

        finally:
            return response

    def __print_debug(self, message, exception=None):
        common_utils.print_debug(message, "APP", debug_enabled=self.debug_mode, exception=exception)