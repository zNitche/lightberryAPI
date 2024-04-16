from lightberry.utils import machine_utils, common_utils
from lightberry.consts import ServerConsts
from lightberry.tasks.task_base import TaskBase
import asyncio


class BlinkLedTask(TaskBase):
    def __init__(self):
        super().__init__(periodic_interval=ServerConsts.LED_BLINK_PERIOD)
        self.led = machine_utils.get_onboard_led()

    async def task(self):
        self.led.on()
        await asyncio.sleep_ms(150)
        self.led.off()


class ReconnectToNetworkTask(TaskBase):
    def __init__(self, is_connected, connection_handler, logging):
        super().__init__(periodic_interval=ServerConsts.WIFI_RECONNECT_PERIOD,
                         logging=logging)

        self.is_connected = is_connected
        self.connection_handler = connection_handler

    async def task(self):
        common_utils.print_debug(f"[{self.__class__.__name__}] reconnecting WiFi, connected: {self.is_connected()}")

        if not self.is_connected():
            self.connection_handler()
