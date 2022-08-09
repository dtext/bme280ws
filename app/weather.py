#!/usr/bin/env python3
import smbus2
import bme280


class Bme280:
    def __init__(self):
        self.port = 1
        self.address = 0x76
        self.bus = smbus2.SMBus(self.port)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
    
    def read_sensor(self):
        reading = bme280.sample(self.bus, self.address, self.calibration_params)
        return reading.temperature, reading.pressure, reading.humidity
        
if __name__ == "__main__":
    sensor = Bme280()
    t, p, h = sensor.read_sensor()
    print("It is %2f°C, with an air pressure of %2f hPa at %2f percent humidity" % (t, p, h))
