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
# DIR:  Pin 31 -> GPIO 6

# 'invert' : mettre True si le moteur tourne à l'envers par rapport à l'autre.
# Règle : pencher le robot vers l'avant à la main.
#   → Les deux roues avancent          → les deux invert=False (correct)
#   → Une roue avance, l'autre recule  → mettre invert=True sur celle qui recule
#   → Les deux roues reculent          → inverser le signe de commande dans test_balance.py

MOTOR_LEFT_PINS = {
    'STEP': 12,
    'DIR': 16,
    'EN': None,
    'invert': True  # ← changer en True si le moteur gauche tourne à l'envers / Le moteur GAUCHE a échoué au test_motors
}

MOTOR_RIGHT_PINS = {
    'STEP': 13,
    'DIR': 6,
    'EN': None,
    'invert': False   # ← changer en False si le moteur droit tourne dans le bon sens
}

# --- PARAMÈTRES MÉCANIQUES ---
MICROSTEPS = 16
STEPS_PER_REV = 200 * MICROSTEPS
WHEEL_DIAMETER_MM = 65
MM_PER_STEP = (WHEEL_DIAMETER_MM * pi) / STEPS_PER_REV