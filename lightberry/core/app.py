import asyncio
from lightberry.core.communication.response import Response
from lightberry.core.server import Server
from lightberry.utils import common_utils
from lightberry.config import AppConfig
from lightberry.tasks.aio import ATaskBase
from lightberry.tasks.threading import TaskBase

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type, Callable, Awaitable
    from asyncio import AbstractEventLoop
    from lightberry.core.routing.router import Router
    from lightberry.core.routing.route import Route
    from lightberry.core.communication.request import Request


class App:
    def __init__(self, debug_mode: bool = AppConfig.DEBUG):

        self.debug_mode: bool = debug_mode
        self.config: Type[AppConfig] = AppConfig

        self.get_host: Callable[[], str | None] | None = None
        self.get_mac_address: Callable[[], str | None] | None = None

        self.__routers: list[Router] = []
        self.__after_request_handler: Callable[[Response], Awaitable[Response]] | None = None

        self.__async_background_tasks: list[ATaskBase] = []
        self.__background_tasks: list[TaskBase] = []

        self.__print_debug("App has been created...")

    def run(self):
        server = Server(app=self)
        server.start()

    @property
    def routers(self):
        return self.__routers

    def add_background_task(self, task: TaskBase | ATaskBase):
        if task is None:
            raise Exception("Task can't be none")

        if isinstance(task, ATaskBase):
            self.__async_background_tasks.append(task)

        elif isinstance(task, TaskBase):
            self.__background_tasks.append(task)

        else:
            raise Exception("unrecognized task type")

    def register_async_background_tasks(self, events_loop: AbstractEventLoop):
        for task in self.__async_background_tasks:  # type: ATaskBase
            events_loop.create_task(task.handler())
            self.__print_debug(f"[TASKS] registering async task: {task.__class__.__name__}")

    def register_background_tasks(self):
        for task in self.__background_tasks:  # type: TaskBase
            task.start()
            self.__print_debug(f"[TASKS] registering threading task: {task.__class__.__name__}")

    def add_router(self, router: Router):
        if router is None:
            raise Exception("Router can't be none")

        router_existence_check = [True if router.name == r.name else False for r in self.__routers]

        if True in router_existence_check:
            raise Exception(f"Router '{router.name}' has already been added")

        self.__routers.append(router)

    async def requests_handler(self, request: Request) -> Response:
        response = Response(500)

        try:
            if request:
                self.__print_debug(f"request header: {request.headers}")
                self.__print_debug(f"request body: {request.body} | {type(request.body)}")

                response = await asyncio.wait_for(self.__process_request(request), self.config.TIMEOUT)

                self.__print_debug(f"response header: '{response.get_headers_string()}'")

        except Exception as e:
            self.__print_debug(f"error while handing request", exception=e)

        finally:
            return response

    async def __process_request(self, request: Request) -> Response:
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

    def __get_route_for_url(self, url: str) -> tuple[Route, Router]:
        target_route = None
        target_router = None

        for router in self.__routers:  # type: Router
            route = router.match_route(url)

            if route:
                target_route = route
                target_router = router
                break

        self.__print_debug(f"route for url '{url}': {target_route.handler.__name__ if target_route else None}")

        return target_route, target_router

    def after_request(self) -> Callable:
        def wrapper(func: Callable):
            self.__after_request_handler = func

        return wrapper

    def get_routers_prefixes(self, excluded: list[str] | None = None) -> list[str]:
        urls = []

        if excluded is None:
            excluded = []

        for router in self.__routers:  # type: Router
            if router.url_prefix not in excluded:
                urls.append(router.url_prefix)

        return urls

    def __print_debug(self, message: str, exception: Exception | None = None):
        common_utils.print_debug(message, "APP", debug_enabled=self.debug_mode, exception=exception)
