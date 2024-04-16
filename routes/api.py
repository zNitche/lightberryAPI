from lightberry import Router, Response
from lightberry.shortcuts import jsonify


api = Router("api", url_prefix="/api")


@api.route("/health", methods=["GET"])
def healthcheck(request):
    return Response(200)


@api.route("/resource/:id/details", methods=["GET"])
def resource_details(request, id):
    return Response(200, payload=jsonify({"id": id, "params": str(request.query_params)}))
