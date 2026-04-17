from drivers.mcp3208 import MCP3208
import time

# === Configuration ===
THRESHOLD = 2007   # Above 3500 it's BLACK; otherwise it's WHITE
DELAY = 0.10       # Delay slightly to make the display easier to read

def main():
    adc = MCP3208(vref=3.3)

    try:
        print("Test des capteurs : Détection NOIR / BLANC (Ctrl+C pour arrêter)...")

        while True:
            # 1. Read the raw values from the 8 sensors (0 through 7)
            valeurs_brutes = [adc.read_canal(i) for i in range(8)]
            
            # 2. Create an empty list to store the state (BLACK or WHITE)
            etats_capteurs = []
            
            # 3. Analyze each raw value
            for val in valeurs_brutes:
                if val > THRESHOLD:
                    etats_capteurs.append("NOIR ") # A space adds a bit of alignment
                else:
                    etats_capteurs.append("BLANC")
            
            # 4. Displaying results
            print(f"Brutes : {valeurs_brutes}")
            # print(f"États  : {etats_capteurs}")
            # print("-" * 50) # Ligne de séparation pour la lisibilité

            time.sleep(DELAY)

    except KeyboardInterrupt:
        adc.close()
        print("\nProgramme arrêté proprement.")

    except Exception as e:
        adc.close()
        print(f"Erreur détectée: {e}")

if __name__ == "__main__":
    main()