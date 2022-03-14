#! /usr/bin/env python

import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter
from settings import imagerms, data_dir, imsize, rarange, decrange, seconds_delta
import datetime

__author__ = "Paul Hancock"
__date__ = "2022-02-24"


def make_ref(template, out=None, epoch_i=0):
    """

    :param template: Template fits file to get headers from.
    :param out: Output fits file name.
    :param epoch_i: Epoch number.
    :return:
    """
    hdulist = fits.open(template)
    header = hdulist[0].header
    header["CRVAL1"] = np.mean(rarange)
    header["CRVAL2"] = np.mean(decrange)
    header["CRPIX1"] = imsize[0] / 2
    header["CRPIX2"] = imsize[1] / 2
    header["CDELT1"] = (rarange[1] - rarange[0]) / imsize[0]
    header["CDELT2"] = (decrange[1] - decrange[0]) / imsize[1]
    # Change date-obs by seconds_delta per epoch
    template_date = datetime.datetime.strptime(header["DATE-OBS"], "%Y-%m-%dT%H:%M:%S.%f")
    new_date = template_date + epoch_i * datetime.timedelta(seconds=seconds_delta)
    header["DATE-OBS"] = new_date.strftime("%Y-%m-%dT%H:%M:%S.%f")
    del header["WSC*"]
    del header["IMAGERMS"]
    del header["ORIGIN"]
    del header["*3"]
    del header["*4"]

    data = np.random.normal(loc=0, scale=1, size=imsize)
    pixperbeam = abs(header["BMAJ"] / header["CDELT1"])
    sigma = pixperbeam / (2 * np.sqrt(2 * np.log(2)))
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


if __name__ == "__main__":
    from settings import nepochs

    for epoch_i in range(nepochs):
        make_ref("template.fits", out=f"{data_dir}/Epoch{epoch_i:02d}_noise.fits", epoch_i=epoch_i)
