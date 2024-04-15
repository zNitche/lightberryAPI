from lightberry.core.communication.response import Response
from lightberry.core.communication.file_response import FileResponse


def redirect(url):
    response = Response(301)
    response.headers["LOCATION"] = url

    return response


def send_file(file_path, filename):
    response = FileResponse(file_path=file_path)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response
