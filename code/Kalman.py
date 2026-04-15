class KalmanFilter1D:
    def __init__(self, q_angle=0.001, q_bias=0.003, r_measure=0.03):
        """
        Q_angle: Bruit de processus de l'angle (confiance dans le modèle gyro)
        Q_bias: Bruit de processus du biais du gyro
        R_measure: Bruit de mesure de l'accéléromètre (augmenter si trop de vibrations moteurs)
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

    def get_angle(self, new_angle, new_rate, dt):
        # 1. Étape de prédiction (Update dynamique via le gyroscope)
        rate = new_rate - self.bias
        self.angle += dt * rate

        # Mise à jour de la matrice de covariance d'erreur
        self.P00 += dt * (dt * self.P11 - self.P01 - self.P10 + self.Q_angle)
        self.P01 -= dt * self.P11
        self.P10 -= dt * self.P11
        self.P11 += self.Q_bias * dt

        # 2. Étape de mise à jour (Correction via l'accéléromètre)
        y = new_angle - self.angle # Erreur entre la mesure et l'estimation
        S = self.P00 + self.R_measure # Estimation de l'erreur

        # Gain de Kalman
        K0 = self.P00 / S
        K1 = self.P10 / S

        # Correction de l'angle et du biais
        self.angle += K0 * y
        self.bias += K1 * y

        # Mise à jour de la matrice de covariance
        P00_temp = self.P00
        P01_temp = self.P01

        self.P00 -= K0 * P00_temp
        self.P01 -= K0 * P01_temp
        self.P10 -= K1 * P00_temp
        self.P11 -= K1 * P01_temp

        return self.angle