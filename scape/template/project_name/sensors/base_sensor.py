from scape.core.sensor import Sensor


class BaseSensor(Sensor):
    def __init__(self):
        super().__init__()

    @staticmethod
    def say():
        return 'say'

    @staticmethod
    def hello():
        return 'hello'
