import numpy as np
from PIL import Image
from skimage import color
from scipy.fftpack import dct, idct

def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

def get_canals_numbers(path_img):
    with Image.open(path_img) as img:
        mode = img.mode
        canal_number = len(mode)
        return mode, canal_number

def prepare_image(img_path):
    # Ouvrir l'image
    img = Image.open(img_path)
    img_array = np.array(img)
    mode,canals_num = get_canals_numbers(img_path)
    print(mode)
    if mode == "RGBA":
        img_array = img_array[:, :, :3]
    elif mode != "RGBA" and mode != "RGB":
        raise ValueError("L'image doit être en RGB ou RGBA.")
    return img_array

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

def apply_dct(block):
    # Appliquer la DCT 2D (DCT type-II) sur le bloc
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def apply_dct_on_blocks(blocks):
    # Appliquer la DCT à chaque bloc de 8x8 pixels
    dct_blocks = [apply_dct(block) for block in blocks]
    return dct_blocks

def apply_idct(block):
    # Appliquer la IDCT 2D (IDCT type-II) sur le bloc
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

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