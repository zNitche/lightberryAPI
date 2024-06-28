class HTTPConsts:
    CONTENT_LENGTH = "CONTENT-LENGTH"
    CONTENT_TYPE = "CONTENT-TYPE"
    CONTENT_ENCODING = "CONTENT-ENCODING"

    CONTENT_TYPE_JSON = "application/json"
    CONTENT_TYPE_CSS = "text/css"
    CONTENT_TYPE_HTML = "text/html"
    CONTENT_TYPE_JS = "text/javascript"
    CONTENT_TYPE_FORM_DATA = "application/x-www-form-urlencoded"
    CONTENT_TYPE_TEXT = "text/plain"
    CONTENT_TYPE_SVG = "image/svg+xml"
    CONTENT_JPEG = "image/jpeg"
    CONTENT_TYPE_PNG = "image/png"

    FILES_TYPES_BY_EXTENSION = {
        ".html": CONTENT_TYPE_HTML,
        ".css": CONTENT_TYPE_CSS,
        ".js": CONTENT_TYPE_JS,
        ".js.gz": CONTENT_TYPE_JS,
        ".css.gz": CONTENT_TYPE_CSS,
        ".txt": CONTENT_TYPE_TEXT,
        ".svg": CONTENT_TYPE_SVG,
        ".jpg": CONTENT_JPEG,
        ".jpeg": CONTENT_JPEG,
        ".png": CONTENT_TYPE_PNG,
        ".json": CONTENT_TYPE_JSON,
    }

    GZIP_COMPRESSED_CONTENT_EXTENSIONS = (".js.gz", ".css.gz")


class ServerConsts:
    LED_BLINK_PERIOD = 10
    WIFI_RECONNECT_PERIOD = 60
