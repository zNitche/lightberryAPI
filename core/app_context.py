from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lightberry.core.app import App


# Contextvars would be perfect...
current_app: App | None = None


class AppContext:
    def __init__(self, app: App):
        self.app: App = app

    def __enter__(self):
        global current_app
        current_app = self.app

    def __exit__(self, exc_type, exc_val, exc_tb):
        global current_app
        current_app = None

    @staticmethod
    def get_current_app(raise_exception: bool = True) -> App:
        if current_app is None and raise_exception:
            raise Exception("trying to access current app out of app context")

        return current_app
