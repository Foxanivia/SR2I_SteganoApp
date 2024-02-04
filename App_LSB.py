###################
#  Bibliothèques  #
###################
import sys
from LSB.LSB_interaction import *
from LSB.LSB_encode import *
from LSB.LSB_decode import *

###################
#  Main fonction  #
###################
def main(input_path= None,output_path= None):
    """
    Processus general d'encodage et décodage de l'image avec LSB
    :return:
    """

    # Choix de l'utilisateur
    if input_path is None:
        image_path = demande_choix_image()
    if output_path is None:
        output_path = "ressources/img/result/encoded_image.png"
    msg_to_hide = demande_message_to_encode()
    choix = demande_mode_LSB()
    canal_number = demande_nbr_canaux(get_canals_numbers(image_path)[1])

    # Processus d'encodage et de décodage guidé
    if choix == '1':
        bit_number = demande_nbr_bits()
        encode_message(image_path,  output_path ,msg_to_hide, bit_number, canal_number)
        decode_message(output_path, bit_number, canal_number)
        linear_normalization(output_path)
    else:
        encode_message_lsb_matching(image_path, output_path, msg_to_hide, canal_number)
        decode_message(output_path, canals=canal_number)
        linear_normalization(output_path)

def encode_only(output_path = None):
    """
    Ne fait que cacher le secret
    :return:
    """
    # Choix de l'utilisateur
    image_path = demande_choix_image()
    if output_path is None:
        output_path = "ressources/img/result/encoded_image.png"
    msg_to_hide = demande_message_to_encode()
    choix = demande_mode_LSB()
    canal_number = demande_nbr_canaux(get_canals_numbers(image_path)[1])

    # Encodage de l'image
    if choix == '1':
        bit_number = demande_nbr_bits()
        encode_message(image_path, output_path,msg_to_hide, bit_number, canal_number)
    else:
        encode_message_lsb_matching(image_path,output_path, msg_to_hide, canal_number)


def decode_only():
    """
    Récupère le secret seulement
    :return:
    """
    image_path = demande_choix_image("ressources/img/result")
    canal_number = demande_nbr_canaux(get_canals_numbers(image_path)[1])
    bit_number = demande_nbr_bits()
    decode_message(image_path, bit_number, canal_number)


if __name__ == '__main__':

    if "-d" in sys.argv:
        decode_only()
    elif "-e" in sys.argv:
        encode_only()
    else:
        main()
