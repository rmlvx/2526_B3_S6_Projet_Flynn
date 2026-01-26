# 🗒️ Journaling

Ce fichier retrace les jours du projet

***

## Jour 1 : 2026-01-20

- Le professeur M. Nicolas PAPAZOGLOU nous a chargé de concevoir un PCB de A à Z qui doit s'adpater sur la Raspberry PI Zero 2W avec ses PINS pour commander un moteur qui dirigera le robot suiveur de lignes FLYNN.
- On a commencé à prendre en main la section "Projects" d'un répertoire GitHub. Raphaël a créer le répertoire du projet et a ouvert cette section pour assigner des ToDo aux mebres du groupe.
- Pour partager et déposer le répértoire sans rien casser du travail des autres membres :
  - a. Faire la commande ``git clone https://github.com/user/nom_du_projet`` pour recopier le projet
  - b. Faire ses modifications puis faire ``git add .`` et ``git commit -m "Nom du message"``
  - c. Lier le projet Git local avec GitHub : ``git remote add origin https://github.com/user/nom_du_projet``
  - d. Si votre brache est nommé master, la renommer avec main avec cette commande : git branch -m master main
  - Rémettre à jour le projet avec git pull et publier le projet git push origin main

***

## Jour 2 : 2026-01-20

- Avancement des schémas des composants sur KICAD
- Finition de la documentation & augmentation du remplissage du journaling

***

## Jour 3 : 2026-01-23

M. Fiack observe nos schémas KICAD pour donner des observations.

- Les labels globaux à éviter, mettre des label hiérarchiques.
- Si on se trompe, on peut modifier les valeurs de ces labels et cela se modifie directement avec le schéma.
- Tracer des lignes de séparation au lieu d'avoir des rectangles.
- Faire un schéma en 2D pour savoir comprendre ce que l'on peut mettre.
- Risque de court-circuit si on lie le ``+3.3V`` du mosfet avec le +``3.3V`` de la Raspberry PI...
- La Rapsberry a besoin d'une tension de ``+5V``.
- Power_Supply (Faire une page en + )
- Brancher les LED pour vérifier que le courant passe bien.
- On met une résistance pour limiter le courant pour éviter de faire cramer la LED.
- Capacités de découplage

A 11h, M. Papazoglou nous a expliqué quelles empreintes il faudrait mettre pour chaque résistance, condensateur, etc.

***

## Jour 4 : 2026-01-26

- 08:45 : M. PAPAZOGLOU a corrigé lquelques erreurs rencontrées lors de la conception du PCB sur PCB Editor sur Kicad sur l'OS Ubuntu.
- 08:52 : Correction des erreurs dans le logiciel Kicad sur Ubuntu.
