""" Module for wrapping cv2 images """

import cv2
import imutils
import numpy as np
import skimage.filters as filters
from cleanscan.transform import four_point_transform

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

    def gray(self):
        """ Convert to gray scale """
        grayscale = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        return Image(grayscale)

    def edges(self):
        """ Edge detetion """
        edged = cv2.Canny(self.data, 75, 200)

        # Dilate edged image to close contours
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(edged, kernel)
        return Image(dilated)

    def contours(self):
        """ Attempts to find the contour of the paper """

        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        contours = cv2.findContours(self.data, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        approxContour = None
        contour = None

        # loop over the contours
        for c in contours:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                approxContour = approx
                contour = c
                break

        if type(approxContour) == type(None):
            raise Exception("Could not locate outline of paper.")

        return (approxContour, contour)

    def drawContour(self, contour):
        """ Draws contour on top of image """
        withContours = self.data.copy()
        cv2.drawContours(withContours, [contour], -1, (0, 255, 0), 2)
        return Image(withContours)

    def warp(self, contour):
        """ Warp content of square contour so it fills the entire image """

        warped = four_point_transform(self.data, contour.reshape(4, 2))
        return Image(warped)

    def crop(self, marginLeft, marginTop, marginRight, marginBottom):
        """ Crop image removing given margins in pixels """

        ny, nx = self.data.shape

        left = marginLeft
        right = nx - marginRight
        top = marginTop
        bottom = ny - marginBottom

        contour = np.array(
            [
                [[left, top]],
                [[left, bottom]],
                [[right, bottom]],
                [[right, top]],
            ]
        )

        return self.warp(contour)

    def monocrome(self):
        """ Convert image to monocrome """

        data = self.data.copy()

        T = filters.threshold_local(data, 201, offset=10, method="gaussian", param=4)
        T2 = filters.threshold_mean(data)
        T_comb = np.minimum(T, T2)
        data = (data > T_comb).astype("uint8") * 255

        return Image(data)

    def clean(self):
        """ Clean the image """

        gray = self.gray()
        edges = gray.edges()
        (approxContour, contour) = edges.contours()

        warped = gray.warp(approxContour)
        cropped = warped.crop(30, 30, 30, 30)
        monocrome = cropped.monocrome()

        return monocrome


def load(path):
    """ Loads and returns image from path """

    return Image.load(path)
