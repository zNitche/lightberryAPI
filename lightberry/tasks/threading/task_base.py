from lightberry.utils import common_utils
import time
import _thread


class TaskBase:
    def __init__(self, periodic_interval: int = 0, logging: bool = False):
        self.is_periodic: bool = periodic_interval > 0
        self.interval: int = periodic_interval

        self.logging: int = logging

    def task(self):
        raise NotImplementedError("task not implemented")

    def start(self):
        _thread.start_new_thread(self.handler, ())

    def handler(self):
        while True:
            try:
                self.task()

            except Exception as e:
                self.__print_log(exception=e)

            if not self.is_periodic:
                break

            time.sleep(self.interval)

    def __print_log(self, message: str | None = None, exception: Exception | None = None):
        if self.logging:
            target_message = f"[THREADING] Error while executing task {self.__class__.__name__}"
            target_message = f"{target_message}: {message}" if message else target_message

            common_utils.print_debug(target_message, debug_enabled=True, exception=exception)
