class AppContext:
    def __init__(self, app):
        self.app = app

    def __enter__(self):
        global current_app
        current_app = self.app

    def __exit__(self, exc_type, exc_val, exc_tb):
        global current_app
        current_app = None

    @staticmethod
    def get_current_app(raise_exception=True):
        if current_app is None and raise_exception:
            raise Exception("trying to access current app out of app context")

        return current_app


# Contextvars would be perfect...
current_app = None
