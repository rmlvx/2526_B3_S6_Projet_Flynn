import glob
import time
import os
import plotext as plt
import pandas as pd

def get_latest_log():
    """Trouve le fichier CSV le plus récent dans le dossier logs/"""
    list_of_files = glob.glob("logs/*.csv")
    if not list_of_files:
        return None
    return max(list_of_files, key=os.path.getctime)

def run_dashboard():
    latest_file = get_latest_log()
    if not latest_file:
        print("[ERREUR] Aucun log trouvé. Lancez d'abord python main.py !")
        return

    print(f"--- Tableau de bord connecté à : {latest_file} ---")
    print("Initialisation...")
    time.sleep(1)

    try:
        while True:
            try:
                # On lit uniquement les 80 dernières lignes pour que ça reste fluide
                df = pd.read_csv(latest_file).tail(80)
                
                # Conversion des données en listes pour le graphique
                magnitude = df["Magnitude"].tolist()
                az = df["Az"].tolist()
                timestamps = df["Timestamp"].tolist()

                # --- DESSIN DU GRAPHIQUE ---
                plt.clear_terminal() # Efface l'écran précédent
                
                plt.title("Télémétrie IMU en Temps Réel (Ctrl+C pour quitter)")
                
                # Tracé des courbes
                plt.plot(magnitude, label="Magnitude (Norme 1g)", color="red")
                plt.plot(az, label="Axe Z (Haut/Bas)", color="cyan")
                
                # Lignes de repères (Seuils)
                plt.hline(1.0, color="green")  # La gravité idéale (1g)
                plt.hline(0.1, color="red")    # Le seuil d'arrêt d'urgence du failsafe
                
                # Réglage de l'affichage
                plt.ylim(-0.5, 2.5) # Fixe l'échelle Y (en g)
                plt.plotsize(100, 30) # Largeur x Hauteur dans le terminal
                
                plt.show()

            except Exception as e:
                # Ignore les erreurs (ex: fichier en cours d'écriture par le robot)
                pass 
            
            # Rafraîchissement rapide (environ 5 images/seconde)
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nArrêt du tableau de bord.")

if __name__ == "__main__":
    run_dashboard()