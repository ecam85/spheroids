"""

ecam Jan20

Basic access and exploration routines

"""

from PIL import Image
import numpy as np
from scipy.stats import lognorm
import multiprocessing as mp
import csv


def get_image(im):
    return Image.open(im)

def get_red(im):
    img = get_image(im)
    return img.getchannel("R")

def get_green(im):
    img = get_image(im)
    return img.getchannel("G")

def get_blue(im):
    img = get_image(im)
    return img.getchannel("B")

def get_ared(im):
    return np.ravel(np.array(get_red(im)))

def get_agreen(im):
    return np.ravel(np.array(get_green(im)))

def get_ared_crop(im):
    return np.ravel(np.array(get_red(im))[:998,:])

def get_agreen_crop(im):
    return np.ravel(np.array(get_green(im))[:998,:])


def get_ablue(im):
    return np.ravel(np.array(get_blue(im)))

def rg_hist(im):
    """
    histogram of red-green channels

    returns a 256x256 array, where rows are green values and columns are red
    """
    hist = np.zeros((256,256))

    ared,agreen = get_ared(im),get_agreen(im)

    #TODO this can be done without splitting colors in advance.
    for r,g in zip(ared,agreen):
        hist[g,r] += 1

    return hist

def r_values_given_g(im,g=150):
    """
    list of red values in pixels with green = g
    """ 
    ared,agreen = get_ared(im),get_agreen(im) 
    return np.array([ r for r,gg in zip(ared,agreen) if gg==g ] )

def red_given_g(im,g=150):
    """
    as before, normalized to 0,1
    """ 
    ared,agreen = get_ared(im),get_agreen(im) 
    return np.array([ r for r,gg in zip(ared,agreen) if gg==g ] )/255.
