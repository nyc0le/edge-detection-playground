import cv2
import numpy as np


def convert_to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def apply_sobel(gray, ksize):
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)

    magnitude = cv2.magnitude(grad_x, grad_y)

    magnitude = np.uint8(
        255 * magnitude / np.max(magnitude)
    )

    return magnitude


def apply_laplacian(gray, ksize):
    laplacian = cv2.Laplacian(
        gray,
        cv2.CV_64F,
        ksize=ksize
    )

    laplacian = np.absolute(laplacian)

    laplacian = np.uint8(
        255 * laplacian / np.max(laplacian)
    )

    return laplacian


def apply_canny(gray, threshold1, threshold2, blur_size):
    blurred = cv2.GaussianBlur(
        gray,
        (blur_size, blur_size),
        0
    )

    edges = cv2.Canny(
        blurred,
        threshold1,
        threshold2
    )

    return edges