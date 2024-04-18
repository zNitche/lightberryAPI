from routes.api import api
from routes.core import core

from lightberry import AppContext

current_app = AppContext.get_current_app()


@current_app.after_request()
async def after_request(response):
    print("app after request")

    return response
