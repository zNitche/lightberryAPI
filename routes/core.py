from lightberry import Router, Response, AppContext, __version__
from lightberry.consts import HTTPConsts

core = Router("core")


@core.catch_all()
async def home(request):
    current_app = AppContext.get_current_app()

    return Response(200,
                    content_type=HTTPConsts.CONTENT_TYPE_TEXT,
                    payload=f"version: {__version__}, MAC: {current_app.server_handlers_manager.get_mac_address()}")
