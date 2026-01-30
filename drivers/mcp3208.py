import spidev

class MCP3208:
    def __init__(self, bus=0, device=0, vref=3.3):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1350000 # 1.35 MHz (sûr pour Pi Zero)
        self.vref = vref

    def read_raw(self, channel):
        """
        Lit la valeur brute (0-4095) du canal (0-7).
        Protocole MCP3208: Start Bit + SGL/DIFF + D2+D1+D0
        """
        if not 0 <= channel <= 7:
            raise ValueError("Le canal doit être entre 0 et 7")
        
        # Construction de la commande : 
        # Byte 0: 00000001 (Start bit)
        # Byte 1: (SGL/DIFF=1)(D2)(D1)(D0)xxxx -> SGL=1 pour Single Ended
        cmd = 4 | 2 | ((channel & 4) >> 2)
        cmd_byte1 = (cmd << 6) | ((channel & 3) << 4)
        
        # Envoi de 3 octets : [Start, Config, Dummy]
        adc = self.spi.xfer2([1, cmd_byte1, 0])
        
        # Reconstruction du résultat 12 bits
        # adc[1] contient les bits de poids fort (masqués avec 0x0F)
        # adc[2] contient les bits de poids faible
        data = ((adc[1] & 0x0F) << 8) | adc[2]
        return data

    def read_voltage(self, channel):
        raw = self.read_raw(channel)
        return (raw * self.vref) / 4095.0

    def close(self):
        self.spi.close()