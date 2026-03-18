import spidev

class MCP3208:
    def __init__(self, bus=0, device=0, vref=5):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000 # 1 MHz
        self.vref = vref

    def read_raw(self, channel):
        if not 0 <= channel <= 7:
            raise ValueError("Le canal doit être entre 0 et 7")
        
        # C'est LA ligne magique du projet qui marche : 
        # Start bit + bit Single Ended + numéro du canal
        command = [4 | 2 | (channel >> 2), (channel & 3) << 6, 0]
        result = self.spi.xfer2(command)
        
        # Reconstruction des 12 bits
        data = ((result[1] & 15) << 8) | result[2]
        return data

    def read_voltage(self, channel):
        raw = self.read_raw(channel)
        return (raw / 4095.0) * self.vref
    
    def read_canal(self, channel):
        raw = self.read_raw(channel)
        return raw

    def close(self):
        self.spi.close()