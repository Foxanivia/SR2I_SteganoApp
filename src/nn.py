import os
import sys

import imageio
import numpy as np
import tensorflow as tf
import efficientnet.tfkeras as efn
import tensorflow.keras.layers as L

from imageio import imread



class Neural:

    def __init__(self, network, shape=(512, 512, 3)):

        self.model_dir = 'models'
        self.shape = shape
        if network == "effnetb0":
            self.model = self.create_model_effnetb0()
        else:
            print("NN __init__ Error: network not found")
            sys.exit(0)

    def create_model_effnetb0(self):

        input_shape = self.shape

        model = tf.keras.Sequential([
            efn.EfficientNetB0(
                input_shape=input_shape,
                weights='imagenet',
                include_top=False
            ),
            L.GlobalAveragePooling2D(),
            L.Dense(2, activation='softmax')

        ])
        return model

    def pred_generator(self, image_list, batch):

        images = []
        for f in image_list:
            img = np.zeros(self.shape)
            try:
                I = imread(f)

                # This function must support images with variable size
                # Note that with big images we are only analyzing a small part
                d0 = min(I.shape[0], self.shape[0])
                d1 = min(I.shape[1], self.shape[1])
                d2 = min(I.shape[2], self.shape[2])
                img[:d0, :d1, :d2] = I[:d0, :d1, :d2]

            except Exception as e:
                print(str(e))
                print("NN pred_generator warning: cannot read image:", f)

            images.append(img)

            if len(images) == batch:
                X = np.array(images).astype('float32') / 255
                yield X
                images = []

        if len(images) > 0:
            X = np.array(images).astype('float32') / 255
            yield X

    def filter_images(self, files):

        files_ok = []
        for f in files:
            try:
                img = imageio.v2.imread(f)
            except:
                print("WARNING: cannot read, image ignored:", f)
                continue

            if len(img.shape) != 3 or img.shape[2] != self.shape[2]:
                print("WARNING: image ignored:", f, ", expected number of channels:",
                      self.shape[2])
                continue

            """
            if (img.shape[0] < self.shape[0] or
                img.shape[1] < self.shape[1]):
                print("WARNING: image ignored:", f, ", image too small, expected:",
                       self.shape[0], "x", self.shape[1])
                continue
            """
            files_ok.append(f)
        return files_ok

    def load_model(self, model_path, quiet=False):

        if os.path.exists(model_path):
            if not quiet:
                print("Loading", model_path, "...")
            self.model.load_weights(model_path)
        elif not quiet:
            print("WARNING: model file not found:", model_path)

    def predict(self, files, batch, verbose=None):

        verb = 1
        if len(files) < batch:
            batch = 1
            verb = 0
        if verbose != None:
            verb = verbose
        steps = len(files) // batch
        # print("steps:", steps, "batch:", batch)
        # print("files:", files[:steps*batch])
        g = self.pred_generator(files[:steps * batch], batch)
        pred = self.model.predict(g, steps=steps, verbose=verb)[:, -1]
        if steps * batch < len(files):
            g = self.pred_generator(files[steps * batch:], batch)
            pred = pred.tolist() + self.model.predict(g, steps=1, verbose=verb)[:, -1].tolist()
        return np.array(pred)
