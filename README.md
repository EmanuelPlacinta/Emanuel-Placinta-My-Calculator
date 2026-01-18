# La calculatrice 

Une calculatrice graphique complète et élégante développée en Python avec Tkinter. Ce projet va au-delà d'une simple interface en intégrant ses propres algorithmes de calcul trigonométrique basés sur les séries de Taylor et une gestion intelligente de l'historique

---

## Fonctionnalités

* **Calculs Scientifiques "Maison"** : Implémentation manuelle de sin, cos et tan via les séries de Taylor (sans utiliser la bibliothèque math)
* **Priorité des Opérations** : Analyseur d'expressions (parser) gérant les parenthèses (), les puissances **, ainsi que la priorité de la multiplication/division sur l'addition
* **Système d'Historique** : Un panneau latéral dédié enregistre chaque opération. Vous pouvez consulter vos anciens résultats ou vider la liste en un clic
* **Interface Moderne** : Design inspiré des calculatrices mobiles avec un code couleur ergonomique et un affichage adaptatif (notation scientifique pour les grands nombres)
* **Centrage Automatique** : L'application détecte la résolution de votre écran pour s'ouvrir parfaitement au centre au démarrage

---

## Installation & Lancement
### 1. Prérequis
Python 3.x installé.
Tkinter (généralement inclus par défaut avec Python sur Windows et macOS)

### 2. Lancement
Aucune installation de bibliothèque tierce n'est requise. Téléchargez le fichier et lancez :
```bash
python calculator.py
```

### 3. Technologies
* **Langage : Python 3.x**
* **Interface Graphique : Tkinter**
* **Logique : Algorithmes mathématiques personnalisés (Séries de Taylor, gestion de priorité opératoire)**

---

## Guide d'utilisation

Opérations de base : Utilisez le pavé numérique et les opérateurs classiques (+, -, ×, ÷)
### Fonctions avancées :
* ** ** **: Élévation à la puissance
* ** √ **: Calcul de la racine carrée du nombre affiché
* ** **sin/cos/tan : Calcule la valeur trigonométrique du nombre actuel (en degrés)

###Gestion de l'affichage :
* **AC **: Efface l'écran et réinitialise les calculs en cours
* **+/- **: Bascule entre positif et négatif
* **% **: Divise la valeur actuelle par 100

###Historique :
Les calculs s'ajoutent automatiquement à droite
Utilisez le bouton Effacer sous la liste pour remettre l'historique à zéro

---

