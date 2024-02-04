from LSB.LSB_commun import *


def decode_message(encoded_img_path, bits=1, canals=1):
    # Vérifie que le nombre de bits est soit 1 soit 2
    if bits not in range(1, 9):
        raise ValueError("Le nombre de bits doit être 1 ou 2 ou 3.")
    if get_canals_numbers(encoded_img_path)[1] < canals:
        raise ValueError("Erreur Canal ")

    # Chargement de l'image encodée
    img = Image.open(encoded_img_path)
    img_array = np.array(img)
    delimiter = "1111111111111110"
    bin_message = ''
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(canals):
                bin_message += format(img_array[i, j, k] & (2 ** bits - 1), f'0{bits}b')

    # Conversion du message binaire en ASCII
    bin_message = bin_message.split(delimiter)[0]
    message = ''.join([chr(int(bin_message[i:i + 8], 2)) for i in range(0, len(bin_message), 8)])
    print("Message décodé:", message)
