from math import pi

# --- SYSTÈME ---
# Sur Raspberry Pi Zero 2W (BCM numbering)
I2C_BUS_ID = 1
SPI_BUS_ID = 0
SPI_DEVICE_ID = 0  # Correspond à la Pin 24 (CE0 / GPIO 8)

# --- CAPTEURS ---
LSM_ADDR = 0x6A    # Adresse I2C par défaut du LSM6DSOX
ADC_VREF = 3.3     # Tension de référence (3.3V)

# --- MOTEURS (TMC2225) ---
# Conversion Pin Physique -> GPIO BCM :
# MOTEUR 1 (Gauche)
# STEP: Pin 32 -> GPIO 12
# DIR:  Pin 36 -> GPIO 16

# MOTEUR 2 (Droit)
# STEP: Pin 33 -> GPIO 13
# DIR:  Pin 31 -> GPIO 6 (Correction appliquée)

MOTOR_LEFT_PINS = {
    'STEP': 12,
    'DIR': 16,
    'EN': None   # Pas connecté sur le schéma (toujours activé hardware)
}

MOTOR_RIGHT_PINS = {
    'STEP': 13,
    'DIR': 6,
    'EN': None   # Pas connecté sur le schéma
}

# --- PARAMÈTRES MÉCANIQUES ---
MICROSTEPS = 16
STEPS_PER_REV = 200 * MICROSTEPS
WHEEL_DIAMETER_MM = 65
MM_PER_STEP = (WHEEL_DIAMETER_MM * pi) / STEPS_PER_REV