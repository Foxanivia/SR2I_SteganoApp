import numpy as np

def zigzag(input):
    # Initialiser les variables
    h = 0
    v = 0
    vmin = 0
    hmin = 0
    vmax = input.shape[0]
    hmax = input.shape[1]
    # On considère la taille de la sortie comme vmax * hmax
    i = 0

    output = []
    while (v < vmax) and (h < hmax):
        if (h + v) % 2 == 0:  # Aller vers le haut
            if v == vmin:
                output.append(input[v, h])  # Si tout en haut, aller à droite
                if h == hmax:
                    v = v + 1
                else:
                    h = h + 1
                i = i + 1
            elif (h == hmax -1 ) and (v < vmax):  # Sinon si à droite, aller vers le bas
                output.append(input[v, h])
                v = v + 1
                i = i + 1
            elif (v > vmin) and (h < hmax -1 ):  # Sinon aller en diagonale
                output.append(input[v, h])
                v = v - 1
                h = h + 1
                i = i + 1
        else:  # Aller vers le bas
            if (h == hmin) and (v < vmax) and (v != vmax -1):  # Si tout à gauche et pas en bas
                output.append(input[v, h])
                v = v + 1
                i = i + 1
            elif v == vmax -1:  # Si en bas, aller à droite
                output.append(input[v, h])
                h = h + 1
                i = i + 1
            elif (v < vmax -1) and (h > hmin):  # Sinon aller en diagonale
                output.append(input[v, h])
                v = v + 1
                h = h - 1
                i = i + 1
        if (v == vmax) and (h == hmax):
            break

    return output

def inverse_zigzag(input):
    liste_64_elements = input.flatten().tolist()

    # Initialiser les variables
    h = 0
    v = 0
    vmin = 0
    hmin = 0
    vmax = input.shape[0]
    hmax = input.shape[1]
    # On considère la taille de la sortie comme vmax * hmax
    i = 0
    output = np.empty((8,8))

    while (v < vmax) and (h < hmax):
        if (h + v) % 2 == 0:  # Aller vers le haut
            if v == vmin:
                output[v][h] = liste_64_elements[i]
                if h == hmax:
                    v = v + 1
                else:
                    h = h + 1
                i = i + 1
            elif (h == hmax - 1) and (v < vmax):  # Sinon si à droite, aller vers le bas
                output[v][h] = liste_64_elements[i]
                v = v + 1
                i = i + 1
            elif (v > vmin) and (h < hmax - 1):  # Sinon aller en diagonale
                output[v][h] = liste_64_elements[i]
                v = v - 1
                h = h + 1
                i = i + 1
        else:  # Aller vers le bas
            if (h == hmin) and (v < vmax) and (v != vmax - 1):  # Si tout à gauche et pas en bas
                output[v][h] = liste_64_elements[i]
                v = v + 1
                i = i + 1
            elif v == vmax - 1:  # Si en bas, aller à droite
                output[v][h] = liste_64_elements[i]
                h = h + 1
                i = i + 1
            elif (v < vmax - 1) and (h > hmin):  # Sinon aller en diagonale
                output[v][h] = liste_64_elements[i]
                v = v + 1
                h = h - 1
                i = i + 1
        if (v == vmax) and (h == hmax):
            break

    return output
