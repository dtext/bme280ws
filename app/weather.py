#!/usr/bin/env python3
import smbus2
import bme280
import sys


def get_bme280_or_exit():
    for i in range(1, 13):
        try:
            print("trying to initialize on /dev/i2c-{}".format(i))
            sensor = Bme280(i)
            print("successful initialization".format(i))
            return sensor
        except OSError:
            continue
    sys.exit("could not initialize I2C bus connection with sensor")


class Bme280:
    def __init__(self, port):
        self.address = 0x76
        self.bus = smbus2.SMBus(port)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

    def read_sensor(self):
        reading = bme280.sample(self.bus, self.address, self.calibration_params)
        return reading.temperature, reading.pressure, reading.humidity


if __name__ == "__main__":
    sensor = Bme280()
    t, p, h = sensor.read_sensor()
    print("It is %2f°C, with an air pressure of %2f hPa at %2f percent humidity" % (t, p, h))
