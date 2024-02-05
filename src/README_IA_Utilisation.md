
# Notes Importantes sur l'Utilisation de l'IA

Ce document contient des instructions cruciales pour l'utilisation optimale des réseaux d'intelligence artificielle (IA) dédiés à la stéganographie d'images. Suivez attentivement ces directives pour garantir la fiabilité et l'efficacité de vos opérations de stéganographie.

## Taille des Images

- Les réseaux ont été entraînés avec des images de taille **512x512 pixels**. Il est fortement recommandé d'utiliser des images s'approchant de cette résolution pour obtenir les meilleurs résultats. La fiabilité de détection diminue avec l'éloignement de cette taille idéale.

## Contenu du Message

- Le message à stéganographier doit être **conséquent**. Assurez-vous que le message constitue au moins **10% de la taille totale de l'image initiale**. Cette proportion est cruciale pour que le réseau de neuronnes ait une bonne appréciation.

## Randomisation du Message

- Pour une stéganographie efficace, le message doit être **suffisamment randomisé**. Une randomisation adéquate a un impact significatif sur la réduction du bruit perceptible et sur la visibilité des modifications des bits de poids faible (LSB - Least Significant Bit) de l'image. Un message prévisible, vraissemblable ou structuré peut augmenter le risque de détection.
