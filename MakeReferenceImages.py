#! /usr/bin/env python

from __future__ import print_function

import numpy as np
import astropy
from astropy.io import fits
import scipy
from scipy.ndimage.filters import gaussian_filter
from settings import imagerms

author = "Paul Hancock"
date = "2018-11-15"

def make_ref(template, out=None):
    """

    :param template:
    :return:
    """
    hdulist = fits.open(template)
    header = hdulist[0].header
    header['CRVAL1'] = 180
    header['CRVAL2'] = 0
    header['CRPIX1'] = 1001
    header['CRPIX2'] = 1001
    del header['WSC*']
    del header['IMAGERMS']
    del header['ORIGIN']
    del header['*3']
    del header['*4']

    data = np.random.normal(loc=0, scale=1, size=(2000, 2000))
    pixperbeam = abs(header['BMAJ'] / header['CDELT1'])
    sigma = pixperbeam / (2*np.sqrt(2*np.log(2)))
    data = gaussian_filter(data, sigma=sigma)
    # zero mean
    data -= np.mean(data)
    # rms =1
    data /= np.std(data)
    # rms = imagerms
    data *= imagerms
    hdulist = fits.PrimaryHDU(data=data, header=header)
    if out is not None:
        hdulist.writeto(out, overwrite=True)
    return hdulist


if __name__ == '__main__':
    from settings import nepochs
    for i in range(nepochs):
        make_ref('template.fits', out='Epoch{0:02d}_noise.fits'.format(i))