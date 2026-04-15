import time
import threading
from gpiozero import DigitalOutputDevice

class TMC2225:
    """
    Pilote pour TMC2225 utilisant gpiozero.
    Gère le threading continu et l'inversion optionnelle de sens.
    """
    def __init__(self, STEP, DIR, EN=None, name="Motor", invert=False):
        self.name = name
        # invert=True retourne le sens logique du moteur sans toucher au câblage
        self.invert = invert

        self.step_pin = DigitalOutputDevice(STEP)
        self.dir_pin  = DigitalOutputDevice(DIR)

        self.enable_pin = None
        if EN is not None:
            self.enable_pin = DigitalOutputDevice(EN, active_high=False, initial_value=False)

        self._running      = False
        self._thread       = None
        self._target_speed = 0.0      # Hz signé
        self._speed_lock   = threading.Lock()

    def enable(self, state=True):
        if self.enable_pin:
            if state: self.enable_pin.on()
            else:     self.enable_pin.off()

    def set_speed(self, speed_hz_signed):
        if self.invert:
            speed_hz_signed = -speed_hz_signed
        with self._speed_lock:
            self._target_speed = speed_hz_signed
        if not self._running:
            self._start_continuous_thread()

    def _start_continuous_thread(self):
        self._running = True
        self.enable(True)
        self._thread = threading.Thread(target=self._continuous_loop, daemon=True)
        self._thread.start()
        
    # def _continuous_loop(self):
    #     current_dir = None  # On mémorise la direction appliquée

    #     while self._running:
    #         with self._speed_lock:
    #             speed = self._target_speed

    #         if abs(speed) < 1.0:
    #             time.sleep(0.001)
    #             continue

    #         new_dir = 1 if speed > 0 else 0

    #         # On met à jour la direction UNIQUEMENT entre deux pas, jamais pendant
    #         if new_dir != current_dir:
    #             self.dir_pin.value = new_dir
    #             current_dir = new_dir
    #             time.sleep(0.0001)  # Délai de setup DIR requis par TMC2225 (≥ 20 ns, on prend large)

    #         delay = 1.0 / abs(speed)
    #         self.step_pin.on()
    #         time.sleep(delay * 0.5)
    #         self.step_pin.off()
    #         time.sleep(delay * 0.5)

    #     self._running = False
        
    # def _continuous_loop(self):
    #     current_dir = None

    #     while self._running:
    #         with self._speed_lock:
    #             speed = self._target_speed

    #         if abs(speed) < 1.0:
    #             time.sleep(0.001)
    #             continue

    #         # ← invert retourne le sens physique sans toucher à la logique PID
    #         effective_speed = -speed if self.invert else speed
    #         new_dir = 1 if effective_speed > 0 else 0

    #         if new_dir != current_dir:
    #             self.dir_pin.value = new_dir
    #             current_dir = new_dir
    #             time.sleep(0.0001)  # setup time DIR → TMC2225

    #         delay = 1.0 / abs(speed)
    #         self.step_pin.on()
    #         time.sleep(delay * 0.5)
    #         self.step_pin.off()
    #         time.sleep(delay * 0.5)

    #     self._running = False
    
    def _continuous_loop(self):
        current_dir = None

        while self._running:
            with self._speed_lock:
                speed = self._target_speed

            if abs(speed) < 1.0:
                time.sleep(0.001)
                continue

            effective_speed = -speed if self.invert else speed
            new_dir = 1 if effective_speed > 0 else 0

            if new_dir != current_dir:
                self.dir_pin.value = new_dir
                current_dir = new_dir
                # ← DEBUG : affiche ce qui est réellement envoyé à la broche
                print(f"[{self.name}] invert={self.invert} | speed={speed:+.0f} | DIR={new_dir}")
                time.sleep(0.0001)

            delay = 1.0 / abs(speed)
            self.step_pin.on()
            time.sleep(delay * 0.5)
            self.step_pin.off()
            time.sleep(delay * 0.5)

        self._running = False

    def move_async(self, steps, speed_hz, acceleration=True):
        signed_speed = speed_hz if steps > 0 else -speed_hz
        self.set_speed(signed_speed)

    def stop(self):
        with self._speed_lock:
            self._target_speed = 0.0
        self._running = False