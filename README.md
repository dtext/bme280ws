# bme280ws

This is a REST service written in python using fastapi that reads data from a Bosch BME280 sensor
connected to a raspberry pi's I2C bus.

## Wait, what?

Bosch's BME280 sensor is a small, low cost, low power sensor that measures ambient temperature,
pressure and relative humidity. Data is read via an I2C or SPI bus, both of which are provided by
the Raspberry Pi 4.

I'm using the Raspberry Pi 4 to host an instance of homeassistant, an open source and (mostly)
excellent community home automation solution. Up until recently (mid-2022, that is), the team
provided support for a BME280 connected to the Pi's I2C bus, offering me a great, simple and
low-cost solution to most of my measurement needs.

Sadly, since then, the team decided to not only drop support for anything GPIO, but also to remove
all integrations using it entirely. At that point, I already had [weather.py](app/weather.py) lying
around from playing with the sensor before, and thus this project was born. At this point, I like to
thank the kind developer who put their python code up for everyone to use in a blog article that I
sadly can't seem to find anymore.

What problem do I solve doing it this way? Instead of _just using ESPHome_ (which actually seems to
be a wonderful project as far as I can tell!) as mostly everyone suggested, I decided to stitch
together something in software so my smooth software developer brain wouldn't have to deal with
hardware problems like powering an ESP32 or ESP8266 and having all that gross wiring dangling
everywhere.

But how does that solve my problem? Great question! As long as the homeassistant team doesn't decide
to remove the RESTful sensor integration, I can use it to query sensor data via HTTP from an API
wrapping my wonderful [weather.py](app/weather.py), which hasn't changed much in about 3 years. What
a burden to maintain, indeed! (I'm kidding here, big thanks to the kind developers
of [RPi.bme280](https://pypi.org/project/RPi.bme280/)!).

## How do run?

Currently, I'm building the image using docker on my Raspberry Pi. However, it should be possible to
build it on any arm64 or using cross-architecture support. I haven't looked into that yet.
Right now, running the following on an RPi4 with this repository checked out does the trick:

```shell
docker build -t sensor .
```

### Compose File

As I am running homeassistant along with other software using docker compose, here is the relevant
part of my `docker-compose.yml` to properly run this image in a setup like mine:

```
version: "3"

services:

  sensor:
    image: sensor:latest
    container_name: sensor
    devices:
      - /dev/i2c-1:/dev/i2c-1
    privileged: true
    restart: unless-stopped
    
  ...
```

### Sensor Configuration in homeassistant

This way, my homeassistant instance can reach the sensor data server at `http://sensor/`. How do I
make use of that? Easy! Just squeeze out some more YAML, you can do it! Here is the relevant excerpt
from the `configuration.yml` used by homeassistant.

```
sensor:
  - platform: rest
    name: ambient_sensor
    resource: http://sensor/
    json_attributes:
      - temperature
      - pressure
      - humidity
    icon: mdi:chip
  - platform: template
    sensors:
      temperature:
        value_template: "{{ state_attr('sensor.ambient_sensor', 'temperature') | round(1) }}"
        device_class: temperature
        unit_of_measurement: "°C"
      pressure:
        value_template: "{{ state_attr('sensor.ambient_sensor', 'pressure') | round(0) }}"
        device_class: pressure
        unit_of_measurement: "mbar"
      humidity:
        value_template: "{{ state_attr('sensor.ambient_sensor', 'humidity') | round(0) }}"
        device_class: humidity
        unit_of_measurement: "%"
      outside_temperature:
        value_template: "{{ state_attr('weather.home', 'temperature') | round(1) }}"
        device_class: temperature
        unit_of_measurement: "°C"

```

## Why Python?

Because. Look, I'm not particularly happy about it either. At least, fastapi seems to be the way to
go about it these days, and it works well for me. 

## Why not X?

Probably because I didn't care to look into it before.

## But docker privileged evil!

I know, I know. It's gonna be alright :)