import csv
import os
from datetime import datetime

class DataLogger:
    def __init__(self, folder='logs'):
        self.file = None
        self.filename = ""
        
        # Create the folder if it does not exist
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        # File name with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"{folder}/session_{timestamp}.csv"
        
        try:
            self.file = open(self.filename, mode='w', newline='')
            self.writer = csv.writer(self.file)
            # Standard headers
            self.writer.writerow(["Timestamp", "Ax", "Ay", "Az", "Magnitude", "ADC", "Statut"])
            print(f"[LOG] Fichier créé : {self.filename}")
        except Exception as e:
            print(f"[LOG] Erreur création fichier : {e}")

    def log(self, ax, ay, az, magnitude, adc_volts, status_msg):
        """Saves a row of data"""
        if self.file:
            t = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            try:
                self.writer.writerow([
                    t, 
                    f"{ax:.3f}", f"{ay:.3f}", f"{az:.3f}", 
                    f"{magnitude:.3f}", f"{adc_volts:.2f}", 
                    status_msg
                ])
                self.file.flush() # Force disk write
            except Exception:
                pass

    def close(self):
        if self.file:
            self.file.close()
            print(f"[LOG] Session sauvegardée.")