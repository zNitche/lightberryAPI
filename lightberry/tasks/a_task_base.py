from lightberry.utils import common_utils
import asyncio

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Awaitable


class ATaskBase:
    def __init__(self, init_delay: int = 0, periodic_interval: int = 0, logging: bool = False):
        self.init_delay: int = init_delay
        self.is_periodic: bool = periodic_interval > 0
        self.interval: int = periodic_interval

        self.logging: int = logging

    async def task(self) -> Awaitable[None]:
        raise NotImplementedError("task not implemented")

    async def handler(self):
        await asyncio.sleep(self.init_delay)

        while True:
            try:
                await self.task()

            except Exception as e:
                self._print_log(exception=e)

            if not self.is_periodic:
                break

            await asyncio.sleep(self.interval)

    def _print_log(self, message: str | None = None, exception: Exception | None = None):
        if self.logging:
            target_message = f"[ASYNC][{self.__class__.__name__}]"
            target_message = f"{target_message}: {message}" if message else target_message

            common_utils.print_debug(target_message, debug_enabled=True, exception=exception)
