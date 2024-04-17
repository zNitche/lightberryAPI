from lightberry import Router, Response
from lightberry.shortcuts import jsonify


api = Router("api", url_prefix="/api")


@api.route("/health", methods=["GET"])
async def healthcheck(request):
    return Response(200)


@api.route("/resource/:id/details/:number", methods=["GET"])
async def resource_details(request, id, number):
    data = {"id": id, "number": number, "params": str(request.query_params)}

    return Response(200, payload=jsonify(data))
