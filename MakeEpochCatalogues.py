#! /usr/bin/env python

from __future__ import print_function

import numpy as np
from MakeRefCatalogue import get_sources
from MakeLightCurves import get_transient_lc, get_lc


author = "Paul Hancock"
date = "2018-11-14"


def get_ref_cat():
    """

    :return:
    """
    nsrc = 10
    rarange = (175, 185)
    decrange = (-5, 5)
    fluxrange = (1e-3, 1)
    cat = get_sources(rarange, decrange, fluxrange, nsrc)
    return cat


def get_catalogues(refcat, nepochs):
    """

    :param refcat:
    :param nepochs:
    :return:
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