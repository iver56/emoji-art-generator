import numpy as np


def calculate_mse(image_a, image_b):
    """
    Calculate the mean squared error between two images.
    The two images must have the same shape.
    :param image_a: 2D numpy array with float-like data type
    :param image_b: 2D numpy array with float-like data type
    :return: mse
    """
    err = np.sum((image_a - image_b) ** 2)
    #err /= float(image_a.shape[0] * image_a.shape[1])
    return err
