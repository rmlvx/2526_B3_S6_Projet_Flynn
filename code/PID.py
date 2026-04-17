class PIDController:
    """
    PID controller for maintaining equilibrium.

    Key difference from the previous version:
    - dt is passed as an argument to compute() and is not recalculated internally.
      This ensures that the PID and the Kalman filter use exactly
      the same dt, avoiding asymmetric drifts caused by variable delays.
    """

    def __init__(self, kp=0.0, ki=0.0, kd=0.0, target_angle=0.0):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

        self.target = target_angle

        self.prev_error = 0.0
        self.integral   = 0.0

        # Anti-windup : upper limit of the integral
        self.max_integral = 1000.0

    def compute(self, current_angle, dt) -> float:
        """
        Calculates the motor control.

        Args:
            current_angle : float — measured angle (degrees)
            dt            : float — cycle duration in seconds (provided by the main loop)

        Returns:
            float — vitesse signée en pas/seconde à envoyer aux moteurs
        """
        if dt <= 0.0:
            dt = 0.001

        # 1. Error
        error = self.target - current_angle

        # 2. Proportional Term
        P = self.Kp * error

        # 3. Full-range term with anti-windup
        self.integral += error * dt
        self.integral  = max(-self.max_integral, min(self.integral, self.max_integral))
        I = self.Ki * self.integral

        # 4. Derived Term
        derivative = (error - self.prev_error) / dt
        D = self.Kd * derivative

        self.prev_error = error

        return P + I + D

    def reset(self):
        """Resets the PID memory (e.g., after a crash)."""
        self.prev_error = 0.0
        self.integral   = 0.0

    def set_tunings(self, kp, ki, kd):
        """Changes the coefficients on the fly."""
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd