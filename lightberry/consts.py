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

    FILES_TYPES_BY_EXTENSION = {
        ".css": CONTENT_TYPE_CSS,
        ".js": CONTENT_TYPE_JS,
        ".html": CONTENT_TYPE_HTML,
        ".txt": CONTENT_TYPE_TEXT,
    }


class ServerConsts:
    LED_BLINK_PERIOD_WIFI_CONNECTING = 250
    LED_BLINK_WIFI_CONNECTED = 3000

    WIFI_RECONNECT_PERIOD = 300000
