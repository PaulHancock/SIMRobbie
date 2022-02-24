#! /usr/bin/env python

import numpy as np
from settings import nsrc, rarange, decrange, fluxrange

author = "Paul Hancock"
date = "2018-11-14"


def get_positions(rarange, decrange, npoints):
    """

    :param rarange:
    :param decrange:
    :param npoints:
    :return:
    """
    # np.random.seed(seed)
    ras = np.random.uniform(rarange[0], rarange[1], size=npoints)
    decs = np.random.uniform(decrange[0], decrange[1], size=npoints)
    pos = (ras, decs)
    return pos


def get_fluxes(min, max, npoints):
    """

    :param min:
    :param max:
    :param npoints:
    :return:
    """
    fluxes = np.logspace(np.log10(min), np.log10(max), num=npoints)
    return fluxes


def get_sources(rarange, decrange, fluxrange, nsrc):
    """

    :param rarange:
    :param decrange:
    :param fluxrange:
    :param nsrc:
    :return:
    """
    ra, dec = get_positions(rarange, decrange, nsrc)
    flux = get_fluxes(fluxrange[0], fluxrange[1], nsrc)
    return np.array(list(zip(ra, dec, flux)))


if __name__ == "__main__":
    cat = get_sources(rarange, decrange, fluxrange, nsrc)
    print(cat)
