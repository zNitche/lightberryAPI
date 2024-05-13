from lightberry import Router, Response, AppContext
import time


async def root(request):
    return Response(payload="home")


async def home_test(request):
    return Response(payload="home test")


async def timeout_test(request):
    current_app = AppContext.get_current_app()
    time.sleep(current_app.config.TIMEOUT + 1)

    return Response(payload="timeout test")


home = Router("home", url_prefix="/home")
home.add_route("/", root)
home.add_route("/test", home_test)
home.add_route("/timeout_test", timeout_test)
