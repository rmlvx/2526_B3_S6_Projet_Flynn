# 📘 Documentation Technique - Projet Flynn

## 1. Présentation du Projet
Ce projet consiste en la réalisation d'un robot auto-équilibré (pendule inversé) piloté par une Raspberry Pi Zero 2W.
Le système repose sur une boucle de contrôle rapide (20Hz+) lisant une centrale inertielle (IMU) et pilotant deux moteurs pas-à-pas.

---

## 2. Architecture Matérielle (Hardware)

### Cœur du système
* **Carte Mère :** Raspberry Pi Zero 2W
* **OS :** Raspberry Pi OS (Legacy/Lite)

### Pinout & Connexions (GPIO BCM)
Voici le mapping validé entre le PCB et le code Python (`config.py`).

| Composant | Signal | Pin Physique (Board) | GPIO (BCM) | Note |
| :--- | :--- | :--- | :--- | :--- |
| **Moteur Gauche** | STEP | 32 | **GPIO 12** | |
| (TMC2225) | DIR | 36 | **GPIO 16** | |
| **Moteur Droit** | STEP | 33 | **GPIO 13** | |
| (TMC2225) | DIR | 31 | **GPIO 6** | |
| **IMU (LSM6DSOX)**| SDA | 3 | **GPIO 2** | Bus I2C-1 |
| | SCL | 5 | **GPIO 3** | Bus I2C-1 |
| **ADC (MCP3208)** | CS | 24 | **GPIO 8** | Bus SPI-0 (CE0) |
| | MOSI | 19 | **GPIO 10** | |
| | MISO | 21 | **GPIO 9** | |
| | SCLK | 23 | **GPIO 11** | |

---

## 3. Architecture Logicielle (Software)

Le code est structuré de manière modulaire pour faciliter la maintenance et les tests.

```text
code/
├── main.py          # Point d'entrée (Lanceur)
├── machine.py       # Cerveau (Logique d'état, Failsafe, Boucle principale)
├── config.py        # Configuration (Constantes, Pinout)
├── logger.py        # Gestionnaire d'enregistrement CSV
└── drivers/         # Couche d'abstraction matérielle (HAL)
    ├── lsm6dsox.py  # Pilote I2C pour Accéléromètre/Gyro
    ├── mcp3208.py   # Pilote SPI pour capteurs analogiques
    └── tmc2225.py   # Pilote GPIO pour moteurs (avec Threading)
```

### Fonctionnalités Clés
1.  **Auto-Réparation (Self-Healing) :** Si l'IMU est déconnecté (faux contact), le système détecte l'erreur, passe en mode "RECONNEXION", et tente de réinitialiser le bus I2C sans planter le script.
2.  **Sécurité (Failsafe) :**
    * Si l'accélération détectée est < 0.1g (chute libre ou erreur lecture 0,0,0) -> **Arrêt Moteurs Immédiat**.
    * Si inclinaison excessive -> **Arrêt Moteurs**.
3.  **Logging :** Chaque session crée un fichier `.csv` dans le dossier `logs/` avec horodatage, données brutes et codes d'état.

---

## 4. Guide d'Installation & Commandes

### Installation initiale
```bash
# 1. Cloner le dépôt
git clone [https://github.com/rmlvx/2526_B3_S6_Projet_Flynn.git](https://github.com/rmlvx/2526_B3_S6_Projet_Flynn.git)
cd 2526_B3_S6_Projet_Flynn/code

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances (via uv pour la rapidité)
pip install uv
uv pip install -r requirements.txt
```

### Lancer le robot
```bash
# Toujours activer l'environnement avant
source .venv/bin/activate

# Lancer le programme principal
python main.py
```

---

## 5. Dépannage Git (Mémo)

Si le dépôt local est corrompu ou désynchronisé, voici les commandes de secours utilisées lors du développement.

### Cas 1 : "Je veux juste récupérer la version du serveur (Table Rase)"
*Attention : Ceci efface les modifications locales non sauvegardées.*
```bash
git fetch origin
git reset --hard origin/main
```

### Cas 2 : "Git refuse d'ajouter un dossier (Submodule error)"
Si un dossier (ex: `others/`) contient un `.git` caché :
```bash
# Supprimer le .git intrus
rm -rf others/dossier_problematique/.git
# Retirer du cache git
git rm --cached others/dossier_problematique
# Ajouter proprement
git add .
```

### Cas 3 : "Push rejeté (Updates were rejected)"
Si l'historique local a été recréé (reset) et diffère du serveur :
```bash
git push -u origin main --force
```
