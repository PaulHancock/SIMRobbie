#! /usr/bin/env python

from astropy.table import Table
import numpy as np
from MakeRefCatalogue import get_sources
from MakeLightCurves import get_transient_lc, get_lc
from AegeanTools.catalogs import save_catalog
from AegeanTools.models import SimpleSource

from settings import (
    nepochs,
    rarange,
    decrange,
    fluxrange,
    seed,
    data_dir,
    nvar,
    ntrans,
    nnorm,
)

__author__ = "Paul Hancock"
__date__ = "2022-02-24"


def get_ref_cat():
    """
    Create a basic reference catalogue on the equator with a range of fluxes
    :return: array of [ra,dec,flux]
    """
    np.random.seed(seed)
    varcat = get_sources(rarange, decrange, fluxrange, nvar)
    normcat = get_sources(rarange, decrange, fluxrange, nnorm)
    transcat = get_sources(rarange, decrange, fluxrange, ntrans)
    cat = np.vstack((varcat, normcat, transcat))
    return cat


def get_catalogues(refcat, nepochs):
    """
    Use a reference catalogue to create a new set of epoch catalogues where each source has a modulation index of 0.05
    :param refcat: array of [ra,dec,flux]
    :param nepochs: number of epochs to simulate
    :return: list of [ [ra,dec,flux], ... ] one per epoch
    """
    np.random.seed(seed)
    # generate all the light curves
    lc2d = np.ones(shape=(len(refcat), nepochs))
    category = []
    fluxes = refcat[:, 2]

    # make variable sources
    for i, f in enumerate(fluxes[:nvar]):
        lc = get_lc(nepochs, f, 0.05)
        lc2d[i] = lc
        category.append(1)
    # make normal sources
    for i, f in enumerate(fluxes[nvar : nvar + nnorm]):
        lc2d[i + nvar] = [f] * nepochs
        category.append(0)
    # make transients
    for i, f in enumerate(fluxes[nvar + nnorm :]):
        lc2d[i + nvar + nnorm] = get_transient_lc(
            nepochs, f, np.random.randint(0, nepochs)
        )
        category.append(2)

    # assign one epoch of fluxes to each source
    epochs = []
    for n in range(nepochs):
        cat = refcat.copy()
        cat[:, 2] = lc2d[:, n]
        epochs.append(cat)

    # master input catalog
    master = np.hstack((refcat.copy(), np.array(category)[:, None], lc2d))

    return epochs, master


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
    aegean_format(refcat, f"{data_dir}/Reference_comp.fits")
    epochs, master = get_catalogues(refcat, nepochs)
    for i, ecat in enumerate(epochs):
        aegean_format(ecat, f"{data_dir}/Epoch{i:02d}_comp.fits")

    names = ["ra", "dec", "Flux_mean", "type"] + [
        f"Flux_{i:02d}" for i in range(nepochs)
    ]
    print(names)
    t = Table(data=master, names=names)
    t.write(f"{data_dir}/Reference_all.fits", overwrite=True)
