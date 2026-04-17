from math import pi

# --- SYSTEM ---
# Sur Raspberry Pi Zero 2W (BCM numbering)
I2C_BUS_ID = 1
SPI_BUS_ID = 0
SPI_DEVICE_ID = 0  # Correspond à la Pin 24 (CE0 / GPIO 8)

# --- CAPTEURS ---
LSM_ADDR = 0x6A    # Adresse I2C par défaut du LSM6DSOX
ADC_VREF = 3.3     # Tension de référence (3.3V)

# --- MOTORS (TMC2225) ---
# Physical Pin to BCM GPIO Conversion:
# MOTOR 1 (Left)
# STEP: Pin 32 -> GPIO 12
# DIR:  Pin 36 -> GPIO 16

# MOTOR 2 (Right)
# STEP: Pin 33 -> GPIO 13
# DIR:  Pin 31 -> GPIO 6

# ‘invert’: Set to True if the motor is rotating in the opposite direction from the other one.
# Rule: Tilt the robot forward by hand.
#   → Both wheels move forward          → both invert=False (correct)
#   → One wheel moves forward, the other moves backward  → set invert=True for the one moving backward
#   → Both wheels move backward          → reverse the command sign in test_balance.py

MOTOR_LEFT_PINS = {
    'STEP': 12,
    'DIR': 16,
    'EN': None,
    'invert': True  # ← Set to True if the left motor is spinning backward / The LEFT motor failed the test_motors
}

MOTOR_RIGHT_PINS = {
    'STEP': 13,
    'DIR': 6,
    'EN': None,
    'invert': False   # ← Set to False if the right motor is rotating in the correct direction
}

# --- MECHANICAL SPECIFICATIONS ---
MICROSTEPS = 16
STEPS_PER_REV = 200 * MICROSTEPS
WHEEL_DIAMETER_MM = 65
MM_PER_STEP = (WHEEL_DIAMETER_MM * pi) / STEPS_PER_REV