from lightberry.utils import common_utils
from lightberry.consts import ServerConsts
from lightberry.tasks.aio import ATaskBase
import asyncio

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


class BlinkLedTask(ATaskBase):
    def __init__(self):
        super().__init__(periodic_interval=ServerConsts.LED_BLINK_PERIOD)
        self.led = common_utils.get_onboard_led()

    async def task(self):
        self.led.on()
        await asyncio.sleep_ms(150)
        self.led.off()


class ReconnectToNetworkTask(ATaskBase):
    def __init__(self, is_connected: Callable[[], bool], connection_handler: Callable, logging: bool):
        super().__init__(periodic_interval=ServerConsts.WIFI_RECONNECT_PERIOD,
                         logging=logging)

        self.is_connected: Callable[[], bool] = is_connected
        self.connection_handler: Callable = connection_handler

    async def task(self):
        common_utils.print_debug(f"[{self.__class__.__name__}] reconnecting WiFi, connected: {self.is_connected()}")

        if not self.is_connected():
            self.connection_handler()
