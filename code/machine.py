import time
import math
import config as cfg
from logger import DataLogger

# Importation robuste des drivers
try:
    from drivers.lsm6dsox import LSM6DSOX
    from drivers.mcp3208 import MCP3208
    from drivers.tmc2225 import TMC2225
except ImportError as e:
    print(f"CRITIQUE : Pilote manquant ({e})")
    exit(1)

class MachineController:
    def __init__(self):
        print("\n--- Initialisation Machine ---")
        
        # 1. Logger
        self.logger = DataLogger()

        # 2. Hardware
        self.imu = None
        self.adc = None
        self.motor_l = None
        self.motor_r = None
        
        self._init_hardware()

    def _init_hardware(self):
        """Initialisation des composants physiques"""
        # IMU
        try:
            self.imu = LSM6DSOX(bus_id=cfg.I2C_BUS_ID, address=cfg.LSM_ADDR)
            print("[OK] IMU LSM6DSOX")
        except Exception as e:
            print(f"[ATTENTION] IMU non détecté: {e}")

        # ADC
        try:
            self.adc = MCP3208(bus=cfg.SPI_BUS_ID, device=cfg.SPI_DEVICE_ID, vref=cfg.ADC_VREF)
            print("[OK] ADC MCP3208")
        except: print("[INFO] Pas d'ADC")

        # Moteurs
        try:
            self.motor_l = TMC2225(**cfg.MOTOR_LEFT_PINS, name="Gauche")
            self.motor_r = TMC2225(**cfg.MOTOR_RIGHT_PINS, name="Droit")
            print("[OK] Moteurs")
        except: print("[ERREUR] Problème Moteurs")

    def _recover_imu(self):
        """Tentative de reconnexion du capteur"""
        if self.imu is None:
            try:
                self.imu = LSM6DSOX(bus_id=cfg.I2C_BUS_ID, address=cfg.LSM_ADDR)
                return True
            except: return False
        else:
            try:
                self.imu.connect()
                return True
            except: return False

    def start(self):
        """Point d'entrée de la boucle principale"""
        print("\n--- Démarrage Robot (Ctrl+C pour stopper) ---")
        
        # Test Moteurs (Rotation lente)
        if self.motor_l and self.motor_r:
            self.motor_l.move_async(5000, 400)
            self.motor_r.move_async(-5000, 400)

        err_count = 0

        try:
            while True:
                # --- A. Acquisition Données ---
                ax, ay, az = 0.0, 0.0, 0.0
                mag = 0.0
                volts = 0.0
                status = "INIT"
                valid_imu = False

                # 1. Lecture IMU + Sanity Check
                try:
                    if self.imu:
                        data = self.imu.read_all()
                        ax, ay, az = data['accel']
                        
                        # Calcul vecteur gravité
                        mag = math.sqrt(ax**2 + ay**2 + az**2)
                        
                        # Si gravité < 0.1g, c'est physiquement impossible -> erreur
                        if mag < 0.1: raise ValueError("Zero-G Error")
                        
                        valid_imu = True
                        err_count = 0
                        status = "OK"
                    else:
                        raise OSError("No Device")

                except (OSError, ValueError, RuntimeError) as e:
                    err_count += 1
                    status = f"ERR: {e}"
                    
                    # Logique de reconnexion après 2 échecs
                    if err_count > 2:
                        status = "RECONNEXION..."
                        if self._recover_imu():
                            err_count = 0

                # 2. Lecture ADC
                if self.adc:
                    try: _, volts = self.adc.read(0)
                    except: pass

                # --- B. Logique de Sécurité (Failsafe) ---
                if not valid_imu:
                    # Si on ne sait pas où on est, on coupe les moteurs !
                    if self.motor_l: self.motor_l.stop()
                    if self.motor_r: self.motor_r.stop()
                    mot_state = "STOP (SECURITE)"
                else:
                    # Ici viendra votre code d'asservissement (PID)
                    # Pour l'instant, on laisse tourner
                    mot_state = "RUN"

                # --- C. Feedback (Console + Log) ---
                # Affichage formaté pour lecture facile
                print(f"IMU: {mag:.2f}g [X:{ax:.1f} Y:{ay:.1f} Z:{az:.1f}] | ADC: {volts:.1f}V | {status} | {mot_state}      ", end='\r')
                
                self.logger.log(ax, ay, az, mag, volts, status)
                
                time.sleep(0.05) # Boucle à 20Hz

        except KeyboardInterrupt:
            print("\n[USER] Arrêt demandé.")
        finally:
            self.stop()

    def stop(self):
        """Arrêt propre de toute la machine"""
        if self.motor_l: self.motor_l.stop()
        if self.motor_r: self.motor_r.stop()
        if self.adc: self.adc.close()
        self.logger.close()
        print("Machine éteinte.")