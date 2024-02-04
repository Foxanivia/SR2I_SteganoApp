import os
from PIL import Image
import numpy as np

def is_valid_type(path_img):
    return os.path.splitext(path_img)[1].lower() in ['.jpg', '.jpeg', '.png']


def get_canals_numbers(path_img):
    with Image.open(path_img) as img:
        return img.mode, len(img.mode)


def verify_encoding(message):
    try:
        message.encode('ascii')
        return 'ASCII', 1
    except UnicodeEncodeError:
        return 'Unicode', 4


def message_to_bin(message):
    return ''.join(format(ord(char), '08b') for char in message)


def process_image(img_path, process_func):
    with Image.open(img_path) as img:
        img_array = np.array(img)
        return process_func(img_array)

def linear_normalization(path_img, bits=1):
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