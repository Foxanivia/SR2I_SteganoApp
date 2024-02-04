###################
#  Bibliothèques  #
###################
from LSB.LSB_commun import *


##########################
#  Encode LSBr           #
##########################
def encode_message(image_path,output_path, message, bits=1, canals=1):
    """
    Récupère une image et utilise n bits sur k canaux pour cacher un secret dedans à l'aide du LSBr
    :param image_path:
    :param message:
    :param bits:
    :param canals:
    :return:
    """

    ### Vérification des param d'entrée
    if bits not in range(1, 9):
        raise ValueError("Le nombre de bits doit être 1, 2 ou 3.")
    if get_canals_numbers(image_path)[1] < canals:
        raise ValueError("Erreur Canal ")

    ### Prépare le secret à être caché
    delimiter = "1111111111111110"
    bin_message = message_to_bin(message)
    bin_message += delimiter

    ### Récupère l'image sous format array de numpy
    img = Image.open(image_path)
    img_array = np.array(img)

    ### Lève une erreur si l'image n'a pas assez de place avec les n bits et k canaux pour cacher le secret
    if img_array.shape[0] * img_array.shape[1] < len(bin_message) / bits:
        raise ValueError("L'image est trop petite pour contenir le message avec l'encodage de {} bits.".format(bits))

    ### Parcours l'ensemble des bits et canaux necessaire pour cacher l'image avec LSBr
    index = 0
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(canals):
                if index < len(bin_message):
                    # LSB remplacement
                    img_array[i, j, k] = (img_array[i, j, k] & ~(2 ** bits - 1)) | int(bin_message[index:index + bits], 2)
                    index += bits
                else:
                    break
        else:
            continue
        break

    ### Enregistre l'image avec le secret caché
    encoded_img = Image.fromarray(img_array)
    encoded_img_path = output_path
    encoded_img.save(encoded_img_path)
    print("Message encodé dans l'image et sauvegardé en tant que", encoded_img_path)
    return encoded_img_path



##########################
#  Encode LSBm           #
##########################
def encode_message_lsb_matching(image_path,output_path, message, canals=1):
    """
    Récupère une image et cache un secret avec la méthode LSBm, elle peut utiliser plusieurs canaux mais qu'un seul bit.
    :param image_path:
    :param message:
    :param canals:
    :return:
    """

    ### Vérification des param d'entrée
    bits = 1
    if get_canals_numbers(image_path)[1] < canals:
        raise ValueError("Erreur Canal ")

    ### Prépare le secret à être caché
    delimiter = "1111111111111110"
    bin_message = message_to_bin(message) + delimiter

    ### Récupère l'image sous format array de numpy
    img = Image.open(image_path)
    img_array = np.array(img)

    if img_array.shape[0] * img_array.shape[1] < len(bin_message) / bits:
        raise ValueError("L'image est trop petite pour contenir le message avec l'encodage de {} bits.".format(bits))

    ### Parcours l'ensemble des bits et canaux necessaire pour cacher l'image avec LSBm
    index = 0
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(canals):
                if index < len(bin_message):
                    # LSB matching
                    bit_to_hide = int(bin_message[index])
                    current_bit = img_array[i, j, k] & 1
                    if bit_to_hide != current_bit:
                        if img_array[i, j, k] == 255:
                            img_array[i, j, k] -= 1
                        elif img_array[i, j, k] == 0:
                            img_array[i, j, k] += 1
                        else:
                            img_array[i, j, k] += 1 if (img_array[i, j, k] & 1) == 0 else -1
                    index += bits
                else:
                    break

    ### Enregistre l'image avec le secret caché
    encoded_img = Image.fromarray(img_array)
    encoded_img_path = output_path
    encoded_img.save(encoded_img_path)
    print("Message encodé avec LSB matching dans l'image et sauvegardé en tant que", encoded_img_path)
    return encoded_img_path