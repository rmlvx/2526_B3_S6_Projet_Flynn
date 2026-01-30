# config.py
import board  # Si utilisation de Blinka, sinon on utilise les numéros BCM directs

# --- PINOUT (BCM) ---
# Moteur 1
MOTOR1_STEP_PIN = 17
MOTOR1_DIR_PIN = 27
MOTOR1_EN_PIN = 22

# Moteur 2
MOTOR2_STEP_PIN = 23
MOTOR2_DIR_PIN = 24
MOTOR2_EN_PIN = 25

# SPI (MCP3208) - Le hardware SPI0 est sur GPIO 10(MOSI), 9(MISO), 11(CLK), 8(CE0)
ADC_SPI_BUS = 0
ADC_SPI_DEVICE = 0  # CE0

# I2C (LSM6DSOX)
IMU_I2C_BUS = 1
IMU_ADDRESS = 0x6A  # Adresse par défaut (ou 0x6B)

# --- CONSTANTES ---
VREF_ADC = 3.3  # Tension de référence ADC
MOTOR_ACCEL_RATE = 0.0005  # Délai en moins par pas pour l'accélération