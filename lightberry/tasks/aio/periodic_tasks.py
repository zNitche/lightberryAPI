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


class ConnectToNetworkTask(ATaskBase):
    def __init__(self,
                 is_connected: Callable[[], bool],
                 connection_handler: Callable,
                 retires: int,
                 reconnect: bool,
                 logging: bool):
        super().__init__(periodic_interval=ServerConsts.WIFI_RECONNECT_PERIOD,
                         logging=logging)
        self.is_periodic = self.is_periodic and reconnect

        self.retires = retires
        self.is_connected: Callable[[], bool] = is_connected
        self.connection_handler: Callable = connection_handler

    async def task(self):
        self.__print_log(f"network check, connected: {self.is_connected()}")

        if not self.is_connected():
            for try_id in range(self.retires):
                self.__print_log(f"connecting... try: {try_id}")
                await self.connection_handler()

                if self.is_connected():
                    break

                await asyncio.sleep(3)

            self.__print_log(f"connection status, connected: {self.is_connected()}")
