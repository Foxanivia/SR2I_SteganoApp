import os
import sys
import glob

import src.nn


def load_model(nn, model_name):
    # Get the directory where the models are installed
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, os.pardir, 'models')

    model_path = os.path.join(dir_path, model_name + ".h5")
    if not os.path.isfile(model_path):
        print(f"ERROR: Model file not found: {model_path}\n")
        sys.exit(-1)
    nn.load_model(model_path, quiet=True)
    return nn


def init(image_path: str):

    path = os.path.join(os.getcwd(), image_path)


    os.environ["CUDA_VISIBLE_DEVICES"] = "CPU"
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    if os.path.isdir(path):
        files = glob.glob(os.path.join(path, '*.*'))
    else:
        files = [path]

    nn = src.nn.Neural("effnetb0")

    return [nn, files]

#Only png
def lsbr(image_path: str) -> None:
    i = init(image_path)
    nn = load_model(i[0], "effnetb0-A-alaska2-lsbr")
    lsbr_pred = nn.predict(nn.filter_images(i[1]), 1)

    return lsbr_pred[0]


#only jpg
def steghide(image_path: str) -> None:
    i = init(image_path)
    nn = load_model(i[0], "effnetb0-A-alaska2-steghide")
    steghide_pred = nn.predict(nn.filter_images(i[1]), 10)

    return steghide_pred[0]


