import time
import math
import config as cfg
from drivers.lsm6dsox import LSM6DSOX
from PID import PIDController

def test_pid():
    print("--- TEST ASSERVISSEMENT (PID) ---")
    
    # 1. Initialisation de l'IMU
    try:
        imu = LSM6DSOX(bus_id=cfg.I2C_BUS_ID, address=cfg.LSM_ADDR)
        print("[OK] IMU Connecté.")
    except Exception as e:
        print(f"[ERREUR] Impossible de connecter l'IMU : {e}")
        return

    # 2. Initialisation du PID avec des coefficients de test
    # On commence par un test purement Proportionnel (P)
    # Kp = 50.0 (Pour 1 degré d'erreur, on demande une vitesse de 50)
    pid = PIDController(kp=50.0, ki=0.0, kd=0.0, target_angle=0.0)
    
    print("\n[OK] PID Prêt. Cible = 0° (Robot parfaitement droit).")
    print("Inclinez le robot d'avant en arrière pour voir la commande réagir !")
    print("-" * 70)
    
    try:
        while True:
            # A. Lecture de l'accéléromètre
            data = imu.read_all()
            ax, ay, az = data['accel']
            
            # B. Calcul de l'angle Theta en degrés (Axe de tangage / Pitch)
            # Selon comment votre carte est fixée, l'angle de chute se lit 
            # souvent entre l'axe X (avant/arrière) et l'axe Z (haut/bas).
            # S'il penche sur le côté, essayez math.atan2(ay, az)
            angle_rad = math.atan2(az, -ay)
            theta = math.degrees(angle_rad)
            
            # C. Calcul de la commande par le PID
            commande = pid.compute(theta)
            
            # D. Affichage visuel dans le terminal
            # Si la commande est positive, on met des "+" vers la droite
            # Si elle est négative, on met des "-" vers la gauche
            barre = ""
            if commande > 0:
                barre = "+" * min(int(commande / 10), 20)
            elif commande < 0:
                barre = "-" * min(int(abs(commande) / 10), 20)
            
            print(f"Data: {ax:6.1f}, {ay:6.1f}, {az:6.1f} | Angle: {theta:6.1f}° | Erreur: {-theta:6.1f}° | Commande: {commande:8.1f} [{barre:<20}]", end='\r')
            
            time.sleep(0.05) # 20 Hz (20 fois par seconde)

    except KeyboardInterrupt:
        print("\n\n[ARRÊT] Fin du test PID.")

if __name__ == "__main__":
    test_pid()