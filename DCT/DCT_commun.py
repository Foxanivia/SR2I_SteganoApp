import numpy as np
from PIL import Image
from skimage import color
from scipy.fftpack import dct, idct
from DCT.zigzag import *

def get_quantization_table():
    quantization_table = [
        [16, 12, 14, 14, 18, 24, 49, 72],
        [11, 12, 13, 17, 22, 35, 64, 92],
        [10, 14, 16, 22, 37, 55, 78, 95],
        [16, 19, 24, 29, 56, 64, 87, 98],
        [24, 26, 40, 51, 68, 81, 103, 112],
        [40, 58, 57, 87, 109, 104, 121, 100],
        [51, 60, 69, 80, 103, 113, 120, 103],
        [61, 55, 56, 62, 77, 92, 101, 99]
    ]
    return quantization_table

def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

def get_canals_numbers(path_img):
    with Image.open(path_img) as img:
        mode = img.mode
        canal_number = len(mode)
        return mode, canal_number

def prepare_image(img_path):
    # Ouvrir l'image et la convertir en un tableau numpy
    img = Image.open(img_path)
    img_array = np.array(img)

    # Vérifier le mode de l'image et ajuster si nécessaire
    mode, canals_num = get_canals_numbers(img_path)
    if mode == "RGBA":
        img_array = img_array[:, :, :3]  # Conserver uniquement les trois premiers canaux pour RGB
    elif mode != "RGBA" and mode != "RGB":
        raise ValueError("L'image doit être en RGB ou RGBA.")

    # Convertir de RGB à YCbCr
    ycbcr_array = color.rgb2ycbcr(img_array)

    save_ycbcr_channels(ycbcr_array, "ressources/img/result/test")

    # Normaliser les valeurs pour qu'elles soient des entiers
    ycbcr_array = np.round(ycbcr_array).astype(np.uint8)

    return ycbcr_array

def center_YCbCr_values(ycbcr_array):
    # Retirer 127 à chaque composante pour centrer les valeurs autour de 0
    centered_array = ycbcr_array.astype(np.int16) - 127
    return centered_array

def convert_rgb_to_ycbcr(img_array):
    # Convertir l'image RGB en YCbCr
    img_ycbcr = color.rgb2ycbcr(img_array)
    return img_ycbcr


def img_to_squares8x8(img_array):
    square_list = []
    for col in np.vsplit(img_array, int(img_array.shape[0] / 8)):
        for square in np.hsplit(col, int(img_array.shape[1] / 8)):
            square_list.append(square)
    return square_list

def apply_dct_on_block(block):
    # Appliquer DCT sur les lignes
    dct_block = dct(block, axis=0, norm='ortho')
    # Appliquer DCT sur les colonnes
    dct_block = dct(dct_block, axis=1, norm='ortho')
    return dct_block

def apply_dct_on_all_blocks(blocks_list):
    dct_blocks_list = [apply_dct_on_block(block) for block in blocks_list]
    return dct_blocks_list

def apply_zigzag_to_all_blocks(dct_blocks_list):
    zigzag_blocks_list = [np.reshape(zigzag(block), (8,8)) for block in dct_blocks_list]
    return zigzag_blocks_list

def apply_inverse_zigzag_to_all_blocks(blocks_list):
    inverse_blocks_list = [np.reshape(inverse_zigzag(block), (8,8)) for block in blocks_list]
    return inverse_blocks_list


def apply_quantization(block, quantization_table):
    # Assurer que block et quantization_table sont des np.array
    block_array = np.array(block)

    # Appliquer la quantification
    quantized_block = np.round(block_array / quantization_table).astype(np.int32)
    return quantized_block


def apply_quantization_to_all_blocks(blocks_list):
    # Convertir quantization_table en np.array une seule fois
    quantization_table = np.array(get_quantization_table())
    quantized_blocks_list = [apply_quantization(block, quantization_table) for block in blocks_list]
    return quantized_blocks_list





def blocks_to_image(blocks, image_shape):
    rows = image_shape[0] - image_shape[0] % 8
    cols = image_shape[1] - image_shape[1] % 8
    image_array = np.zeros((rows, cols), dtype=np.float32)

    current_row = 0
    for i in range(0, len(blocks), cols // 8):
        current_block_row = np.hstack(blocks[i:i + cols // 8])
        image_array[current_row:current_row + 8, :cols] = current_block_row
        current_row += 8

    return image_array



##############################
#             Debug          #
##############################

def save_ycbcr_channels(img_ycbcr, base_filename):
    # Extraire les canaux Y, Cb, et Cr
    Y, Cb, Cr = img_ycbcr[:, :, 0], img_ycbcr[:, :, 1], img_ycbcr[:, :, 2]

    # Créer une image en niveaux de gris pour Y
    Y_img = Image.fromarray(np.uint8(Y))
    Y_img.save(f'{base_filename}_Y.jpg', 'JPEG')

    # Pour Cb et Cr, créer des images colorées
    # Fixer Y à 128 pour visualiser les canaux de chrominance
    Y_fixed = 128 * np.ones_like(Y)

    # Créer des images YCbCr pour Cb et Cr avec Y fixe et convertir en RGB
    Cb_img_array = color.ycbcr2rgb(np.stack((Y_fixed, Cb, np.zeros_like(Cb)), axis=-1))
    Cr_img_array = color.ycbcr2rgb(np.stack((Y_fixed, np.zeros_like(Cr), Cr), axis=-1))

    # Convertir les tableaux en images PIL et sauvegarder
    Cb_img = Image.fromarray((Cb_img_array * 255).astype(np.uint8))
    Cr_img = Image.fromarray((Cr_img_array * 255).astype(np.uint8))

    Cb_img.save(f'{base_filename}_Cb.jpg', 'JPEG')
    Cr_img.save(f'{base_filename}_Cr.jpg', 'JPEG')