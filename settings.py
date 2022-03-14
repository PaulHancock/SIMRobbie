#! python
__author__ = "Paul Hancock"
__date__ = "2022-02-24"

seed = 20181126  # Seed for random number generator
nepochs = 25  # Total number of epochs to generate
nsrc = 1100  # Total number of sources to generate
nvar = 500  # Number of sources which are variable (flux varies between epochs)
ntrans = 100  # Number of sources which are transient (present in only a single epoch)
nnorm = 500  # Number of persistent sources (no change between epochs)
rarange = (150, 157)  # The range of RA over which to simulate the sources (Degrees)
decrange = (-15, -10)  # The range of Dec over which to simulate the sources (Degrees)
imsize = (1001, 1001)  # The size of the image in pixels
fluxrange = (5e-3, 1)  # The min/max flux of sources in Jy
imagerms = 5e-3  # Individual epoch image rms in Jy
data_dir = "data"  # The directory in which the simulated files will be stored
seconds_delta = 120 # Seconds to separate each epoch by