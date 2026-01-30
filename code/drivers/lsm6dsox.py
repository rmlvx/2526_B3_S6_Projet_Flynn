from smbus2 import SMBus
import struct

# Registres LSM6DSOX
REG_WHO_AM_I = 0x0F
REG_CTRL1_XL = 0x10 # Accel config
REG_CTRL2_G  = 0x11 # Gyro config
REG_OUTX_L_G = 0x22 # Début des données Gyro (X,Y,Z)
REG_OUTX_L_A = 0x28 # Début des données Accel (X,Y,Z)

class LSM6DSOX:
    def __init__(self, bus_id=1, address=0x6A):
        self.bus = SMBus(bus_id)
        self.address = address
        self._check_id()
        self._configure()

    def _check_id(self):
        chip_id = self.bus.read_byte_data(self.address, REG_WHO_AM_I)
        if chip_id != 0x6C: # ID par défaut du DSOX
            print(f"Warning: ID LSM6DSOX incorrect (lu: {hex(chip_id)})")

    def _configure(self):
        # Configuration ODR (Output Data Rate) et Echelle
        # Accel: 52Hz, 4g (0b00111000 -> 0x38)
        self.bus.write_byte_data(self.address, REG_CTRL1_XL, 0x38)
        # Gyro: 52Hz, 2000dps (0b00111100 -> 0x3C)
        self.bus.write_byte_data(self.address, REG_CTRL2_G, 0x3C)

    def read_all(self):
        """
        Lit l'accélération et le gyroscope en une seule transaction optimisée (ou deux blocs proches).
        Pour simplifier et rester robuste : lecture bloc Gyro (6 bytes) puis Accel (6 bytes).
        """
        # Lecture Gyro (6 octets consécutifs)
        g_data = self.bus.read_i2c_block_data(self.address, REG_OUTX_L_G, 6)
        # Lecture Accel (6 octets consécutifs)
        a_data = self.bus.read_i2c_block_data(self.address, REG_OUTX_L_A, 6)

        # Conversion binaire (little endian short)
        gx, gy, gz = struct.unpack('<3h', bytes(g_data))
        ax, ay, az = struct.unpack('<3h', bytes(a_data))

        # Facteurs d'échelle (dépendent de la config ci-dessus)
        # Gyro 2000dps -> 70 mdps/LSB
        gyro_scale = 0.070
        # Accel 4g -> 0.122 mg/LSB
        accel_scale = 0.122 / 1000.0 * 9.81 # en m/s^2

        return {
            'accel': (ax * accel_scale, ay * accel_scale, az * accel_scale),
            'gyro': (gx * gyro_scale, gy * gyro_scale, gz * gyro_scale)
        }