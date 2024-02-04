from DCT.DCT_encode import *
from DCT.DCT_decode import *
import cv2
from skimage import color


def main():
    """
    Ce petit programme a pour but de montrer l'utilisation de la méthode DCT.
    De par la complexité de cette dernière elle n'est que partiellement implémenté.
    :return:
    """

    print("!!! CE SCRIPT SE DEROULE PAR ETAPE PRESSEZ ENTREZ POUR CONTINUER JUSQU A LA FIN !!!")
    print("Ce script à pour but de montrer toutes les étapes de la méthode stéganographique DCT.")
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
    print(f"\n1)  Nous récupérons l'image: {img_path}")


    ## - Préparer l'image et convertir en YCbCr
    ycbcr_image = prepare_image(img_path, verbose=1)
    ycbcr_image = center_YCbCr_values(ycbcr_image,verbose=1)


    ## - Découper les canaux en blocs de 8x8
    a = input()
    print("\n6) Nous séparons les canaux en 3 puis nous séparons chacun des canaux en bitmap de 8*8")
    Y_blocks = img_to_squares8x8(ycbcr_image[:, :, 0])
    Cb_blocks = img_to_squares8x8(ycbcr_image[:,:,1])
    Cr_blocks = img_to_squares8x8(ycbcr_image[:,:,2])
    print("Voici la première bitmap de chacun des canaux")
    print("Canal Y:")
    print(Y_blocks[0])
    print("Canal Cb:")
    print(Cb_blocks[0])
    print("Canal Cr:")
    print(Cr_blocks[0])

    # Application de la DCT 2D
    a = input()
    print("\n7) Nous récupérons seulement le canal Y pour l'intensité et nous appliquons une DCT en 2 dimensions:")
    Y_block_DCT = apply_dct_on_all_blocks(Y_blocks)
    print(Y_block_DCT[0])

    #Quantization
    quantified_Y_blocks = apply_quantization_to_all_blocks(Y_block_DCT)
    a = input()
    print("\n8) Nous utilisons la matrice de quantification JPEG sur chacune de nos bitmap:\n(Chaque valeur est arrondi pour ne conserver que les fréquences les plus importantes.)")
    print(quantified_Y_blocks[0])

    # Sort coef with ZigZag
    zig_zag_y_block = np.array(apply_zigzag_to_all_blocks(quantified_Y_blocks))
    a = input()
    print("\n9) Nous utilisons par la suite l'algorithme de ZigZag pour classer dans l'ordre les bits les plus importants ")

    # Impact sur les hautes fréquences
    a = input()
    print("10) Les bits les plus importants sont au débuts")
    if IMPACT ==1:
        print("Vous avez choisis une implémentation permettant de regarder l'impact de modification des fréquences\nNous allons donc modifier la première séquence avec un bit (Comme ça serait le cas en LSB pour montrer son impact).")
        zig_zag_y_block[0][0][0] += 1
    else:
        print(" Vous avez choisis une implémentation sans cacher de data ")
    print("(Nous pouvons utiliser la méthode LSB pour cacher des data à ce moment là)")
    print(zig_zag_y_block[0][0])


    # Inverse sort
    zig_zag_inverse_block = apply_inverse_zigzag_to_all_blocks(zig_zag_y_block)
    a = input()
    print("\n11) Nous utilisons l'algorithme de zig zag inverse pour remmetre les bits dans l'ordre")
    print(zig_zag_inverse_block[0][0])


    # Déquantization
    dct_dequants = [np.multiply(data, get_quantization_table()) for data in zig_zag_inverse_block]
    a = input()
    print("\n12) Nous multiplions par les quantificateurs jpeg")
    print(dct_dequants[0][0])

    # IDCT
    idct_blocks = [np.round(cv2.idct(block)) for block in dct_dequants]
    a = input()
    print("\n13) Nous utilisons une idct pour récupérer nos bits de base ")
    print(idct_blocks[0][0])

    # Reassemble_image
    assembled_blocks = blocks_to_image(idct_blocks,ycbcr_image[:, :, 0].shape)
    a = input()
    print("\n14) Nous réassembons les bloques pour former une image")

    # Remet sur un format 0 à 255 PNG
    assembled_blocks = np.clip((assembled_blocks + 127),0,255).astype(np.uint8)

    # Exemple modification de l'itensité
    Y_img = Image.fromarray(np.uint8(assembled_blocks))
    Y_img.save(f'{"ressources/img/result/steg_CDT"}_Y.jpg', 'JPEG')
    a = input()
    print("15) Le canal Y de l'image peut être regardé dans ressources/img/result/steg_CDT_Y.jpg")
    print("Fin du script.")


if __name__ == '__main__':
    main()
