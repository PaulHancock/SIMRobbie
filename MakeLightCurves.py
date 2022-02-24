#! /usr/bin/env python

import numpy as np

author = "Paul Hancock"
date = "2018-11-14"


def get_norm_lc(nepochs, m):
    """
    Create a light curve with a given modulation index

    :param nepochs: Number of data points
    :param m: The modulation index
    :return:
    """
    data = np.random.normal(loc=0, scale=m, size=nepochs)
    # force std = 1
    data /= np.std(data)
    # foce std = m
    data *= m
    # force mean = 1
    data += 1 - np.mean(data)
    return data


def get_lc(nepochs, flux, m):
    """
    Generate a light curve with a given mean flux and modulation index
    :param nepohcs: Number of data points
    :param flux: Mean flux density
    :param m: Modulation index (0<= m <=1)
    :return:
    """
    return get_norm_lc(nepochs=nepochs, m=m) * flux


def get_transient_lc(nepochs, flux, transient_epoch):
    """
    Generate a light curve for a transient of given flux in a single epoch
    :param nepohcs: Number of data points
    :param flux: Transient flux
    :param transient_epoch: The epoch in which the transient occurs (0 indexed)
    :return:
    """
    lc = np.zeros(shape=nepochs)
    lc[transient_epoch] = flux
    return lc


if __name__ == "__main__":
    lc = get_lc(nepochs=15, flux=0.75, m=0.2)
    print(lc)
    print(
        "mean {0}, std {1}, m {2}".format(
            np.mean(lc), np.std(lc), np.std(lc) / np.mean(lc)
        )
    )

    t = get_transient_lc(nepochs=4, flux=0.62, transient_epoch=2)
    print(t)
