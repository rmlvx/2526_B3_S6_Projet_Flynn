import time
import config as cfg
from drivers.tmc2225 import TMC2225

def test_motors():
    print("--- TEST MATÉRIEL : MOTEURS TMC2225 ---")
    
    try:
        # 1. Initialisation
        print("Initialisation GPIO...")
        motor_l = TMC2225(**cfg.MOTOR_LEFT_PINS, name="Gauche")
        motor_r = TMC2225(**cfg.MOTOR_RIGHT_PINS, name="Droit")
        print("[OK] Moteurs configurés sur les GPIO de la Pi.")

        # Paramètres de test
        vitesse = 400  # Hertz (pas/seconde). Vitesse lente pour éviter de "sauter" des pas
        tours = 1
        pas_par_tour = cfg.STEPS_PER_REV # Normalement 3200 (200 * 16 microsteps)
        pas_total = tours * pas_par_tour

        while True:
            # # 2. Test Moteur Gauche
            # print(f"\n-> Moteur GAUCHE : {tours} tour(s) en avant à {vitesse}Hz...")
            # motor_l.move_async(steps=pas_total, speed_hz=vitesse)
            # time.sleep((pas_total / vitesse) + 1) # Attendre la fin du mouvement

            # print("-> Moteur GAUCHE : Retour...")
            # motor_l.move_async(steps=-pas_total, speed_hz=vitesse)
            # time.sleep((pas_total / vitesse) + 1)

            # # 3. Test Moteur Droit
            # print(f"\n-> Moteur DROIT : {tours} tour(s) en avant à {vitesse}Hz...")
            # motor_r.move_async(steps=pas_total, speed_hz=vitesse)
            # time.sleep((pas_total / vitesse) + 1)

            # print("-> Moteur DROIT : Retour...")
            # motor_r.move_async(steps=-pas_total, speed_hz=vitesse)
            # time.sleep((pas_total / vitesse) + 1)

            # 4. Test Simultané
            print("\n-> Les DEUX moteurs en même temps...")
            motor_l.move_async(steps=pas_total, speed_hz=vitesse)
            motor_r.move_async(steps=-pas_total, speed_hz=vitesse) # Sens inverse (pour avancer le robot)
            time.sleep((pas_total / vitesse) + 1)

            print("\n[SUCCÈS] Test terminé proprement.")

    except KeyboardInterrupt:
        print("\n[ARRÊT] Interruption par l'utilisateur.")
    except Exception as e:
        print(f"\n[ERREUR FATALE] {e}")
    finally:
        # Coupe le courant des moteurs pour ne pas qu'ils chauffent inutilement
        if 'motor_l' in locals(): motor_l.stop()
        if 'motor_r' in locals(): motor_r.stop()

if __name__ == "__main__":
    test_motors()