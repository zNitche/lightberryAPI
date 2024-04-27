from lightberry.utils import common_utils
import asyncio


class TaskBase:
    def __init__(self, periodic_interval=0, logging=False):
        self.is_periodic = periodic_interval > 0
        self.interval = periodic_interval

        self.logging = logging

    async def task(self):
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

    def __print_log(self, message=None, exception=None):
        if self.logging:
            target_message = f"Error while executing task {self.__class__.__name__}"
            target_message = f"{target_message}: {message}" if message else target_message

            common_utils.print_debug(target_message, debug_enabled=True, exception=exception)
