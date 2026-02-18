from smbus2 import SMBus
import struct
import time

class LSM6DSOX:
    # Registres (Datasheet ST)
    WHO_AM_I = 0x0F
    CTRL1_XL = 0x10  # Config Accel
    CTRL2_G  = 0x11  # Config Gyro
    CTRL3_C  = 0x12  # Control Register 3 (Reset)
    OUTX_L_G = 0x22  # Début données Gyro
    OUTX_L_A = 0x28  # Début données Accel

    def __init__(self, bus_id=1, address=0x6A):
        self.bus_id = bus_id
        self.address = address
        self.bus = None
        self.connect()

    def connect(self):
        """Tente d'ouvrir le bus et de configurer le capteur"""
        try:
            if self.bus:
                self.bus.close()
        except:
            pass
            
        self.bus = SMBus(self.bus_id)
        
        # 1. Vérification ID
        try:
            who_am_i = self.bus.read_byte_data(self.address, self.WHO_AM_I)
            if who_am_i != 0x6C:
                raise RuntimeError(f"ID Inconnu: {hex(who_am_i)}")
        except OSError:
            raise RuntimeError("Capteur non détecté sur le bus I2C")

        # 2. Reset Logiciel (Pour nettoyer les erreurs précédentes)
        # Bit 0 = SW_RESET, Bit 2 = IF_INC (Auto-increment, vital pour la lecture par bloc)
        self.bus.write_byte_data(self.address, self.CTRL3_C, 0x05) 
        time.sleep(0.1) # Attendre le redémarrage du capteur

        # 3. Configuration
        # Accel: 52Hz, +/- 4g (0x38) - Plus robuste aux vibrations que 2g
        self.bus.write_byte_data(self.address, self.CTRL1_XL, 0x38)
        # Gyro: 52Hz, 250 dps (0x30)
        self.bus.write_byte_data(self.address, self.CTRL2_G, 0x30)

    def read_all(self):
        """Retourne un dictionnaire avec accel et gyro"""
        # Lit 12 octets d'un coup (6 Gyro + 6 Accel) car les registres se suivent
        # Note: OUTX_L_G (0x22) est avant OUTX_L_A (0x28) dans la mémoire
        # Mais il y a un trou entre les deux, donc on lit en deux blocs pour être sûr.
        
        # Lecture Gyro
        g_data = self.bus.read_i2c_block_data(self.address, self.OUTX_L_G, 6)
        gx, gy, gz = struct.unpack('<hhh', bytes(g_data))
        
        # Lecture Accel
        a_data = self.bus.read_i2c_block_data(self.address, self.OUTX_L_A, 6)
        ax, ay, az = struct.unpack('<hhh', bytes(a_data))

        # Facteurs de conversion
        # Accel 4g = 0.122 mg/LSB
        a_factor = 0.122 / 1000.0
        # Gyro 250dps = 8.75 mdps/LSB
        g_factor = 8.75 / 1000.0

        return {
            'accel': (ax * a_factor, ay * a_factor, az * a_factor),
            'gyro':  (gx * g_factor, gy * g_factor, gz * g_factor)
        }