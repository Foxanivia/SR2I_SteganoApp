import argparse
from analyse_nn import lsbr, steghide
from attack import spa
#from attack import analyse_supplementaire_1, analyse_supplementaire_2, analyse_supplementaire_3, analyse_supplementaire_4, analyse_supplementaire_5

def main():
    parser = argparse.ArgumentParser(description="Some steganalysis tools")
    parser.add_argument("image_path", type=str, help="Image path to analyse")
    parser.add_argument("--method", type=str, choices=['ia_lsbr', 'ia_steghide', 'pairanal', 'sup2', 'sup3', 'sup4', 'sup5'], help="Steganalysis method to be used")

    args = parser.parse_args()

    if args.method == 'ia_lsbr':
        print("Probabilité d'utilisation de LSBR sur cette image : {}l".format(lsbr(args.image_path)))
    elif args.method == 'ia_steghide':
        print("Probabilité d'utilisation de Steghide sur cette image : {}l".format(steghide(args.image_path)))
    elif args.method == 'pairanal':
        spa(args.image_path)
    else:
        print("Unknown analysis method !")

if __name__ == "__main__":
    main()
