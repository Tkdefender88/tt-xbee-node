

class DataMapper:
    """
    Used to create simple y=mx+b data mapper function supply the data range of the sensor and you will get a function
    that can map your sensor to 000 to 999 output
    """
    DATA_RANGE = 9999 - 0000

    def __init__(self, sensor_max, sensor_min):
        self.m = DataMapper.DATA_RANGE / (sensor_max - sensor_min)
        self.b = -(self.m * sensor_min)

    def map(self, analog_value):
        return int(analog_value * self.m + self.b)
