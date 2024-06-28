from lightberry import Router, Response, AppContext

core = Router("core")


@core.catch_all()
async def home(request):
    current_app = AppContext.get_current_app()

    return Response(200, payload=f"Home, MAC: {current_app.mac_address}")
