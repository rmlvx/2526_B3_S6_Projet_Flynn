# Projet Gyroscope LSM6DSOX : Driver I2C et Fusion de Capteurs


## 🚀 Vue d'Ensemble

Ce projet fournit un **driver Python pour le capteur IMU LSM6DSOX** de STMicroelectronics, utilisé via l'interface I2C sur une plateforme comme le Raspberry Pi.

L'objectif principal est de lire les données brutes d'accélération (en $g$) et de vitesse angulaire (en $dps$), puis d'appliquer un **Filtre Complémentaire** pour calculer une **orientation 3D stable (Roll, Pitch, Yaw)**.
***
## 🛠️ Prérequis

Pour exécuter ce projet, vous devez disposer :

1. D'un capteur **LSM6DSOX** câblé correctement.
2. D'une plateforme avec support I2C (ex : Raspberry Pi).
3. De la librairie Python `smbus2`.

```Bash
# S'assurer que le support I2C soit bien activé sur le système (ex: raspi-config)
sudo apt-get install python3-smbus
# Installer la librairie Python
pip install smbus2
```
***
## 📂 Structure du Projet

Le projet est divisé en quatre fichiers principaux pour garantir une architecture propre (Programmation Orientée Objet - POO) :

| **Fichier**                          | **Rôle**                 | **Description**                                                                                                                                                         |
| ------------------------------------ | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`main.py`**                        | **Point d'Entrée**       | Initialise l'application (`IMU_Application`) et gère le cycle de vie (`initialize`, `run`, `cleanup`).                                                                  |
| **`driver/app.py`**                  | **Contrôleur**           | Gère la boucle principale de lecture, l'instanciation du capteur et l'intégration du `ComplementaryFilter`.                                                             |
| **`driver/settings.py`**             | **Configuration**        | Centralise toutes les constantes matérielles (adresses I2C, registres) et les mappings pour les différentes plages de mesure du capteur.                                |
| **`driver/lsm6dsox.py`**             | **Driver de Bas Niveau** | Contient la classe `LSM6DSOX_IMU` qui gère la communication I2C, le soft reset, la configuration des registres et la conversion des données brutes en unités physiques. |
| **`driver/complementary_filter.py`** | **Fusion de Capteurs**   | Contient la classe `ComplementaryFilter` pour combiner les données Accélérateur et Gyroscope.                                                                           |

***

## ⚙️ Fonctionnalités Clés

### 1. Driver Dynamique (`lsm6dsox.py` & `settings.py`)

Le driver I2C a été amélioré pour supporter toutes les plages (Full Scale - FS) du composant :

- **Accéléromètre FS :** $\pm 2g, \pm 4g, \pm 8g, \pm 16g$.
    
- **Gyroscope FS :** $\pm 125 dps, \pm 250 dps, \pm 500 dps, \pm 1000 dps, \pm 2000 dps$.
    

**Utilisation :** La plage est choisie lors de l'instanciation du capteur dans `app.py`.


```python
# Exemple dans app.py pour configurer le capteur en +/- 4g et +/- 1000 dps
self.sensor = LSM6DSOX_IMU(
    fs_accel='4g',     
    fs_gyro='1000dps'  
)
```

### 2. Algorithme de Fusion : Filtre Complémentaire (`complementary_filter.py`)

Pour surmonter les limitations des capteurs individuels, l'orientation finale est calculée par fusion de capteurs :

|**Capteur**|**Mesure**|**Inconvénient**|**Rôle dans la Fusion**|
|---|---|---|---|
|**Accéléromètre**|Orientation statique|Très sensible aux mouvements (bruit).|**Correction à long terme** (stable).|
|**Gyroscope**|Vitesse angulaire|Dérive sur le temps (accumulation d'erreur).|**Réactivité à court terme** (rapide).|

Le filtre utilise la constante $\mathbf{ALPHA = 0.98}$ pour pondérer les données. Une valeur proche de `1.0` signifie que le filtre fait principalement confiance au Gyroscope, utilisant l'Accéléromètre uniquement pour corriger la dérive.

#### Formule du Filtre (Roll/Pitch)

$$\text{Angle Fused} = \mathbf{ALPHA} \times (\text{Angle Gyro Prédictif}) + (1 - \mathbf{ALPHA}) \times (\text{Angle Accel Statique})$$

#### Calcul du Yaw (Lacet)

L'angle de Yaw est calculé par simple intégration du taux de rotation sur l'axe Z ($G_z$), car l'Accéléromètre ne peut pas corriger la dérive du Yaw. _Pour une correction sans dérive du Yaw, un Magnétomètre est nécessaire._

***

## ▶️ Exécution du Projet

1. Assurez-vous que l'adresse I2C `LSM6DSOX_ADDR` dans `settings.py` correspond à votre configuration (par défaut : `0x6A`).
    
2. Exécutez le script principal :
    

```bash
python3 main.py
```

Le programme affichera les données brutes des deux capteurs, suivies des angles stabilisés (Roll, Pitch, Yaw) calculés par le Filtre Complémentaire.

---

## 📝 Améliorations Futures

- **Calibration :** Implémenter une routine de calibration pour déterminer les biais (offsets) des gyroscopes.
    
- **Magnétomètre :** Intégrer un magnétomètre pour obtenir une orientation absolue et sans dérive sur l'axe du Yaw.
    
- **Filtre de Kalman :** Remplacer le Filtre Complémentaire par un Filtre de Kalman pour une fusion plus optimale des incertitudes des capteurs.
    
- **ODR Dynamique :** Rendre l'Output Data Rate (ODR) configurable par l'utilisateur (actuellement fixé à $26 Hz$).


© Zoléni KOKOLO ZASSI | Clara CHATELAIS-VAUFLEURY | Damien THEAS CHARLOT
24 octobre 2025