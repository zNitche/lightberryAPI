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
        try:
            while True:
                await self.task()

                if not self.is_periodic:
                    break

                await asyncio.sleep(self.interval)

        except Exception as e:
            common_utils.print_debug(f"Error while executing task {self.__class__.__name__}",
                                     self.logging, exception=e)
