from lightberry import TaskBase


class ExampleTask(TaskBase):
    def __init__(self):
        super().__init__(periodic_interval=10)

    async def task(self):
        print("Output from example background task...")
