#! /usr/bin/env python

from __future__ import print_function

import numpy as np
from MakeRefCatalogue import get_sources
from MakeLightCurves import get_transient_lc, get_lc
from AegeanTools.catalogs import save_catalog
from AegeanTools.models import SimpleSource

from settings import nepochs, nsrc, rarange, decrange, fluxrange

author = "Paul Hancock"
date = "2018-11-19"


def get_ref_cat():
    """
    Create a basic reference catalogue on the equator with a range of fluxes
    :return: array of [ra,dec,flux]
    """
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
    lc2d = np.ones(shape=(len(refcat), nepochs))
    fluxes = refcat[:, 2]
    for i, f in enumerate(fluxes):
        # all light curves have some variability in them
        lc = get_lc(nepochs, f, 0.05)
        lc2d[i] = lc
        # 0.1% of sources are transient
        if np.random.rand() < 0.001:
            lc2d[i] = get_transient_lc(nepochs, f, np.random.randint(0, nepochs))

    # assign one epoch of fluxes to each source
    epochs = []
    for n in range(nepochs):
        cat = refcat.copy()
        cat[:, 2] = lc2d[:, n]
        epochs.append(cat)

    return epochs


def aegean_format(catalogue, out):
    """
    Save a catalogue in a format that Aegean will recognize
    :param catalogue: Catalogue
    :param out: Output filename
    :return:
    """
    sources = []
    for i, c in enumerate(catalogue):
        src = SimpleSource()
        src.ra, src.dec, src.peak_flux = c
        src.uuid = "injected_{0:04d}".format(i)
        src.pa = 0
        src.a = src.b = 0.0326580516349937 * 3600
        sources.append(src)
    save_catalog(out, sources)
    print("Wrote to file {0}".format(out))
    return


if __name__ == "__main__":
    refcat = get_ref_cat()
    aegean_format(refcat, 'Reference.fits')
    epochs = get_catalogues(refcat, nepochs)
    for i, ecat in enumerate(epochs):
        aegean_format(ecat, 'Epoch{0:02d}_comp.fits'.format(i))

