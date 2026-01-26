<div align="center">

  <h1>🤖 Projet Flynn</h1>

  <p>
    <img src="https://img.shields.io/badge/Status-En_D%C3%A9veloppement-orange" alt="Status" />
    <img src="https://img.shields.io/badge/Version-1.0.0-blue" alt="Version" />
    <img src="https://img.shields.io/badge/Hardware-Raspberry_Pi_Zero_2W-C51A4A?logo=raspberry-pi&logoColor=white" alt="Hardware" />
    <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
    <br>
    </p>

  <p>
    <em>Un robot autonome suiveur de ligne avec vision par ordinateur, alliant conception électronique et traitement du signal sur Raspberry Pi.</em>
  </p>

</div>

---

## 📖 À propos

Le **Projet Flynn** a pour objectif de concevoir, prototyper et déployer un robot mobile autonome. Sa mission principale est de suivre des trajectoires (lignes noires ou blanches) sur différents types de surfaces grâce à un système de vision par ordinateur embarqué.

Ce projet s'inscrit dans une démarche d'ingénierie complète, combinant :
* **Conception PCB** sous Kicad.
* **Traitement d'image** et du signal pour la navigation.
* **Pilotage moteur** précis via des drivers silencieux.

<!-- ## 🎥 Démonstration

![Demo](https://via.placeholder.com/800x400?text=Inserer+GIF+ou+Video+du+Robot+Ici) -->

## 🛠️ Architecture Matérielle (BOM)

Le cerveau du robot est une **Raspberry Pi Zero 2W** qui centralise les données des capteurs et assure le pilotage des actionneurs en temps réel.

| Composant | Qté | Fonction | Réf / Doc |
| :--- | :---: | :---: | :---: |
| **Raspberry Pi Zero 2W** | 1 | Unité centrale de contrôle & Vision | [Datasheet](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#raspberry-pi-zero-2-w) |
| **LSM6DSOX** | 1 | IMU (Accéléromètre/Gyro) - Mesure X,Y,Z | [Datasheet](https://www.st.com/resource/en/datasheet/lsm6dsox.pdf) |
| **TMC2225** | 2 | Driver Moteur (Contrôle précis et silencieux) | [Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/TMC2225_datasheet_rev1.14.pdf) |
| **MCP3208** | 1 | ADC 12-bit - Conversion détection couleur | [Datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/21298E.pdf) |

## 💻 Stack Technique

* **Langage** : ![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
* **Conception PCB** : ![Kicad](https://img.shields.io/badge/KiCad-9.0-314CB0?logo=kicad&logoColor=white)
* **VCS** : ![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)

## 🚀 Installation et Démarrage

### Prérequis

* Une Raspberry Pi Zero 2W avec **Raspberry Pi OS** configuré.
* Accès SSH ou terminal activé.
* Interfaces **SPI** et **I2C** activées via `raspi-config`.

### Installation

Clonez le dépôt sur votre Raspberry Pi et installez les dépendances nécessaires :

```bash
# Cloner le dépôt
git clone [https://github.com/votre-user/projet-flynn.git](https://github.com/votre-user/projet-flynn.git)

# Accéder au dossier
cd projet-flynn

# Installer les dépendances Python
pip install -r requirements.txt
```

## 👥 L'Équipe

<div align="center">

| Raphaël MILVAUX | Emire GUIOSE | Merihene REKIK | Zoléni KOKOLO ZASSI |
| :---: | :---: | :---: | :---: |
| <a href="https://github.com/rmlvx"><img src="https://wsrv.nl/?url=github.com/rmlvx.png&w=100&h=100&mask=circle" alt="rmlvx"></a> | <a href="https://github.com/emiregse"><img src="https://wsrv.nl/?url=github.com/emiregse.png&w=100&h=100&mask=circle" alt="emiregse"></a> | <a href="https://github.com/skelf24"><img src="https://wsrv.nl/?url=github.com/skelf24.png&w=100&h=100&mask=circle" alt="skelf24"></a> | <a href="https://github.com/Sikoso774"><img src="https://wsrv.nl/?url=github.com/Sikoso774.png&w=100&h=100&mask=circle" alt="Sikoso774"></a> |

</div>

<br>

<div align="left">
  <img src="https://www.ensea.fr/sites/default/files/styles/paragraph_image/public/content/paragraphs/images/2024-06/Logo%20ENSEA%20RVB.png.webp?itok=HkgQVZf7" alt="Logo ENSEA" width="100" />
  <br><br>
  <strong>© 2026 - Raphaël MILVAUX, Emire GUIOSE, Merihene REKIK, Zoléni KOKOLO ZASSI.</strong><br>
  <em>Projet réalisé dans le cadre de la formation ENSEA.</em>
</div>

<br>

<div align="left">
  <img src="https://www.ensea.fr/sites/default/files/styles/paragraph_image/public/content/paragraphs/images/2024-06/Logo%20ENSEA%20RVB.png.webp?itok=HkgQVZf7" alt="Logo ENSEA" width="100" />
  <br><br>
  <strong>© 2026 - Raphaël MILVAUX, Emire GUIOSE, Merihene REKIK, Zoléni KOKOLO ZASSI.</strong><br>
  <em>Projet réalisé dans le cadre de la formation ENSEA.</em>
</div>
