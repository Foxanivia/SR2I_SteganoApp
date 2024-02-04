from DCT.DCT_commun import *

def binary_to_string(bin_message):
    """Convertir un message binaire en chaîne de caractères."""
    return ''.join([chr(int(bin_message[i:i + 8], 2)) for i in range(0, len(bin_message), 8)])

def recover_hidden_message(img_path):
    # Préparer l'image et convertir en YCbCr
    img_array = prepare_image(img_path)
    print(img_array[0])
    img_ycbcr = convert_rgb_to_ycbcr(img_array)

    # Travailler uniquement avec le canal Y
    Y_channel = img_ycbcr[:, :, 0]

    # Découper le canal Y en blocs de 8x8
    Y_blocks = img_to_squares8x8(Y_channel)

    # Initialiser le message binaire caché
    hidden_binary_message = ''

    # Récupérer le message caché dans les coefficients de 4,4 à 7,7
    for block in Y_blocks:
        break
        for i in range(4, 8):
            for j in range(4, 8):
                coef = block[i, j]
                hidden_binary_message += str(int(coef) & 1)  # Récupérer le dernier bit

    # Convertir le message binaire en chaîne de caractères
    return binary_to_string(hidden_binary_message)