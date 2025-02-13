from lightberry import Router, Response, AppContext
from lightberry.consts import HTTPConsts
import time


async def root(request):
    return Response(payload="home", content_type=HTTPConsts.CONTENT_TYPE_TEXT)


async def home_test(request):
    return Response(payload="home test", content_type=HTTPConsts.CONTENT_TYPE_TEXT)


async def timeout_test(request):
    current_app = AppContext.get_current_app()
    time.sleep(current_app.config.TIMEOUT + 1)

    return Response(payload="timeout test", content_type=HTTPConsts.CONTENT_TYPE_TEXT)


home = Router("home", url_prefix="/home")
home.add_route("/", root)
home.add_route("/test", home_test)
home.add_route("/timeout-test", timeout_test)
