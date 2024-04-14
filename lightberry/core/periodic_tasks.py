import asyncio
from lightberry.utils import machine_utils


async def blink_led(period, interval=10):
    led = machine_utils.get_onboard_led()

    while True:
        led.on()
        await asyncio.sleep_ms(interval)
        led.off()

        await asyncio.sleep_ms(period)


async def reconnect_to_network(is_connected, connection_handler, period):
    while True:
        await asyncio.sleep_ms(period)

        if not is_connected:
            connection_handler()
