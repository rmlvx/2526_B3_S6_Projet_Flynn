class PIDController:
    """
    Régulateur PID pour le maintien en équilibre.

    Différence clé par rapport à la version précédente :
    - dt est passé en argument de compute() et non recalculé en interne.
      Cela garantit que le PID et le filtre de Kalman utilisent exactement
      le même dt, évitant les dérives asymétriques liées aux délais variables.
    """

    def __init__(self, kp=0.0, ki=0.0, kd=0.0, target_angle=0.0):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

        self.target = target_angle

        self.prev_error = 0.0
        self.integral   = 0.0

        # Anti-windup : limite absolue de l'intégrale
        self.max_integral = 1000.0

    def compute(self, current_angle, dt):
        """
        Calcule la commande moteur.

        Paramètres
        ----------
        current_angle : float — angle mesuré (degrés)
        dt            : float — durée du cycle en secondes (fourni par la boucle principale)

        Retourne
        --------
        float — vitesse signée en pas/seconde à envoyer aux moteurs
        """
        if dt <= 0.0:
            dt = 0.001

        # 1. Erreur
        error = self.target - current_angle

        # 2. Terme Proportionnel
        P = self.Kp * error

        # 3. Terme Intégral avec anti-windup
        self.integral += error * dt
        self.integral  = max(-self.max_integral, min(self.integral, self.max_integral))
        I = self.Ki * self.integral

        # 4. Terme Dérivé
        derivative = (error - self.prev_error) / dt
        D = self.Kd * derivative

        self.prev_error = error

        return P + I + D

    def reset(self):
        """Réinitialise la mémoire du PID (ex : après une chute)."""
        self.prev_error = 0.0
        self.integral   = 0.0

    def set_tunings(self, kp, ki, kd):
        """Modifie les coefficients à la volée."""
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd