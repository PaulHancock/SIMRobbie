#! /usr/bin/env python

from __future__ import print_function

import numpy as np
from MakeRefCatalogue import get_sources
from MakeLightCurves import get_transient_lc, get_lc


author = "Paul Hancock"
date = "2018-11-14"


def get_ref_cat():
    """
    Create a basic reference catalogue on the equator with a range of fluxes
    :return: array of [ra,dec,flux]
    """
    nsrc = 10
    rarange = (175, 185)
    decrange = (-5, 5)
    fluxrange = (1e-3, 1)
    cat = get_sources(rarange, decrange, fluxrange, nsrc)
    return cat


def get_catalogues(refcat, nepochs):
    """
    Use a reference catalogue to create a new set of epoch catalogues where each source has a modulation index of 0.05
    :param refcat: array of [ra,dec,flux]
    :param nepochs: number of epochs to simulate
    :return: list of [ [ra,dec,flux], ... ] one per epoch
    """
    # generate all the light curves
    lc2d = np.ones(shape=(len(refcat),nepochs))
    fluxes = refcat[:,2]
    for i, f in enumerate(fluxes):
        lc = get_lc(nepochs, f, 0.05)
        lc2d[i] = lc

    # assign one epoch of fluxes to each source
    epochs = []
    for n in range(nepochs):
        cat = refcat.copy()
        cat[:, 2] = lc2d[:, n]
        epochs.append(cat)

    return epochs


if __name__ == "__main__":
    nepochs = 3
    refcat = get_ref_cat()
    epochs = get_catalogues(refcat, nepochs)
    print(epochs)