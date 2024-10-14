from lightberry.tasks import ATaskBase, TaskBase


class ExampleAsyncTask(ATaskBase):
    def __init__(self):
        super().__init__(periodic_interval=10, init_delay=5, logging=True)

    async def task(self):
        self._print_log("Output from example background task...")


class ExampleThreadingTask(TaskBase):
    def __init__(self):
        super().__init__(periodic_interval=10, logging=True)

    def task(self):
        self._print_log("Output from example background task...")
