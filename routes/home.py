from lightberry import Router, Response


async def root(request):
    return Response(payload="home")


async def home_test(request):
    return Response(payload="home test")


home = Router("home", url_prefix="/home")
home.add_route("/", root)
home.add_route("/test", home_test)
