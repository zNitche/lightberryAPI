from lightberry.core.routing.route import Route
from lightberry.core.routing.catch_all_route import CatchAllRoute

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Awaitable, Coroutine
    from lightberry.core.communication.response import Response
    from lightberry.core.communication.request import Request


class Router:
    def __init__(self, name: str, url_prefix: str | None = None):
        self.name: str = name
        self.url_prefix: str = url_prefix

        self.__routes: list[Route] = []
        self.__catch_all_route: CatchAllRoute | None = None
        self.after_request_handler: Callable[[Response], Awaitable[Response]] | None = None

    @property
    def routes(self):
        return self.__routes

    def add_route(self, url: str,
                  route_handler: Callable[[Request, ...],
                  Coroutine[Response]],
                  methods: list[str] | None = None):

        if not url or not route_handler:
            raise Exception("route url and handler can't be none")

        if not self.__check_if_url_added(url):
            if url == "/":
                route_url = f"{self.url_prefix}" if self.url_prefix else url

            else:
                route_url = f"{self.url_prefix}{url}" if self.url_prefix else url

            self.__routes.append(Route(route_url, route_handler, methods))

        else:
            raise Exception(f"route for {url} has been already added")

    def add_catch_all_route(self, route_handler, methods=None, excluded_routes=None):
        if not route_handler:
            raise Exception("catch all route handler can't be none")

        self.__catch_all_route = CatchAllRoute(route_handler, methods, excluded_routes)

    def __check_if_url_added(self, url: str) -> bool:
        found = True if len([route for route in self.__routes if route.url == url]) > 0 else False

        return found

    def route(self, url: str, methods: list[str] | None = None) -> Callable:
        def wrapper(func: Callable):
            self.add_route(url, func, methods)

        return wrapper

    def catch_all(self, methods: list[str] | None = None, excluded_routes: list[str] | None = None):
        def wrapper(func: Callable):
            self.add_catch_all_route(func, methods, excluded_routes)

        return wrapper

    def set_catch_all_excluded_routes(self, routes: list[str]):
        if self.__catch_all_route:
            self.__catch_all_route.excluded_routes = routes

    def after_request(self) -> Callable:
        def wrapper(func: Callable):
            self.after_request_handler = func

        return wrapper

    def match_route(self, url: str) -> Route | None:
        target_route: Route | None = None
        split_url = url.split("?")[0]
        split_test_url = split_url.split("/")

        for route in self.__routes:  # type: Route
            is_root_route = route.url == self.url_prefix and split_url == self.url_prefix

            if is_root_route or route.match_url(split_test_url, is_url_split=True):
                target_route = route
                break

        if target_route is None:
            if self.__catch_all_route is not None and not self.__catch_all_route.is_url_excluded(url):
                return self.__catch_all_route

        return target_route
