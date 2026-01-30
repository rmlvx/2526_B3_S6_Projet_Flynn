from gpiozero import OutputDevice
import time
import threading

class TMC2225:
    def __init__(self, step_pin, dir_pin, en_pin, name="Motor"):
        self.name = name
        self._step = OutputDevice(step_pin)
        self._dir = OutputDevice(dir_pin)
        self._en = OutputDevice(en_pin, initial_value=True) # Active Low: True = Disable au démarrage
        self._running = False
        self._thread = None

    def enable(self):
        self._en.off() # Active Low

    def disable(self):
        self._en.on()

    def set_direction(self, clockwise=True):
        if clockwise:
            self._dir.on()
        else:
            self._dir.off()

    def move_steps(self, steps, delay=0.001, accel=False):
        """
        Déplace le moteur de n pas. Bloquant si appelé directement, 
        mais prévu pour être encapsulé si besoin.
        """
        self.enable()
        current_delay = delay * 3 if accel else delay # Départ lent si accélération
        
        for i in range(steps):
            self._step.on()
            time.sleep(1e-6) # Pulse très court (min 100ns pour TMC2225)
            self._step.off()
            
            # Gestion simple de l'accélération (Ramp-up)
            if accel and current_delay > delay:
                current_delay -= (delay * 0.05) # Réduit le délai de 5% par pas
            
            time.sleep(current_delay)
            
        self.disable()

    def move_async(self, steps, delay=0.001):
        """Lance le mouvement dans un thread séparé"""
        if self._thread and self._thread.is_alive():
            print(f"[{self.name}] Moteur déjà en mouvement.")
            return
        
        self._thread = threading.Thread(target=self.move_steps, args=(steps, delay, True))
        self._thread.start()