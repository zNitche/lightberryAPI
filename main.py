from lightberry import Server, App
from lightberry.utils import common_utils, files_utils


def create_app():
    app = App()

    from routes.api import api
    app.add_router(api)

    return app


def main():
    common_utils.print_debug(f"Free space: {files_utils.get_free_space()} kB",
                             debug_enabled=True)

    app = create_app()
    server = Server(app=app)

    server.start()


if __name__ == '__main__':
    main()
