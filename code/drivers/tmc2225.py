import time
import threading
from gpiozero import DigitalOutputDevice

class TMC2225:
    """
    Pilote pour TMC2225 utilisant gpiozero.
    Gère l'accélération, le threading et le cas où la broche Enable est absente.
    """
    def __init__(self, STEP, DIR, EN=None, name="Motor"):
        self.name = name
        self.step_pin = DigitalOutputDevice(STEP)
        self.dir_pin = DigitalOutputDevice(DIR)
        
        # Gestion optionnelle de la broche Enable
        self.enable_pin = None
        if EN is not None:
            # active_high=False car souvent LOW=Enabled sur les drivers
            self.enable_pin = DigitalOutputDevice(EN, active_high=False, initial_value=False)
        
        self._running = False
        self._thread = None

    def enable(self, state=True):
        """Active ou désactive le courant (si la broche EN est connectée)"""
        if self.enable_pin:
            if state:
                self.enable_pin.on()
            else:
                self.enable_pin.off()

    def move_async(self, steps, speed_hz, acceleration=True):
        """
        Lance un mouvement dans un thread (non-bloquant).
        """
        if self._running:
            return # Ignore si déjà en mouvement

        direction = 1 if steps > 0 else 0
        self.dir_pin.value = direction
        
        self._thread = threading.Thread(
            target=self._step_loop, 
            args=(abs(steps), speed_hz, acceleration)
        )
        self._thread.start()

    def _step_loop(self, steps, target_speed, acceleration):
        """Boucle de génération des impulsions."""
        self._running = True
        self.enable(True)
        
        delay = 1.0 / target_speed
        
        for i in range(steps):
            if not self._running: break
            
            # Pulse
            self.step_pin.on()
            time.sleep(delay * 0.5)
            self.step_pin.off()
            time.sleep(delay * 0.5)

        self._running = False
        # On ne désactive pas le moteur ici pour garder le couple (Hold Torque)

    def stop(self):
        """Arrêt d'urgence"""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join()