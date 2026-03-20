import time
import math
import config as cfg
from logger import DataLogger

THRESHOLD = 2007  # Ligne > 2007 = Ligne Noire,
                  # <= 2007 = Blanc
                  
# Importation robuste des drivers
try:
    from drivers.lsm6dsox import LSM6DSOX
    from drivers.mcp3208 import MCP3208
    from drivers.tmc2225 import TMC2225
    # from line_dectector import LineDetector
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
            self.detector = LineDetector(adc_instance=self.adc, threshold=1.5)
            print("[OK] ADC MCP3208")
            print("Line detector OK")
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
        # if self.motor_l and self.motor_r:
        #     self.motor_l.move_async(5000, 400)
        #     self.motor_r.move_async(-5000, 400)
            
        #     Démarrage des threads des moteurs
        # if self.motor_l: self.motor_l.start()
        # if self.motor_r: self.motor_r.start()
        
        print("--- Démarrage Robot (Ctrl+C pour stopper) ---")

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
                        # On demande au capteur où est la ligne
                        tensions_str, position = self.detector.read_status()

                        # # Affichage dynamique sur la console
                        # print(f"{tensions_str} --> {position}      ", end='\r')
                except: pass

                # --- B. Logique de Sécurité et Suivi de ligne ---
                # --- B. Logique de Sécurité et Suivi de ligne ---
                mot_state = "INIT"
                valeurs_brutes = [0] * 8 # Liste vide par défaut pour les 8 capteurs

                if not valid_imu:
                    if self.motor_l: self.motor_l.stop()
                    if self.motor_r: self.motor_r.stop()
                    mot_state = "STOP (SECURITE IMU)"
                
                # ---------------------------------------------------------
                # --- NOUVEAU CERVEAU : LECTURE DIRECTE ADC & STRATÉGIES ---
                # ---------------------------------------------------------
                if self.adc:
                    # 1. Lecture de tous les capteurs en compréhension de liste
                    valeurs_brutes = [self.adc.read_raw(i) for i in range(8)]
                    
                    # 2. Exclusion des capteurs défectueux (2 et 6)
                    # On garde les indices : 0, 1, 3, 4, 5, 7
                    valeurs_valides = [valeurs_brutes[i] for i in range(8) if i not in [2, 6]]
                    
                    # 3. Stratégie 1 : LIGNE LARGE (Moyenne des capteurs valides)
                    moyenne_large = sum(valeurs_valides) / len(valeurs_valides)
                    
                    # Stratégie 2 : LIGNE PETITE (Moyenne des 3 capteurs du milieu valides: 3, 4, 5)
                    valeurs_milieu = [valeurs_brutes[i] for i in [3, 4, 5]]
                    moyenne_petite = sum(valeurs_milieu) / len(valeurs_milieu)
                    
                    # 4. Choix du seuil et de la valeur à analyser
                    THRESHOLD = 2007
                    
                    # !!! ICI VOUS CHOISISSEZ LA STRATÉGIE !!!
                    # Remplacez "moyenne_large" par "moyenne_petite" selon la piste testée
                    valeur_analysee = moyenne_large 
                    
                    # 5. Logique de décision de mouvement
                    if valeur_analysee > THRESHOLD:
                        # Il détecte du NOIR -> Il roule
                        if self.motor_l: self.motor_l.move_async(5000, 400)
                        if self.motor_r: self.motor_r.move_async(-5000, 400) # En miroir
                        mot_state = "RUN  (NOIR) "
                    else:
                        # Il détecte du BLANC -> Il s'arrête
                        if self.motor_l: self.motor_l.stop()
                        if self.motor_r: self.motor_r.stop()
                        mot_state = "STOP (BLANC)"

                    # Affichage clair dans le terminal pour déboguer
                    print(f"Moyenne lue: {valeur_analysee:4.0f}/4095 | Seuil: {THRESHOLD} -> {mot_state}      ", end='\r')

                # ---------------------------------------------------------


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