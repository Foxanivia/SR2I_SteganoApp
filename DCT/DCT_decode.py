from DCT.DCT_commun import *

def binary_to_string(bin_message):
    """Convertir un message binaire en chaîne de caractères."""
    return ''.join([chr(int(bin_message[i:i + 8], 2)) for i in range(0, len(bin_message), 8)])

def recover_hidden_message(img_path):
    """
    Methode non implémenté
    :param img_path:
    :return:
    """
    return ""