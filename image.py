""" Module for wrapping cv2 images """

import cv2

""" Class for wrapping cv2 images """


class Image:
    def __init__(self, path):
        """ Initializes image by loading it from path """
        self.data = cv2.imread(str(path))

    def save(self, path):
        """ Saves image to path """
        cv2.imwrite(str(path), self.data)


def load(path):
    """ Loads and returns image from path """

    return Image(path)
