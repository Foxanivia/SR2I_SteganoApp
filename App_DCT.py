from DCT.DCT_encode import *
from DCT.DCT_decode import *
import cv2
from skimage import color

def main():

    print("Ce petit programme a pour but de montrer l'utilisation de la méthode DCT.")
    print("De par la complexité de cette dernière elle n'est que partiellement implémenté.")
    print("Vous avez la possibilité de voir l'impact d'une modification brut et sans distinction sur les hautes fréquences:\n 0) Extraction sans impact\n 1) Impact\n 2) Exit ")

    # Gestion réponse
    IMPACT =0
    while True:
        result = input()
        if result =='0':

            break
        if result =='1':
            IMPACT = 1
            break
        if result =='2':
            exit()

    ## - Exemple d'utilisation
    img_path = "ressources/img/lenna.jpg"

    ## - Préparer l'image et convertir en YCbCr
    ycbcr_image = prepare_image(img_path)
    ycbcr_image = center_YCbCr_values(ycbcr_image)

    ## - Découper les canaux en blocs de 8x8
    Y_blocks = img_to_squares8x8(ycbcr_image[:, :, 0])
    Cb_blocks = img_to_squares8x8(ycbcr_image[:,:,1])
    Cr_blocks = img_to_squares8x8(ycbcr_image[:,:,2])

    # Application de la DCT 2D
    Y_block_DCT = apply_dct_on_all_blocks(Y_blocks)

    #Quantization
    quantified_Y_blocks = apply_quantization_to_all_blocks(Y_block_DCT)

    # Sort coef with ZigZag
    zig_zag_y_block = np.array(apply_zigzag_to_all_blocks(quantified_Y_blocks))

    # Impact sur les hautes fréquences
    if IMPACT ==1:
        zig_zag_y_block[0][5][5] = 1

    # Inverse sort
    zig_zag_inverse_block = apply_inverse_zigzag_to_all_blocks(zig_zag_y_block)
    print(zig_zag_inverse_block[0])

    # Déquantization
    dct_dequants = [np.multiply(data, get_quantization_table()) for data in zig_zag_inverse_block]

    # IDCT
    idct_blocks = [np.round(cv2.idct(block)) for block in dct_dequants]

    # Reassemble_image
    assembled_blocks = blocks_to_image(idct_blocks,ycbcr_image[:, :, 0].shape)

    # Remet sur un format 0 à 255 PNG
    assembled_blocks = np.clip((assembled_blocks + 127),0,255).astype(np.uint8)

    # Exemple modification de l'itensité
    Y_img = Image.fromarray(np.uint8(assembled_blocks))
    Y_img.save(f'{"ressources/img/result/steg_CDT"}_Y.jpg', 'JPEG')

if __name__ == '__main__':
    main()
