from lightberry.core.routing.route import Route


class Router:
    def __init__(self, name, url_prefix=None):
        self.name = name
        self.url_prefix = url_prefix

        self.routes = []

    def add_route(self, url, route_handler, methods):
        self.routes.append(Route(url, route_handler, methods))

    def route(self, url, methods=None):
        def wrapper(func):
            route_url = f"{self.url_prefix}{url}" if self.url_prefix else url

            if not self.check_if_url_added(url):
                self.add_route(route_url, func, methods)

            else:
                raise Exception(f"route for {url} has been already added")

        return wrapper

    def check_if_url_added(self, url):
        found = True if len([route for route in self.routes if route.url == url]) > 0 else False

        return found

    def match_route(self, url):
        target_route = None

        for route in self.routes:
            if route.match_url(url):
                target_route = route
                break

        return target_route
