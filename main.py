from lightberry import Server, App, AppContext
from lightberry.utils import common_utils, files_utils


def create_routers(app):
    from routes import api, core, home

    app.add_router(api)
    app.add_router(home)

    core.set_catch_all_excluded_routes(app.get_routers_prefixes())
    app.add_router(core)


def setup_tasks(app):
    import tasks

    app.add_background_task(tasks.ExampleAsyncTask())
    # app.add_background_task(tasks.ExampleThreadingTask())


def setup_app(app):
    setup_tasks(app)
    create_routers(app)


def main():
    common_utils.print_debug(f"Free space: {files_utils.get_free_space()} kB",
                             debug_enabled=True)

    # app = App()
    #
    # with AppContext(app):
    #     setup_app(app)
    #
    #     server = Server(app=app)
    #     server.start()

    # Or

    app = App()

    with AppContext(app):
        setup_app(app)
        app.run()


if __name__ == '__main__':
    main()
