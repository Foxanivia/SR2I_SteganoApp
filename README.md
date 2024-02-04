
# Projet Stegano SR2I203

## Description
Ce projet implémente un système de stéganalyse avancé utilisant des techniques d'intelligence artificielle et des méthodes d'analyse traditionnelles pour détecter la présence de données cachées dans des images numériques. Il fournit une interface en ligne de commande (CLI) pour analyser des images en utilisant diverses méthodes, y compris deux réseaux de neurones différents et deux méthodes d'attaques structurelles .

## Installation

### Prérequis
- Python 3.8 ou plus récent
- pip pour la gestion des packages Python

### Configuration de l'environnement
Il est recommandé d'utiliser un environnement virtuel pour éviter les conflits de dépendances.

```bash
python -m venv env
source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate`
```

### Installation des dépendances
Installez les dépendances nécessaires à l'aide de `pip` :

```bash
pip install -r requirements.txt
```

## Utilisation

Pour analyser une image, utilisez la commande suivante dans le terminal :

```bash
python main.py --method nom_methode nom_image
```

`nom_methode` peut être l'un des suivants : `ia_lsb`, `ia_steghide`, `spa`.

## Méthodes d'Analyse

- **ia_lsbr** : Utilise le réseau de neurones pour l'analyse lsbr.
- **ia_steghide** : Utilise le réseau de neurones pour l'analyse steghide.
- **spa** : attaque SimplePairs (statistique sur le fait que le LSBR est une opération asymétrique : LSBR fait augmenter la valeur des pixels pairs et decrémenter la valeur des pixels impairs).


## Cloisonement

## Auteurs

