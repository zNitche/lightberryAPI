from lightberry.tasks.aio.a_task_base import ATaskBase
from lightberry.tasks.threading.task_base import TaskBase


class ExampleAsyncTask(ATaskBase):
    def __init__(self):
        super().__init__(periodic_interval=10)

    async def task(self):
        print("[A] Output from example background task...")


class ExampleThreadingTask(TaskBase):
    def __init__(self):
        super().__init__(periodic_interval=10)

    def task(self):
        print("[T] Output from example background task...")
