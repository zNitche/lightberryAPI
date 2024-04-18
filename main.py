from lightberry import Server, App, AppContext
from lightberry.utils import common_utils, files_utils


def create_routers(app):
    from routes import api, core

    app.add_router(api)
    app.add_router(core)


def create_app():
    app = App()

    with AppContext(app):
        import tasks

        app.add_background_task(tasks.ExampleTask())
        create_routers(app)

        return app


def main():
    common_utils.print_debug(f"Free space: {files_utils.get_free_space()} kB",
                             debug_enabled=True)

    app = create_app()
    server = Server(app=app)

    server.start()


if __name__ == '__main__':
    main()
