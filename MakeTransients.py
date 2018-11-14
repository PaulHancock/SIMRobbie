#! /usr/bin/env python

from __future__ import print_function

import numpy as np

author = "Paul Hancock"
date = "2018-11-14"


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
    t = get_transient_lc(nepochs=4, flux=0.62, transient_epoch=2)
    print(t)