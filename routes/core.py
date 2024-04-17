from lightberry import Router, Response


core = Router("core", url_prefix="/panel")


@core.catch_all(methods=["GET"])
async def home(request):
    return Response(200)
