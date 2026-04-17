import time
import math
import config as cfg
from logger import DataLogger

THRESHOLD = 2007  # Line > 2007 = Black Line,
                  # <= 2007 = White

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
        """Initializing physical components"""
        # IMU
        try:
            self.imu = LSM6DSOX(bus_id=cfg.I2C_BUS_ID, address=cfg.LSM_ADDR)
            print("[OK] IMU LSM6DSOX")
        except Exception as e:
            print(f"[ATTENTION] IMU non détecté: {e}")

        # ADC
        try:
            self.adc = MCP3208(bus=cfg.SPI_BUS_ID, device=cfg.SPI_DEVICE_ID, vref=cfg.ADC_VREF)
            self.detector = LineDetector(adc_instance=self.adc, threshold=1.5)
            print("[OK] ADC MCP3208")
            print("Line detector OK")
        except: print("[INFO] Pas d'ADC")

        # Motors
        try:
            self.motor_l = TMC2225(**cfg.MOTOR_LEFT_PINS, name="Gauche")
            self.motor_r = TMC2225(**cfg.MOTOR_RIGHT_PINS, name="Droit")
            print("[OK] Moteurs")
        except: print("[ERREUR] Problème Moteurs")

    def _recover_imu(self):
        """Attempting to reconnect the sensor"""
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
        """Entry point of the main loop"""
        print("\n--- Démarrage Robot (Ctrl+C pour stopper) ---")
        
        # Engine Test (Slow Rotation)
        # if self.motor_l and self.motor_r:
        #     self.motor_l.move_async(5000, 400)
        #     self.motor_r.move_async(-5000, 400)
            
        # Starting the engine threads
        # if self.motor_l: self.motor_l.start()
        # if self.motor_r: self.motor_r.start()
        
        print("--- Démarrage Robot (Ctrl+C pour stopper) ---")

        err_count = 0

        try:
            while True:
                # --- A. Data Acquisition ---
                ax, ay, az = 0.0, 0.0, 0.0
                mag = 0.0
                volts = 0.0
                status = "INIT"
                valid_imu = False

                # 1. IMU Course  + Sanity Check
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
                    
                    # Reconnection logic after 2 failed attempts
                    if err_count > 2:
                        status = "RECONNEXION..."
                        if self._recover_imu():
                            err_count = 0

                # 2. ADC Reading
                    if self.adc:
                        # We ask the sensor where the line is
                        tensions_str, position = self.detector.read_status()

                        # Digital signage on the console
                        # print(f"{tensions_str} --> {position}      ", end='\r')
                except: pass

                # --- B. Safety Logic and Line Monitoring ---
                mot_state = "INIT"
                valeurs_brutes = [0] * 8 # Liste vide par défaut pour les 8 capteurs

                if not valid_imu:
                    if self.motor_l: self.motor_l.stop()
                    if self.motor_r: self.motor_r.stop()
                    mot_state = "STOP (SECURITE IMU)"
                
                if self.adc:
                    # 1. Reading from the 8 sensors
                    valeurs_brutes = [self.adc.read_raw(i) for i in range(8)]
                    
                    THRESHOLD = 2007
                    
                    # Reading from the 8 sensors:
                    # active_sensors = range(8) 
                    
                    # (If the robot refuses to stop because the faulty sensors are reading 4000, 
                    # comment out the line above and uncomment the one below
                    capteurs_actifs = [0, 1, 3, 4, 5, 7]
                    
                    # 2. The “any” condition checks whether at least ONE sensor exceeds 2007
                    voit_le_noir = any(valeurs_brutes[i] > THRESHOLD for i in capteurs_actifs)
                    
                    # 3. Action !
                    if voit_le_noir:
                        # At least one sensor detects the line -> Let's move forward!
                        if self.motor_l: self.motor_l.move_async(5000, 400)
                        if self.motor_r: self.motor_r.move_async(5000, 400) # En miroir
                        mot_state = "RUN  (NOIR) "
                    else:
                        # Absolutely NO sensors detect the line -> We stop
                        if self.motor_l: self.motor_l.stop()
                        if self.motor_r: self.motor_r.stop()
                        mot_state = "STOP (BLANC)"

                    # Digital signage for viewing real-time data
                    affichage_vals = " ".join([f"CH{i}:{valeurs_brutes[i]:4d}" for i in capteurs_actifs])
                    print(f"Yeux [{affichage_vals}] | {mot_state}      ", end='\r')

                # ---------------------------------------------------------


        except KeyboardInterrupt:
            print("\n[USER] Arrêt demandé.")
        finally:
            self.stop()

    def stop(self):
        """Complete shutdown of the entire machine"""
        if self.motor_l: self.motor_l.stop()
        if self.motor_r: self.motor_r.stop()
        if self.adc: self.adc.close()
        self.logger.close()
        print("Machine éteinte.")