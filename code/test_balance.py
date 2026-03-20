import time
import math
import config as cfg
from drivers.lsm6dsox import LSM6DSOX
from drivers.tmc2225 import TMC2225
from PID import PIDController

def test_balance():
    print("--- TEST D'ÉQUILIBRE (FILTRE COMPLÉMENTAIRE & PID) ---")
    
    try:
        imu = LSM6DSOX(bus_id=cfg.I2C_BUS_ID, address=cfg.LSM_ADDR)
        motor_l = TMC2225(**cfg.MOTOR_LEFT_PINS, name="Gauche")
        motor_r = TMC2225(**cfg.MOTOR_RIGHT_PINS, name="Droit")
        
        motor_l.start()
        motor_r.start()
        
        # On ajoute le "Kd" (Le frein anticipatif)
        pid = PIDController(kp=0.8, ki=0.0, kd=5.0, target_angle=0.0)
        
        print("[OK] Système prêt. Le robot utilise désormais son oreille interne (Gyro) !")
        
        # Variables pour le Filtre Complémentaire
        theta = 0.0
        alpha = 0.8
        prev_time = time.time()
        
        while True:
            data = imu.read_all()
            
            # Récupération de l'accéléromètre ET du gyroscope
            ax, ay, az = data['accel']
            gx, gy, gz = data['gyro'] 
            
            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time
            
            # 1. Calcul de l'angle "Bruité" via l'accéléromètre (Votre formule magique)
            accel_angle = math.degrees(math.atan2(az, -ay))
            
            # 2. Le Filtre Complémentaire
            # L'axe de rotation des roues correspond à l'axe X de la carte (donc 'gx')
            # (Si l'angle part à l'envers quand vous le penchez, remplacez + gx par - gx)
            theta = alpha*theta + (1 - alpha) * (0.8 * (theta + gx * dt) + 0.2 * accel_angle)
            
            # 3. Calcul de la vitesse par le PID
            commande = pid.compute(theta)
            
            # 4. Envoi de la commande
            motor_l.set_speed(commande)
            motor_r.set_speed(commande) # En miroir
            
            # Affichage console pour comparer la magie du filtre
            print(f"Angle Filtré: {theta:6.1f}° | Accel pur: {accel_angle:6.1f}° | Gyro: {gx:6.1f}, {gy:6.1f}, {gy:6.1f} | Cmd: {commande:8.0f} Hz   ", end='\r')
            
            time.sleep(0.01) # On passe à 100 Hz pour que le Gyro soit ultra précis

    except KeyboardInterrupt:
        print("\n\n[ARRÊT] Moteurs coupés.")
    finally:
        if 'motor_l' in locals(): motor_l.stop()
        if 'motor_r' in locals(): motor_r.stop()

if __name__ == "__main__":
    test_balance()