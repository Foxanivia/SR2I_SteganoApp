import os
from LSB.LSB_commun import *

def demande_choix_image(dossier_cible="ressources/img/"):
    # Vérifier si le dossier existe
    if not os.path.exists(dossier_cible):
        print("Le dossier spécifié n'existe pas.")
        exit()

    # Liste les images dans le dossier
    fichiers = os.listdir(dossier_cible)
    images = [f for f in fichiers if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if len(images) == 0:
        print("Aucune image trouvée dans le dossier.")
        exit()

    else:
        print(f"Choisissez un numéro pour une image dans {dossier_cible} ou 'exit': ")
        for index, image in enumerate(images):
            print(f"{index}) {image}")
        print()

        while True:
            choix = input("Entrez le numéro de l'image ou 'exit': ")
            if choix.lower() == 'exit':
                exit()
            elif choix.isdigit() and 0 <= int(choix) < len(images):
                print()
                return dossier_cible+"/"+images[int(choix)]
            else:
                print("Entrée invalide. Veuillez réessayer.\n")


def demande_mode_LSB():
    while True:
        choix = input("Veuillez choisir un mode :\n1) LSB normal\n2) LSB matching\n")
        if choix.lower() == 'exit':
            exit()
        if choix in ['1', '2']:
            return choix
        print("Entrée invalide. Veuillez saisir 1 ou 2.")


def demande_message_to_encode():
    while True:
        msg = input("Veuillez entrer le message à cacher (encodage ASCII) : ")
        if msg.lower() == 'exit':
            exit()
        if verify_encoding(msg)[0] == 'ASCII':
            print()
            return msg
        print("Votre message ne peut pas être encodé en ASCII. Recommencez.\n")

def demande_nbr_canaux(max_canaux):
    while True:
        msg = input(f"Veuillez entrer le nombre de canaux à utiliser (max {max_canaux}): ")
        if msg.isdigit() and int(msg) <= max_canaux and int(msg) > 0:
            print()
            return int(msg)
        print("Entrée invalide. Veuillez saisir un nombre.\n")

def demande_nbr_bits():
    while True:
        nbr_bit = input("Veuillez choisir un nombre de bits (Max 8) : ")
        if nbr_bit.isdigit() and 1 <= int(nbr_bit) <= 8:
            return int(nbr_bit)
        print("Entrée invalide. Veuillez saisir un nombre entre 1 et 8.\n")

