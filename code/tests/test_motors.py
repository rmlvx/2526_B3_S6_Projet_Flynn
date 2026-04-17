import time
import config as cfg
from drivers.tmc2225 import TMC2225

def test_motors():
    print("--- TEST MATÉRIEL : MOTEURS TMC2225 ---")
    
    try:
        # 1. Initialization
        print("Initialisation GPIO...")
        motor_l = TMC2225(**cfg.MOTOR_LEFT_PINS, name="Gauche")
        motor_r = TMC2225(**cfg.MOTOR_RIGHT_PINS, name="Droit")
        print("[OK] Moteurs configurés sur les GPIO de la Pi.")

        # Test parameters
        vitesse = 400  # Hertz (step/second). Slow speed to avoid “skipping” steps
        tours = 1
        pas_par_tour = cfg.STEPS_PER_REV # Normally 3200 (200 × 16 microsteps)
        pas_total = tours * pas_par_tour

        while True:
            # 2. Left Engine Test
            # print(f"\n-> Moteur GAUCHE : {tours} tour(s) en avant à {vitesse}Hz...")
            # motor_l.move_async(steps=pas_total, speed_hz=vitesse)
            # time.sleep((pas_total / vitesse) + 1) # Attendre la fin du mouvement

            # print("-> Moteur GAUCHE : Retour...")
            # motor_l.move_async(steps=-pas_total, speed_hz=vitesse)
            # time.sleep((pas_total / vitesse) + 1)

            # 3. Right Engine Test
            # print(f"\n-> Moteur DROIT : {tours} tour(s) en avant à {vitesse}Hz...")
            # motor_r.move_async(steps=pas_total, speed_hz=vitesse)
            # time.sleep((pas_total / vitesse) + 1)

            # print("-> Moteur DROIT : Retour...")
            # motor_r.move_async(steps=-pas_total, speed_hz=vitesse)
            # time.sleep((pas_total / vitesse) + 1)

            # 4. Simultaneous Testing
            print("\n-> Les DEUX moteurs en même temps...")
            motor_l.set_speed(steps=pas_total, speed_hz=vitesse)
            motor_r.move_async(steps=-pas_total, speed_hz=vitesse) # Reverse (to move the robot forward)
            time.sleep((pas_total / vitesse) + 1)

            print("\n[SUCCÈS] Test terminé proprement.")

    except KeyboardInterrupt:
        print("\n[ARRÊT] Interruption par l'utilisateur.")
    except Exception as e:
        print(f"\n[ERREUR FATALE] {e}")
    finally:
        # Turn off the power to the motors so they don't overheat
        if 'motor_l' in locals(): motor_l.stop()
        if 'motor_r' in locals(): motor_r.stop()

if __name__ == "__main__":
    test_motors()