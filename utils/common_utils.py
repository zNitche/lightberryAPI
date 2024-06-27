import sys
import gc
import machine


def print_debug(message: str, origin: str = "CORE", debug_enabled: bool = False, exception: Exception | None = None):
    if debug_enabled:
        print(f"[{origin}][FREE_MEM: {int(gc.mem_free() / 1024)}kB] - {message}")

        if exception and isinstance(exception, Exception):
            sys.print_exception(exception)


def get_onboard_led() -> machine.Pin:
    return machine.Pin("LED", machine.Pin.OUT)


def get_readable_mac_address(encoded_mac: bytes) -> str:
    return ':'.join([f"{char:02X}" for char in encoded_mac])
