from .base_sensor import BaseSensor


class HelloSensor(BaseSensor):
    def __init__(self):
        super().__init__()

    def say_hello(self):
        return self.say() + " " + self.hello()
