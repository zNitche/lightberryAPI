from lightberry.core.communication.response import Response
from lightberry.utils import common_utils
from lightberry.config import AppConfig


class App:
    def __init__(self, debug_mode=AppConfig.DEBUG):

        self.debug_mode = debug_mode
        self.routers = []

        self.__print_debug("App created...")

    def add_router(self, router):
        self.routers.append(router)

    async def requests_handler(self, request):
        response = Response(500)

        try:
            if request:
                self.__print_debug(f"request header: {request.headers}")
                self.__print_debug(f"request body: {request.body} | {type(request.body)}")

                response = await self.__process_request(request)

                self.__print_debug(f"response header for: '{response.get_headers()}'")

        except Exception as e:
            self.__print_debug(f"error while handing request", exception=e)

        finally:
            return response

    async def __process_request(self, request):
        route, path_parameters = self.__get_route_for_url(request.url)
        response = Response(404)

        if route:
            if request.method not in route.methods:
                response = Response(405)

            else:
                response = await route.handler(request, **path_parameters)

        return response

    def __get_route_for_url(self, url):
        target_route = None
        core_url = url.split("?")[0]

        for router in self.routers:
            route = router.match_route(core_url)

            if route:
                target_route = route
                break

        self.__print_debug(f"route for url '{url}': {target_route.handler.__name__ if target_route else None}")

        path_parameters = target_route.get_path_parameters_for_url(url) if target_route else None
        self.__print_debug(f"path parameters for '{url}': {path_parameters}")

        return target_route, path_parameters

    def __print_debug(self, message, exception=None):
        common_utils.print_debug(message, "APP", debug_enabled=self.debug_mode, exception=exception)