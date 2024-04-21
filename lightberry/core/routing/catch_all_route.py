from lightberry.core.routing.route import Route


class CatchAllRoute(Route):
    def __init__(self, handler, methods, excluded_routes=None):
        super().__init__("", handler, methods)

        self.excluded_routes = excluded_routes if excluded_routes is not None else []

    def is_url_excluded(self, url):
        is_excluded = False

        if url:
            for inner_url in self.excluded_routes:
                if inner_url and url.startswith(inner_url):
                    is_excluded = True
                    break

        return is_excluded
