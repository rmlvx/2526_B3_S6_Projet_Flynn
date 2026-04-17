import time
import math
import config as cfg
from drivers.lsm6dsox import LSM6DSOX
from drivers.tmc2225 import TMC2225
from PID import PIDController
from Kalman import KalmanFilter1D

# Maximum speed sent to the motors (Hz).
# Increase this value if the robot isn't responding quickly enough; decrease it if the motors stall.
MAX_SPEED_HZ = 800.0

# Angle beyond which the robot is considered to have fallen (safety)
FALL_ANGLE = 45.0


def test_balance():
    print("--- TEST D'ÉQUILIBRE (KALMAN + PID) ---")

    try:
        imu = LSM6DSOX(bus_id=cfg.I2C_BUS_ID, address=cfg.LSM_ADDR)
        motor_l = TMC2225(**cfg.MOTOR_LEFT_PINS,  name="Gauche")
        motor_r = TMC2225(**cfg.MOTOR_RIGHT_PINS, name="Droit")

        motor_l.enable()
        motor_r.enable()

        pid    = PIDController(kp=15, ki=0, kd=0, target_angle=0.0)
        kalman = KalmanFilter1D()

        print("[OK] Système prêt. Démarrage de la boucle de contrôle…")

        prev_time = time.perf_counter()

        while True:
            # ── 1. IMU reading ──────────────────────────────────────────────
            data = imu.read_all()
            ax, ay, az = data['accel']
            gx, gy, gz = data['gyro']

            # ── 2. Calculation of dt ─────────────────────────────────────────────
            now = time.perf_counter()
            dt  = now - prev_time
            prev_time = now

            # Safety check: if dt is invalid, skip this loop
            if dt <= 0.0 or dt > 0.5:
                time.sleep(0.01)
                continue

            # ── 3. Kalman Angle ─────────────────────────────────────────────
            # atan2(az, -ay) returns the forward/reverse pitch angle;
            # gx must be the corresponding angular velocity (in °/s)
            accel_angle = math.degrees(math.atan2(az, -ay))
            theta = kalman.get_angle(accel_angle, gx, dt)

            # ── 4. Fall Protection ──────────────────────────────────────
            if abs(theta) > FALL_ANGLE:
                motor_l.set_speed(0)
                motor_r.set_speed(0)
                print(f"\n[CHUTE DÉTECTÉE] Angle = {theta:.1f}° — moteurs coupés.")
                time.sleep(1.0)
                pid.reset()
                prev_time = time.perf_counter()
                continue

            # ── 5. PID ─────────────────────────────────────────────────────
            # Switch the PID controller to use the same time constant as the Kalman filter
            commande = pid.compute(theta, dt)

            # ── 6. Speed saturation ─────────────────────────────────
            commande = max(-MAX_SPEED_HZ, min(commande, MAX_SPEED_HZ))

            # ── 7. Directly pass the signed speed (set_speed is thread-safe)
            motor_l.set_speed( commande)
            motor_r.set_speed(-commande)   # moteur droit monté en miroir

            # ── 8. Display ────────────────────────────────────────────────
            print(
                f"dt:{dt*1000:5.1f}ms | "
                f"Angle:{theta:6.2f}° | "
                f"Cmd:{commande:+8.1f} Hz   ",
                end='\r'
            )

            time.sleep(0.01)   # ~100 Hz

    except KeyboardInterrupt:
        print("\n[ARRÊT] CTRL +")
        motor_l.stop()
        motor_r.stop()


if __name__ == "__main__":
    test_balance()