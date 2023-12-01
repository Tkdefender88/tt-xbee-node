import hdc1080
from machine import I2C
import data_mapper


class TemperatureSensor:

    def __init__(self):
        self.i2c = I2C(1)
        self.mapper = data_mapper.DataMapper(sensor_max=125, sensor_min=-40)
        self.temp_sensor = hdc1080.HDC1080(self.i2c)

    def read_temperature(self):
        temp_c = self.temp_sensor.read_temperature(celsius=True)
        print('temp C', temp_c)
        print('temp F', (temp_c * 9/5 + 32))
        return self.mapper.map(temp_c)
