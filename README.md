
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

## Utilisation "IA detection"

Pour analyser une image, utilisez la commande suivante dans le terminal :

```bash
python main.py --method nom_methode nom_image
```

`nom_methode` peut être l'un des suivants : `ia_lsb`, `ia_steghide`, `spa`.

## Méthodes d'Analyse

- **ia_lsbr** : Utilise le réseau de neurones pour l'analyse lsbr.
- **ia_steghide** : Utilise le réseau de neurones pour l'analyse steghide.
- **spa** : attaque SimplePairs (statistique sur le fait que le LSBR est une opération asymétrique : LSBR fait augmenter la valeur des pixels pairs et decrémenter la valeur des pixels impairs).

## Utilisation "création d'image steganographique"

### LSB 

#### Commande

```bash
python App_LSB.py
```

#### Fonctionnement

- Ce petit script guide l'utilisateur dans la création d'une image steganographique.
- L'utilisateur doit indiquer une image présente dans le repertoire ressource/img.
- L'utilisateur indique ensuite son mode de steganographique (LSB simple ou LSB matching)
- Le mode de récupération du mot de passe est le même pour LSB simple et LSB matching
- L'utilisateur indique le nombre de canaux utilisés
- Si l'utilisateur a choisis LSB normal, lui demande le nombre de bit à utiliser

#### Resultat 

- Les résultats apparaissent dans ressource/img/result
- L'image steganographié est dans ressource/img/result/encoded_image.png
- L'image avec une normalisation des LSB est dans ressource/img/result/encoded_image.png

#### Commande:

Afin de seulement cacher un secret.
Le choix de chemin de sorti n'est que partiellement implémenter. 
```bash
python App_DCT.py -e
```

#### Commande:
Afin de seulement récupérer un secret.
Le choix du chemin d'entrée n'est que partiellement implémenté.
```bash
python App_DCT.py -d 
```

### DCT



#### Commande:

```bash
python App_DCT.py
```

#### Fonctionnement 
L'utilisation de la méthode DCT étant délicate ce script explique l'ensemble de son fonctionnement étape par étape. 
Le fait de cacher un message avec cette méthode n'est pas trivial.
Le script explique donc de lui même l'ensemble des étapes passé et des actions effectué. 

#### Resultat

Dans le dossier /ressources/img/result se trouvent un ensemble d'image généré au cours des explications. 
- steg_CDT_Y.jpg (Image utilisant la méthode DCT pour montrer le retour à la normal du canal Y après épuration des hautes fréquences)
- test_Cb.jpg 
- test_Cr.jpg 
- test_Y.jpg (qui montrent toutes trois la décomposition en YCbCr de l'image)

## Auteurs

Lucas MARACINE 
Loïc TESTA

