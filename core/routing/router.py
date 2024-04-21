from lightberry.core.routing.route import Route
from lightberry.core.routing.catch_all_route import CatchAllRoute


class Router:
    def __init__(self, name, url_prefix=None):
        self.name = name
        self.url_prefix = url_prefix

        self.__routes = []
        self.__catch_all_route = None
        self.after_request_handler = None

    @property
    def routes(self):
        return self.__routes

    def __add_route(self, url, route_handler, methods):
        self.__routes.append(Route(url, route_handler, methods))

    def __check_if_url_added(self, url):
        found = True if len([route for route in self.__routes if route.url == url]) > 0 else False

        return found

    def route(self, url, methods=None):
        def wrapper(func):
            route_url = f"{self.url_prefix}{url}" if self.url_prefix else url

            if not self.__check_if_url_added(url):
                self.__add_route(route_url, func, methods)

            else:
                raise Exception(f"route for {url} has been already added")

        return wrapper

    def catch_all(self, methods=None, excluded_routes=None):
        def wrapper(func):
            self.__catch_all_route = CatchAllRoute(func, methods, excluded_routes)

        return wrapper

    def set_catch_all_excluded_routes(self, routes):
        if self.__catch_all_route:
            self.__catch_all_route.excluded_routes = routes

    def after_request(self):
        def wrapper(func):
            self.after_request_handler = func

        return wrapper

    def match_route(self, url):
        target_route = None

        for route in self.__routes:
            if route.match_url(url):
                target_route = route
                break

        if self.__catch_all_route is not None and not self.__catch_all_route.is_url_excluded(url):
            return self.__catch_all_route

        return target_route
