import sys
import gc


def print_debug(origin, message, debug_enabled=False, exception=None):
    if debug_enabled:
        print(f"[{origin}][FREE_MEM: {int(gc.mem_free() / 1024)}kB] - {message}")

        if exception and isinstance(exception, Exception):
            sys.print_exception(exception)
