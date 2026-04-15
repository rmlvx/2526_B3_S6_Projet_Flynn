# test_dir_pin.py
import time
from gpiozero import DigitalOutputDevice

dir_pin = DigitalOutputDevice(16)  # GPIO 16 = DIR moteur gauche

print("DIR = HIGH (3.3V attendu sur la broche)")
dir_pin.value = 1
time.sleep(10)

print("DIR = LOW (0V attendu sur la broche)")
dir_pin.value = 0
time.sleep(10)

print("Fin.")