# test_motor_signs.py
# Run this script BEFORE performing any load balancing tests.
# It verifies that each motor is rotating in the correct direction based on the speed sign.

import time
import config as cfg
from drivers.tmc2225 import TMC2225

def test_motor_signs():
    print("=== DIAGNOSTIC SIGNE MOTEURS ===")
    print("Observez physiquement le sens de rotation des roues.\n")

    motor_l = TMC2225(**cfg.MOTOR_LEFT_PINS, name="Gauche")
    motor_r = TMC2225(**cfg.MOTOR_RIGHT_PINS, name="Droit")
    motor_l.enable()
    motor_r.enable()

    tests = [
        # ("Moteur GAUCHE — vitesse POSITIVE (+300 Hz)", motor_l, +300),
        # ("Moteur GAUCHE — vitesse NEGATIVE (-300 Hz)", motor_l, -300),
        ("Moteur DROIT  — vitesse POSITIVE (+300 Hz)", motor_r, +300),
        ("Moteur DROIT  — vitesse NEGATIVE (-300 Hz)", motor_r, -300),
    ]

    for label, motor, speed in tests:
        print(f"[TEST] {label}")
        print("       Appuyez sur Entrée pour démarrer...")
        input()
        motor.set_speed(speed)
        time.sleep(10)
        motor.set_speed(0)
        print("       Moteur arrêté.\n")

    motor_l.stop()
    motor_r.stop()
    print("=== FIN DU DIAGNOSTIC ===")

if __name__ == "__main__":
    try:
        while True :
            test_motor_signs()
    except KeyboardInterrupt:
        print("CTRL + C")