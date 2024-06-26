from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import StreamReader, StreamWriter


def url_encode(value: str | int | None) -> str | None:
    # currently only spaces are supported
    if value is None:
        return value

    return value.replace(" ", "%20")


def add_query_params_to_url(url: str, query_params: dict[str, ...]) -> str:
    if query_params:
        if not url.endswith("?"):
            url += "?"

        for index, query_param in enumerate(query_params):
            url += f"{query_param}={query_params[query_param]}"

            if index < len(query_params) - 1:
                url += "&"

    return url


async def load_request_header_from_stream(stream: StreamReader) -> str:
    request_header_string = ""

    while True:
        request_line = await stream.readline()
        request_line = request_line.decode()

        if request_line == "\r\n" or not request_line:
            break

        request_header_string += request_line

    return request_header_string


def write_to_stream(stream: StreamWriter, data: str, encoding="utf-8"):
    stream.write(bytes(data, encoding))
