import time
import math
import config as cfg
from drivers.lsm6dsox import LSM6DSOX
from PID import PIDController

def test_pid():
    print("--- TEST ASSERVISSEMENT (PID) ---")
    
    # 1. Initializing the IMU
    try:
        imu = LSM6DSOX(bus_id=cfg.I2C_BUS_ID, address=cfg.LSM_ADDR)
        print("[OK] IMU Connecté.")
    except Exception as e:
        print(f"[ERREUR] Impossible de connecter l'IMU : {e}")
        return

    # 2. Initializing the PID with test coefficients
    # We start with a purely proportional (P) test
    # Kp = 50.0 (For every 1 degree of error, we set the speed to 50)
    pid = PIDController(kp=50.0, ki=0.0, kd=0.0, target_angle=0.0)
    
    print("\n[OK] PID Prêt. Cible = 0° (Robot parfaitement droit).")
    print("Inclinez le robot d'avant en arrière pour voir la commande réagir !")
    print("-" * 70)
    
    try:
        while True:
            # A. Accelerometer Reading
            data = imu.read_all()
            ax, ay, az = data['accel']
            
            # B. Calculating the angle Theta in degrees (Pitch axis)
            # Depending on how your board is mounted, the pitch angle is often measured
            # between the X-axis (forward/backward) and the Z-axis (up/down).
            # If it is tilted to the side, try math.atan2(ay, az)
            angle_rad = math.atan2(az, -ay)
            theta = math.degrees(angle_rad)
            
            # C. Calculating the control signal using PID
            commande = pid.compute(theta)
            
            # D. Visual display in the terminal
            # If the command is positive, display “+” to the right
            # If it is negative, display “-” to the left
            barre = ""
            if commande > 0:
                barre = "+" * min(int(commande / 10), 20)
            elif commande < 0:
                barre = "-" * min(int(abs(commande) / 10), 20)
            
            print(f"Data: {ax:6.1f}, {ay:6.1f}, {az:6.1f} | Angle: {theta:6.1f}° | Erreur: {-theta:6.1f}° | Commande: {commande:8.1f} [{barre:<20}]", end='\r')
            
            time.sleep(0.05) # 20 Hz (20 times per second)

    except KeyboardInterrupt:
        print("\n\n[ARRÊT] Fin du test PID.")

if __name__ == "__main__":
    test_pid()