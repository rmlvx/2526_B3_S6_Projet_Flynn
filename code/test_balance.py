import time
import math
import config as cfg
from drivers.lsm6dsox import LSM6DSOX
from drivers.tmc2225 import TMC2225
from PID import PIDController
from Kalman import KalmanFilter1D

def test_balance():
    print("--- TEST D'ÉQUILIBRE (FILTRE COMPLÉMENTAIRE & PID) ---")
    
    try:
        imu = LSM6DSOX(bus_id=cfg.I2C_BUS_ID, address=cfg.LSM_ADDR)
        motor_l = TMC2225(**cfg.MOTOR_LEFT_PINS, name="Gauche")
        motor_r = TMC2225(**cfg.MOTOR_RIGHT_PINS, name="Droit")
        
        motor_l.enable()
        motor_r.enable()
        
        # On ajoute le "Kd" (Le frein anticipatif)
        # (Suite du code existant avant la boucle...)
        pid = PIDController(kp=0.8, ki=0.0, kd=5.0, target_angle=0.0)
        
        # Initialisation du Filtre de Kalman
        from Kalman import KalmanFilter1D 
        kalman = KalmanFilter1D()
        
        print("[OK] Système prêt. Le robot utilise tes fonctions TMC2225 réelles !")
        
        # ATTENTION : On supprime les motor_l.start() qui n'existent pas dans ton driver.
        
        prev_time = time.time()
        
        while True:
            data = imu.read_all()
            
            # Récupération de l'accéléromètre ET du gyroscope
            ax, ay, az = data['accel']
            gx, gy, gz = data['gyro'] 
            
            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time
            
            if dt <= 0.0 or dt > 0.1:
                dt = 0.01 
            
            # 1. Calcul de l'angle via Kalman
            accel_angle = math.degrees(math.atan2(az, -ay))
            theta = kalman.get_angle(accel_angle, gx, dt)
            
            # 2. Calcul de la commande (vitesse en Hz) par le PID
            commande = pid.compute(theta)
            
            # 3. Conversion de la vitesse en nombre de pas pour ce cycle de 10ms
            # La commande est en pas/seconde. On multiplie par dt (secondes) pour avoir le nombre de pas immédiat
            steps_to_move = int(commande * dt)
            speed = abs(commande)
            
            # 4. Envoi de la commande avec tes fonctions
            # On doit impérativement stopper le thread précédent pour que move_async accepte le nouveau
            motor_l.stop()
            motor_r.stop()
            
            # On lance le thread pour les prochains 10ms (avec acceleration=False pour être réactif)
            if abs(steps_to_move) > 0 and speed > 5.0:
                motor_l.move_async(steps_to_move, speed, acceleration=False)
                # Remarque : si un moteur est monté en face de l'autre, ajoute un signe "-" devant steps_to_move
                motor_r.move_async(-steps_to_move, speed, acceleration=False) 
            
            # Affichage console
            print(f"Angle Kalman: {theta:6.1f}° | Cmd: {commande:8.0f} Hz | Pas/cycle: {steps_to_move:3d}   ", end='\r')
            
            time.sleep(0.01) # Maintien de la boucle à environ 100 Hz
            
    except KeyboardInterrupt:
        print("[ARRET]")


if __name__=="__main__":
    test_balance()