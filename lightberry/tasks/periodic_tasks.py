from lightberry.utils import common_utils
from lightberry.consts import ServerConsts
from lightberry.tasks.a_task_base import ATaskBase
import asyncio

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Awaitable


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
                 is_wlan_enabled: Callable[[], bool],
                 is_connected: Callable[[], bool],
                 connection_handler: Callable,
                 retires: int,
                 reconnect: bool,
                 logging: bool):
        super().__init__(periodic_interval=ServerConsts.WIFI_RECONNECT_PERIOD,
                         logging=logging)
        self.is_periodic = self.is_periodic and reconnect

        self.is_wlan_enabled = is_wlan_enabled
        self.retires = retires
        self.is_connected: Callable[[], bool] = is_connected
        self.connection_handler: Callable[[], Awaitable[None]] = connection_handler

    async def task(self):
        self._print_log(f"network check, connected: {self.is_connected()}")

        if self.is_wlan_enabled() and not self.is_connected():
            for try_id in range(self.retires):
                self._print_log(f"connecting... try: {try_id}")
                await self.connection_handler()

                if self.is_connected():
                    break

                await asyncio.sleep(3)

            self._print_log(f"connection status, connected: {self.is_connected()}")
