from lightberry.core.communication.response import Response
from lightberry.core.communication.file_response import FileResponse
from lightberry.core.app_context import AppContext
import json


def redirect(url):
    response = Response(404)

    if url:
        response = Response(301)
        response.headers["LOCATION"] = url

    return response


def send_file(file_path, filename):
    response = FileResponse(file_path=file_path)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response


def url_for(endpoint_name, path_parameters=None, query_params=None):
    endpoint_url = None
    app = AppContext.get_current_app()

    for router in app.routers:
        for route in router.routes:
            route_full_name = f"{router.name}.{route.handler.__name__}"

            if route_full_name == endpoint_name:
                endpoint_url = route.url if not route.accepts_path_params\
                    else route.concat_url_with_parameters(path_parameters, query_params)

                break

            if endpoint_url is not None:
                break

    return endpoint_url


def jsonify(content):
    return json.dumps(content)
