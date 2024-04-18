import sys
import gc
import machine


def print_debug(message, origin="CORE", debug_enabled=False, exception=None):
    if debug_enabled:
        print(f"[{origin}][FREE_MEM: {int(gc.mem_free() / 1024)}kB] - {message}")

        if exception and isinstance(exception, Exception):
            sys.print_exception(exception)


def get_onboard_led():
    return machine.Pin("LED", machine.Pin.OUT)
