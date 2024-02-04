###################
#  Bibliothèques  #
###################

import os
from PIL import Image
import numpy as np

##########################
#  Encode/Decode Commun  #
##########################
def is_valid_type(path_img):
    """
    Renvoie si l'image choisis est supporté par le script
    :param path_img:
    :return:
    """
    return os.path.splitext(path_img)[1].lower() in ['.jpg', '.jpeg', '.png']


def get_canals_numbers(path_img):
    """
    Récupère le nombre de canaux utilisable dans l'image
    :param path_img:
    :return:
    """
    with Image.open(path_img) as img:
        return img.mode, len(img.mode)


def verify_encoding(message):
    """
    Vérifie l'encodage de l'image (reste d'une première version qui visait à être trop complète en utilisant ascii et Unicode)
    :param message:
    :return:
    """
    try:
        message.encode('ascii')
        return 'ASCII', 1
    except UnicodeEncodeError:
        return 'Unicode', 4


def message_to_bin(message):
    """
    Retourne le binaire correspondant du message
    :param message:
    :return:
    """
    return ''.join(format(ord(char), '08b') for char in message)


def process_image(img_path, process_func):
    """
    Récupère le tableau de pixel de l'image sous forme d'un objet numpy
    :param img_path:
    :param process_func:
    :return:
    """
    with Image.open(img_path) as img:
        img_array = np.array(img)
        return process_func(img_array)

#####################################
#  Verification basique de l'image  #
#####################################

def linear_normalization(path_img, bits=1):
    """
    Utilisation de la normalisation linéaire des LSB pour vérifier si l'image possède un secret
    :param path_img:
    :param bits:
    :return:
    """
    # Ouvrir l'image
    img = Image.open(path_img)
    img_array = np.array(img)

    # Calcul du facteur de normalisation
    normalization_factor = 255 // (2 ** bits - 1)

    # Extraire le LSB de chaque composante de couleur en utilisant des opérations vectorielles
    lsb_array = (img_array & (2 ** bits - 1)) * normalization_factor

    # Convertir la matrice LSB en image
    lsb_img = Image.fromarray(lsb_array.astype(np.uint8))

    # Sauvegarde de l'image résultante pour visualisation
    lsb_img_path = "ressources/img/result/normalized_image.png"
    lsb_img.save(lsb_img_path)