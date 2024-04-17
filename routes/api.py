from lightberry import Router, Response
from lightberry.shortcuts import jsonify


api = Router("api", url_prefix="/api")


@api.route("/health", methods=["GET"])
async def healthcheck(request):
    return Response(200)


@api.route("/params/:p1/next/:p2", methods=["GET"])
async def params(request, p1, p2):
    data = {"p1": p1, "p2": p2, "params": str(request.query_params)}

    return Response(200, payload=jsonify(data))


@api.after_request()
async def after_request(response):
    print("API router after request...")
    return response
