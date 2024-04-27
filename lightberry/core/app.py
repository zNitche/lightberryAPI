from lightberry.core.communication.response import Response
from lightberry.utils import common_utils
from lightberry.config import AppConfig


class App:
    def __init__(self, debug_mode=AppConfig.DEBUG):

        self.debug_mode = debug_mode
        self.config = AppConfig

        self.host = None

        self.__routers = []
        self.__after_request_handler = None

        self.__background_tasks = []

        self.__print_debug("App created...")

    def add_background_task(self, task):
        if task is None:
            raise Exception("Task can't be none")

        self.__background_tasks.append(task)

    def register_background_tasks(self, events_loop):
        for task in self.__background_tasks:
            events_loop.create_task(task.handler())
            self.__print_debug(f"registering task: {task.__class__.__name__}")

    def add_router(self, router):
        if router is None:
            raise Exception("Router can't be none")

        router_existence_check = [True if router.name == r.name else False for r in self.__routers]

        if True in router_existence_check:
            raise Exception(f"Router '{router.name}' has already been added")

        self.__routers.append(router)

    @property
    def routers(self):
        return self.__routers

    async def requests_handler(self, request):
        response = Response(500)

        try:
            if request:
                self.__print_debug(f"request header: {request.headers}")
                self.__print_debug(f"request body: {request.body} | {type(request.body)}")

                response = await self.__process_request(request)

                self.__print_debug(f"response header: '{response.get_headers()}'")

        except Exception as e:
            self.__print_debug(f"error while handing request", exception=e)

        finally:
            return response

    async def __process_request(self, request):
        route, router = self.__get_route_for_url(request.url)
        response = Response(404)

        if route:
            if request.method not in route.methods:
                response = Response(405)

            else:
                path_parameters = route.get_path_parameters_for_url(request.url)
                response = await route.handler(request, **path_parameters)

            if router.after_request_handler:
                response = await router.after_request_handler(response)

        if self.__after_request_handler:
            response = await self.__after_request_handler(response)

        return response

    def __get_route_for_url(self, url):
        target_route = None
        target_router = None

        for router in self.__routers:
            route = router.match_route(url)

            if route:
                target_route = route
                target_router = router
                break

        self.__print_debug(f"route for url '{url}': {target_route.handler.__name__ if target_route else None}")

        return target_route, target_router

    def after_request(self):
        def wrapper(func):
            self.__after_request_handler = func

        return wrapper

    def get_routers_prefixes(self, excluded=None):
        urls = []

        if excluded is None:
            excluded = []

        for router in self.__routers:
            if router.url_prefix not in excluded:
                urls.append(router.url_prefix)

        return urls

    def __print_debug(self, message, exception=None):
        common_utils.print_debug(message, "APP", debug_enabled=self.debug_mode, exception=exception)