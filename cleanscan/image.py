""" Module for wrapping cv2 images """

import cv2

""" Class for wrapping cv2 images """


class Image:
    def __init__(self, data):
        """ Initializes image with given image data """
        self.data = data

    @classmethod
    def load(cls, path):
        """ Loads an image and returns it """
        return cls(cv2.imread(str(path)))

    def save(self, path):
        """ Saves image to path """
        cv2.imwrite(str(path), self.data)

    def clean(self):
        gray = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        # Dilate edged image to close contours
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(edged, kernel)
        return Image(dilated)


def load(path):
    """ Loads and returns image from path """

    return Image.load(path)
