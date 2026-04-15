import time
import threading
from gpiozero import DigitalOutputDevice

class TMC2225:
    def __init__(self, STEP, DIR, EN=None, name="Motor"):
        self.name = name
        self.step_pin = DigitalOutputDevice(STEP)
        self.dir_pin = DigitalOutputDevice(DIR)
        
        self.enable_pin = None
        if EN is not None:
            self.enable_pin = DigitalOutputDevice(EN, active_high=False, initial_value=False)
        
        # Variables pour le contrôle de vitesse en continu
        self._running = False
        self._target_speed_hz = 0.0
        self._thread = None
        
        self.enable(True)

    def enable(self, state=True):
        if self.enable_pin:
            if state:
                self.enable_pin.on()
            else:
                self.enable_pin.off()

    def set_speed(self, speed_hz):
        """Met à jour la vitesse (Hz) et la direction instantanément."""
        self._target_speed_hz = speed_hz
        
        # Changement de direction
        if speed_hz > 0:
            self.dir_pin.on()
        elif speed_hz < 0:
            self.dir_pin.off()

    def start(self):
        """Lance le thread de rotation infinie."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()

    def _run_loop(self):
        """Boucle qui tourne en tâche de fond à la vitesse demandée."""
        while self._running:
            speed = abs(self._target_speed_hz)
            
            # En dessous de 10 Hz, on considère que le moteur est à l'arrêt
            if speed < 10:
                time.sleep(0.01)
                continue
                
            # Calcul du délai pour la vitesse actuelle
            delay = 1.0 / speed
            half_delay = delay / 2.0
            
            self.step_pin.on()
            time.sleep(half_delay)
            self.step_pin.off()
            time.sleep(half_delay)

    def stop(self):
        """Arrête proprement le moteur."""
        self._running = False
        self._target_speed_hz = 0.0
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)