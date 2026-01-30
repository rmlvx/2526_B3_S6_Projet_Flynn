import time
import config
from drivers.tmc2225 import TMC2225
from drivers.mcp3208 import MCP3208
from drivers.lsm6dsox import LSM6DSOX

class MachineController:
    def __init__(self):
        print("Initialisation des sous-systèmes...")
        
        # Init Moteurs
        self.motor1 = TMC2225(config.MOTOR1_STEP_PIN, config.MOTOR1_DIR_PIN, config.MOTOR1_EN_PIN, "Axe X")
        self.motor2 = TMC2225(config.MOTOR2_STEP_PIN, config.MOTOR2_DIR_PIN, config.MOTOR2_EN_PIN, "Axe Y")
        
        # Init Capteurs
        try:
            self.imu = LSM6DSOX(config.IMU_I2C_BUS, config.IMU_ADDRESS)
            print("IMU initialisé.")
        except Exception as e:
            print(f"Erreur IMU: {e}")
            self.imu = None

        try:
            self.adc = MCP3208(config.ADC_SPI_BUS, config.ADC_SPI_DEVICE, config.VREF_ADC)
            print("ADC initialisé.")
        except Exception as e:
            print(f"Erreur ADC: {e}")
            self.adc = None

    def run_demo(self):
        print("Démarrage de la démo...")
        
        # Lancer un mouvement moteur en arrière-plan (Non-bloquant)
        self.motor1.move_async(steps=2000, delay=0.002) # Rotation lente
        
        # Boucle principale de lecture capteurs
        start_time = time.time()
        while time.time() - start_time < 10: # Tourne pendant 10 secondes
            
            # Lecture IMU
            if self.imu:
                data = self.imu.read_all()
                ax, ay, az = data['accel']
                print(f"IMU Accel: X={ax:.2f} Y={ay:.2f} Z={az:.2f}")

            # Lecture ADC (ex: capteur distance sur ch 0)
            if self.adc:
                volts = self.adc.read_voltage(0)
                print(f"ADC CH0: {volts:.2f}V")

            time.sleep(0.1) # 10Hz de lecture

        print("Fin de la démo.")
        self.close()

    def close(self):
        if self.adc: self.adc.close()
        # gpiozero gère le cleanup automatiquement à la fermeture du script

if __name__ == "__main__":
    machine = MachineController()
    try:
        machine.run_demo()
    except KeyboardInterrupt:
        print("Arrêt d'urgence")
        machine.close()