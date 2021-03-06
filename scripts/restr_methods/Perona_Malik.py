import numpy as np
from scipy import ndimage


def Perona_Malik(im, dd, delta, kappa):

    """
    Function which uses the Perona Malik method for restoration,
    the diffusion parameter used is:
    f = 1/(1 + (s/k)^2)

    :param im: image in array form
    :param dd: parameter of the coefficient
    :param delta: parameter of the coefficient
    :param kappa: contrast parameter
    :return: the region or image after the transformation in array form
    """

    windows = generate_kern()
    nab = [ndimage.filters.convolve(im, w) for w in windows]
    gpm1 = [1 / (1 + (n / kappa) ** 2) for n in nab]
    res = [gpm1[i] * nab[i] for i in range(8)]
    im = im + delta * (sum(res))

    return im


def Perona_Malik_2(im, dd, delta, kappa):

    """
    Function which uses the Perona Malik method for restoration,
    the diffusion parameter used is:
    f = e^{-(s/K)^2}

    :param im: image in array form
    :param dd: parameter of the coefficient
    :param delta: parameter of the coefficient
    :param kappa: contrast parameter
    :return: the region or image after the transformation in array form

    """

    windows = generate_kern()
    nab = [ndimage.filters.convolve(im, w) for w in windows]
    gpm2 = [np.exp(-(n/kappa)**2) for n in nab]
    res = [gpm2[i] * nab[i] for i in range(8)]
    im = im + delta*(sum(res))

    return im

def generate_neighb_matrix(coordinate, image):

    """
    A function to get the neighbors of a given point and return a matrix of them in the form:

    M =
     __ __ __
    |u1|u2|u3|
     -- -- --
    |u4|u5|u6|
     -- -- --
    |u7|u8|u9|
     -- -- --

    it doesn't work for border points.
    :param coordinate: the coordinate of the point p[i,j] of which to obtain the matrix
    :param image: the image, in array form where to get the sub-matrix
    :return: a matrix with the neighborhood
    """

    u1 = image[coordinate[0] - 1, coordinate[1] - 1]
    u2 = image[coordinate[0], coordinate[1] - 1]
    u3 = image[coordinate[0] + 1, coordinate[1] - 1]
    u4 = image[coordinate[0] - 1, coordinate[1]]
    u5 = image[coordinate[0], coordinate[1]]
    u6 = image[coordinate[0] + 1, coordinate[1]]
    u7 = image[coordinate[0] - 1, coordinate[1] + 1]
    u8 = image[coordinate[0], coordinate[1] + 1]
    u9 = image[coordinate[0] + 1, coordinate[1] + 1]

    return np.array([[u1, u2, u3], [u4, u5, u6], [u7, u8, u9]])


def impaint_Perona_Malik(im, mask):
    """
    function for image imapinting using Perona Malik method
    :param im: image in array form
    :param mask: mask of which points are needed to be restored.
    :return: the restoration after a step of the Perona-Malik method using the diffusion parameter
    f = 1/(1 + (s/k)^2)

    """
    im_new = np.zeros(np.shape(im))
    mask = mask.astype(np.bool)
    mask_pts = np.array(np.where(mask)).T
    windows = generate_kern()
    delta = 0.1
    kappa = 15
    nab = [ndimage.filters.convolve(im, w) for w in windows]
    gpm1 = [1 / (1 + (n / kappa) ** 2) for n in nab]
    res = [gpm1[i] * nab[i] for i in range(8)]
    res = delta * sum(res)

    for mask_pt_n, mask_pt_idx in enumerate(mask_pts):
        im_new[mask_pt_idx[0], mask_pt_idx[1]] = res[mask_pt_idx[0], mask_pt_idx[1]]

    im = im + im_new
    return im

def generate_kern():

    """
    :return: a list with the kernels in array form

    """

    ker = [
    np.array([[0, 1, 0],
              [0, -1, 0],
              [0, 0, 0]]),
    np.array([[0, 0, 0],
              [0, -1, 0],
              [0, 1, 0]]),
    np.array([[0, 0, 0],
              [0, -1, 1],
              [0, 0, 0]]),
    np.array([[0, 0, 0],
              [1, -1, 0],
              [0, 0, 0]]),
    np.array([[0, 0, 1],
              [0, -1, 0],
              [0, 0, 0]]),
    np.array([[0, 0, 0],
              [0, -1, 0],
              [0, 0, 1]]),
    np.array([[0, 0, 0],
              [0, -1, 0],
              [1, 0, 0]]),
    np.array([[1, 0, 0],
              [0, -1, 0],
              [0, 0, 0]])]

    return ker



