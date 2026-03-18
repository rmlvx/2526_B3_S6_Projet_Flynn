from drivers.mcp3208 import MCP3208
import time

# === Configuration ===
THRESHOLD = 2007  # Au-delà de 3500 c'est NOIR, sinon c'est BLANC
DELAY = 0.5       # J'ai augmenté un peu le délai pour que l'affichage soit lisible

def main():
    adc = MCP3208(vref=3.3)

    try:
        print("Test des capteurs : Détection NOIR / BLANC (Ctrl+C pour arrêter)...")

        while True:
            # 1. On lit les valeurs brutes des 8 capteurs (de 0 à 7)
            valeurs_brutes = [adc.read_canal(i) for i in range(8)]
            
            # 2. On crée une liste vide pour stocker l'état (NOIR ou BLANC)
            etats_capteurs = []
            
            # 3. On analyse chaque valeur brute
            for val in valeurs_brutes:
                if val > THRESHOLD:
                    etats_capteurs.append("NOIR ") # L'espace ajoute un peu d'alignement
                else:
                    etats_capteurs.append("BLANC")
            
            # 4. Affichage des résultats
            print(f"Brutes : {valeurs_brutes}")
            print(f"États  : {etats_capteurs}")
            print("-" * 50) # Ligne de séparation pour la lisibilité

            time.sleep(DELAY)

    except KeyboardInterrupt:
        adc.close()
        print("\nProgramme arrêté proprement.")

    except Exception as e:
        adc.close()
        print(f"Erreur détectée: {e}")

if __name__ == "__main__":
    main()