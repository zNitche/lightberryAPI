from lightberry.tasks.aio import ATaskBase
from lightberry.tasks.threading import TaskBase


class ExampleAsyncTask(ATaskBase):
    def __init__(self):
        super().__init__(periodic_interval=10, init_delay=5)

    async def task(self):
        print("[A] Output from example background task...")


class ExampleThreadingTask(TaskBase):
    def __init__(self):
        super().__init__(periodic_interval=10)

    def task(self):
        print("[T] Output from example background task...")
