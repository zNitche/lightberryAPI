from lightberry import Router, Response
from lightberry.shortcuts import jsonify

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lightberry import Request


api = Router("api", url_prefix="/api")


@api.route("/health", methods=["GET"])
async def healthcheck(request):
    return Response(200)


@api.route("/params/:p1/next/:p2", methods=["GET"])
async def params(request: Request, p1, p2):
    data = {"p1": p1, "p2": p2, "params": str(request.query_params)}

    return Response(payload=jsonify(data))


@api.after_request()
async def after_request(response: Response):
    print("API router after request...")
    return response
