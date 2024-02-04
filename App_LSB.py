from LSB.LSB_interaction import *
from LSB.LSB_encode import *
from LSB.LSB_decode import *

def main():

    # Choice Image and message
    image_path = demande_choix_image()
    #msg_to_hide = "Testing message"
    msg_to_hide = demande_message_to_encode()
    choix = demande_mode_LSB()

    canal_number = demande_nbr_canaux(get_canals_numbers(image_path)[1])

    if choix == '1':
        bit_number = demande_nbr_bits()
        encode_message(image_path, msg_to_hide, bit_number, canal_number)
        decode_message("ressources/img/result/encoded_image.png", bit_number, canal_number)
        linear_normalization("ressources/img/result/encoded_image.png")
    else:
        encode_message_lsb_matching(image_path, msg_to_hide, canal_number)
        decode_message("ressources/img/result/encoded_image_lsb_matching.png", canals=canal_number)
        linear_normalization("ressources/img/result/encoded_image_lsb_matching.png")


if __name__ == '__main__':
    main()
