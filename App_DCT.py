from DCT.DCT_encode import *
from DCT.DCT_decode import *

def main():
    ## - Exemple d'utilisation
    message = "Secret Message"
    img_path = "ressources/img/lenna.jpg"
    output_path = "ressources/img/result/lenna_stego.jpg"

    ## - Préparer l'image et convertir en YCbCr
    prepared_image = prepare_image(img_path)
    ycbcr_image = convert_rgb_to_ycbcr(prepared_image)
    #save_ycbcr_channels(ycbcr_image, "ressources/img/result/test")


    ## - Découper le canal Y en blocs de 8x8
    Y_channel = ycbcr_image[:, :, 0]
    Y_img = Image.fromarray(np.uint8(Y_channel))
    Y_img.save(f'{"ressources/img/result/test"}_Y.jpg', 'JPEG')

    Y_blocks = img_to_squares8x8(Y_channel)

    ## - Appliquer la DCT et modifier les coefficients pour cacher le message
    modified_Y_blocks = apply_dct_modify_coefficients(Y_blocks, message)

    ## - Reconstruire le canal Y à partir des blocs modifiés
    rows, cols = Y_channel.shape
    modified_Y_image = blocks_to_image(modified_Y_blocks, (rows, cols))
    print(modified_Y_image[0])

    Y_img = Image.fromarray(np.uint8(modified_Y_image))
    Y_img.save(f'{"ressources/img/result/test_modif"}_Y.jpg', 'JPEG')

    ## - Remplacer le canal Y modifié dans l'image YCbCr
    modified_ycbcr_image = np.copy(ycbcr_image)
    modified_ycbcr_image[:, :, 0] = modified_Y_image

    ## - Convertir l'image YCbCr modifiée en RGB pour sauvegarde
    modified_rgb_image = color.ycbcr2rgb(modified_ycbcr_image)
    modified_rgb_image = (modified_rgb_image * 255).astype(np.uint8)
    print(modified_rgb_image[0])
    ## - Sauvegarder l'image modifiée
    image = Image.fromarray(modified_rgb_image)
    image.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == '__main__':
    main()
