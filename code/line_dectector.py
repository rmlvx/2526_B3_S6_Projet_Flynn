class LineDetector:
    def __init__(self, adc_instance, threshold=1.5):
        self.adc = adc_instance
        self.threshold = threshold

    def read_status(self):
        """Lit les 8 capteurs et renvoie les tensions et la position."""
        # Lecture des 8 canaux
        v = [self.adc.read_voltage(i) for i in range(8)]
        
        # Formatage de l'affichage (identique à vos logs)
        volt_str = (f"L:{v[0]:.2f}V | L1:{v[1]:.2f}V | L2:{v[2]:.2f}V | "
                    f"C:{v[3]:.2f}V | C1:{v[4]:.2f}V | "
                    f"R:{v[5]:.2f}V | R1:{v[6]:.2f}V | R2:{v[7]:.2f}V")
        
        # Logique de détection
        if v[0] < self.threshold or v[1] < self.threshold or v[2] < self.threshold:
            position = "Line on the left"
        elif v[3] < self.threshold or v[4] < self.threshold:
            position = "Line in the center"
        elif v[5] < self.threshold or v[6] < self.threshold or v[7] < self.threshold:
            position = "Line on the right"
        else:
            position = "No line detected"
            
        return volt_str, position