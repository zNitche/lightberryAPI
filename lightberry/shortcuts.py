from lightberry.core.communication.response import Response
from lightberry.core.communication.file_response import FileResponse
from lightberry.core.app_context import AppContext
import json


def redirect(url: str) -> Response:
    response = Response(404)

    if url:
        response = Response(301)
        response.add_header("LOCATION", url)

    return response


def send_file(file_path: str, filename: str) -> FileResponse:
    response = FileResponse(file_path=file_path)
    response.add_header("Content-Disposition", f"attachment; filename={filename}")

    return response


def url_for(endpoint_name: str,
            path_parameters: dict[str, ...] | None = None,
            query_params: dict[str, ...] | None = None,
            external: bool = False) -> str | None:

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

    if endpoint_url and external:
        endpoint_url = f"{app.get_host()}{endpoint_url}"

    return endpoint_url


def jsonify(content: dict | list) -> str:
    return json.dumps(content)
