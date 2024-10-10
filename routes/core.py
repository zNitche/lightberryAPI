from lightberry import Router, Response, AppContext, __version__

core = Router("core")


@core.catch_all()
async def home(request):
    current_app = AppContext.get_current_app()

    return Response(200, payload=f"version: {__version__}, MAC: {current_app.get_mac_address()}")
