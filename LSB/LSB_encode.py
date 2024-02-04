from LSB.LSB_commun import *

def encode_message(image_path, message, bits=1, canals=1):
    if bits not in range(1, 9):
        raise ValueError("Le nombre de bits doit être 1, 2 ou 3.")
    if get_canals_numbers(image_path)[1] < canals:
        raise ValueError("Erreur Canal ")

    delimiter = "1111111111111110"

    bin_message = message_to_bin(message)
    bin_message += delimiter

    img = Image.open(image_path)
    img_array = np.array(img)

    if img_array.shape[0] * img_array.shape[1] < len(bin_message) / bits:
        raise ValueError("L'image est trop petite pour contenir le message avec l'encodage de {} bits.".format(bits))

    index = 0
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(canals):
                if index < len(bin_message):
                    img_array[i, j, k] = (img_array[i, j, k] & ~(2 ** bits - 1)) | int(bin_message[index:index + bits], 2)
                    index += bits
                else:
                    break
        else:
            continue
        break

    encoded_img = Image.fromarray(img_array)
    encoded_img_path = "ressources/img/result/encoded_image.png"
    encoded_img.save(encoded_img_path)
    print("Message encodé dans l'image et sauvegardé en tant que", encoded_img_path)
    return encoded_img_path


def encode_message_lsb_matching(image_path, message, canals=1):
    bits = 1
    if get_canals_numbers(image_path)[1] < canals:
        raise ValueError("Erreur Canal ")

    delimiter = "1111111111111110"
    bin_message = message_to_bin(message) + delimiter

    img = Image.open(image_path)
    img_array = np.array(img)

    if img_array.shape[0] * img_array.shape[1] < len(bin_message) / bits:
        raise ValueError("L'image est trop petite pour contenir le message avec l'encodage de {} bits.".format(bits))

    index = 0
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(canals):
                if index < len(bin_message):
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

    encoded_img = Image.fromarray(img_array)
    encoded_img_path = "ressources/img/result/encoded_image_lsb_matching.png"
    encoded_img.save(encoded_img_path)
    print("Message encodé avec LSB matching dans l'image et sauvegardé en tant que", encoded_img_path)
    return encoded_img_path