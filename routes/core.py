from lightberry import Router, Response


core = Router("core")


@core.catch_all(excluded_routes=["/api"])
async def home(request):
    return Response(200, payload="Home")
