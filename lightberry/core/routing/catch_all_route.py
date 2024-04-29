from lightberry.core.routing.route import Route

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


class CatchAllRoute(Route):
    def __init__(self, handler: Callable, methods: list[str], excluded_routes: list[str] | None = None):
        super().__init__("", handler, methods)

        self.excluded_routes = excluded_routes if excluded_routes is not None else []

    def is_url_excluded(self, url: str) -> bool:
        is_excluded = False

        if url:
            for excluded_url_prefix in self.excluded_routes:
                if excluded_url_prefix and url.startswith(excluded_url_prefix):
                    is_excluded = True
                    break

        return is_excluded
