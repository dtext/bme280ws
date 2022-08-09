#!/usr/bin/env python3
from fastapi import FastAPI
from .weather import Bme280

sensor = Bme280()

app = FastAPI()

@app.get("/")
def get_all():
    t, p, h = sensor.read_sensor()
    return {
        "temperature": t,
        "humidity": h,
        "pressure": p
    }

@app.get("/temperature")
def get_temp():
    t, _, _ = sensor.read_sensor()
    return t

@app.get("/humidity")
def get_humid():
    _, p, _ = sensor.read_sensor()
    return p

@app.get("/pressure")
def get_pressure():
    _, _, h = sensor.read_sensor()
    return h