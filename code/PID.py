import time

class PIDController:
    """
    Régulateur PID (Proportionnel, Intégral, Dérivé) pour le maintien en équilibre.
    """
    def __init__(self, kp=0.0, ki=0.0, kd=0.0, target_angle=0.0):
        # Constantes (Coefficients) modifiables par l'utilisateur
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        
        # Cible à atteindre (0 degrés = parfaitement vertical)
        self.target = target_angle
        
        # Variables de mémoire pour les calculs I et D
        self.prev_error = 0.0
        self.integral = 0.0
        self.prev_time = time.time()
        
        # Limite de sécurité pour éviter que l'intégrale n'explose (Windup)
        self.max_integral = 1000.0 

    def compute(self, current_angle):
        """
        Calcule la vitesse à envoyer aux moteurs en fonction de l'angle actuel.
        """
        current_time = time.time()
        dt = current_time - self.prev_time
        
        # Sécurité : éviter la division par zéro si la boucle est trop rapide
        if dt <= 0.0:
            dt = 0.001
            
        # 1. Calcul de l'erreur (Distance entre la réalité et la cible)
        error = self.target - current_angle
        
        # 2. Terme Proportionnel (P) : Réagit à l'erreur instantanée
        P = self.Kp * error
        
        # 3. Terme Intégral (I) : Corrige les petites erreurs accumulées dans le temps
        self.integral += error * dt
        # Anti-windup : on bride l'intégrale pour ne pas saturer les moteurs
        self.integral = max(-self.max_integral, min(self.integral, self.max_integral))
        I = self.Ki * self.integral
        
        # 4. Terme Dérivé (D) : Anticipe le mouvement et freine pour éviter d'osciller
        derivative = (error - self.prev_error) / dt
        D = self.Kd * derivative
        
        # Sauvegarde pour le prochain cycle
        self.prev_error = error
        self.prev_time = current_time
        
        # La commande finale est la somme des trois actions
        output = P + I + D
        return output

    def reset(self):
        """Réinitialise la mémoire du PID (utile si le robot tombe et qu'on le relève)"""
        self.prev_error = 0.0
        self.integral = 0.0
        self.prev_time = time.time()

    def set_tunings(self, kp, ki, kd):
        """Permet de modifier les coefficients à la volée"""
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd