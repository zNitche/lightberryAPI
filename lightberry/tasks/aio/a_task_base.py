from lightberry.utils import common_utils
import asyncio

from lightberry.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Awaitable


class ATaskBase:
    def __init__(self, periodic_interval: int = 0, logging: bool = False):
        self.is_periodic: bool = periodic_interval > 0
        self.interval: int = periodic_interval

        self.logging: int = logging

    async def task(self) -> Awaitable[None]:
        raise NotImplementedError("task not implemented")

    async def handler(self):
        while True:
            try:
                await self.task()

            except Exception as e:
                self.__print_log(exception=e)

            if not self.is_periodic:
                break

            await asyncio.sleep(self.interval)

    def __print_log(self, message: str | None = None, exception: Exception | None = None):
        if self.logging:
            target_message = f"[ASYNC] Error while executing task {self.__class__.__name__}"
            target_message = f"{target_message}: {message}" if message else target_message

            common_utils.print_debug(target_message, debug_enabled=True, exception=exception)
