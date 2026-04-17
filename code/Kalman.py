class KalmanFilter1D:
    def __init__(self, q_angle=0.001, q_bias=0.003, r_measure=0.03):
        """
        Q_angle: Process noise of the angle (confidence in the gyro model)
        Q_bias: Process noise of the gyro bias
        R_measure: Measurement noise of the accelerometer (increase if there is too much engine vibration)
        """
        self.Q_angle = q_angle
        self.Q_bias = q_bias
        self.R_measure = r_measure

        self.angle = 0.0 # Angle estimé
        self.bias = 0.0  # Biais estimé du gyroscope

        # Matrice de covariance d'erreur P (2x2)
        self.P00 = 0.0
        self.P01 = 0.0
        self.P10 = 0.0
        self.P11 = 0.0

    def get_angle(self, new_angle, new_rate, dt) -> float:
        # 1. Prediction phase (Dynamic update via the gyroscope)
        rate = new_rate - self.bias
        self.angle += dt * rate

        # Updating the error covariance matrix
        self.P00 += dt * (dt * self.P11 - self.P01 - self.P10 + self.Q_angle)
        self.P01 -= dt * self.P11
        self.P10 -= dt * self.P11
        self.P11 += self.Q_bias * dt

        # 2. Update phase (Correction using the accelerometer)
        y = new_angle - self.angle    # Discrepancy between the measurement and the estimate
        S = self.P00 + self.R_measure # Error estimation

        # Kalman gain
        K0 = self.P00 / S
        K1 = self.P10 / S

        # Angle and Skew Correction
        self.angle += K0 * y
        self.bias += K1 * y

        # Updating the covariance matrix
        P00_temp = self.P00
        P01_temp = self.P01

        self.P00 -= K0 * P00_temp
        self.P01 -= K0 * P01_temp
        self.P10 -= K1 * P00_temp
        self.P11 -= K1 * P01_temp

        return self.angle