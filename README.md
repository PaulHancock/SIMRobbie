# Description
This repository was created in order to generate a set of test images for [Robbie](https://github.com/PaulHancock/Robbie).
The images contain a population of persistent sources, variable sources, and transient sources.

[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://www.python.org/downloads/release/)

## Simulation settings
The parameters of the simulation can be set in `settings.py`.
The default parameters and a description are shown below:
```
seed = 20181126       # Seed for random number generator
nepochs = 25          # Total number of epochs to generate
nsrc = 1100           # Total number of sources to generate
nvar = 500            # Number of sources which are variable (flux varies between epochs)
ntrans = 100          # Number of sources which are transient (present in only a single epoch)
nnorm = 500           # Number of persistent sources (no change between epochs)
rarange = (173, 187)  # The range of RA over which to simulate the sources (Degrees)
decrange = (-7, 7)    # The range of Dec over which to simulate the sources (Degrees)
fluxrange = (5e-3, 1) # The min/max flux of sources in Jy
imagerms = 5e-3       # Individual epoch image rms in Jy
data_dir = "data"     # The directory in which the simulated files will be stored
```

## Data products

All the data will be stored in the `data_dir` as specified in `settings.py`.
The following files are created:

- Epoch??.fits
  - Simulated image for this epoch
- Epoch??_nois.fits
  - Source free image for this epcoch (just nosie)
- Epoch??_comp_simp.fits
  - Catalogue of sources for this epoch
- Reference_comp_sim.fits
  - The reference catalogue with ra/dec and mean flux for each source
- Reference_all.fits
  - The reference catalogue with ra/dec for each source and the flux in each epoch.
- square.mim, square.reg
  - MIMAS and DS9 format region files for the area of interest.
  - Not used in the simulation, but may be useful for visulatisation


## How2Run
- Modify `settings.py` or use the default
- Run `./MakeEpochImages.sh`
- ?
- Profit


## Credit
If you make use of Robbie or SIMRobbie as part of your work please cite [Hancock et al. 2018](http://adsabs.harvard.edu/abs/2019A%26C....27...23H), and link to this repository.