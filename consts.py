class HTTPConsts:
    HOST_KEY = "HOST"
    CONTENT_LENGTH = "CONTENT-LENGTH"
    CONTENT_TYPE = "CONTENT-TYPE"

    CONTENT_TYPE_JSON = "application/json"
    CONTENT_TYPE_CSS = "text/css"
    CONTENT_TYPE_HTML = "text/html"
    CONTENT_TYPE_JS = "text/javascript"
    CONTENT_TYPE_FORM_DATA = "application/x-www-form-urlencoded"
    CONTENT_TYPE_TEXT = "text/plain"
    CONTENT_TYPE_SVG = "image/svg+xml"

    FILES_TYPES_BY_EXTENSION = {
        ".css": CONTENT_TYPE_CSS,
        ".js": CONTENT_TYPE_JS,
        ".html": CONTENT_TYPE_HTML,
        ".txt": CONTENT_TYPE_TEXT,
        ".svg": CONTENT_TYPE_SVG,
    }


class ServerConsts:
    LED_BLINK_PERIOD = 10
    WIFI_RECONNECT_PERIOD = 120
