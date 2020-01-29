"""Settings for testing FOOOF on simulated data."""

import pkg_resources

import numpy as np

###################################################################################################
###################################################################################################

# Project paths
DATA_PATH = '../data/'
FIGS_PATH = '../figures/'

# Plot settings
SAVE_EXT = '.pdf'

# Simulation Settings
F_RANGE = [2, 40]
F_RES = 0.25
F_RANGE_LONG = [1, 100]
F_RES_LONG = 0.5

# Time series simulation settings
N_SECONDS = 10
FS = 500

# Define the number of peaks and probabilities
N_PEAK_OPTS = [0, 1, 2]
N_PEAK_PROBS = [1/3, 1/3, 1/3]

# Load the distribution of center frequencies to use
CF_OPTS = np.load(pkg_resources.resource_filename(__name__, 'data/freqs.npy'))
CF_PROBS = np.load(pkg_resources.resource_filename(__name__, 'data/probs.npy'))

# Define the power and bandwidth possibilities and probabilities
PW_OPTS = [0.15, 0.20, 0.25, 0.4]
PW_PROBS = [0.25, 0.25, 0.25, 0.25]
BW_OPTS = [1.0, 2.0, 3.0]
BW_PROBS = [1/3, 1/3, 1/3]

# Define the aperiodic parameter options and probabilities
OFF_OPTS = [0]
OFF_PROBS = [1]
KNE_OPTS = [0, 10, 25, 100, 150]
KNE_PROBS = [0.2, 0.2, 0.2, 0.2, 0.2]
EXP_OPTS = [0.5, 1, 1.5, 2]
EXP_PROBS = [0.25, 0.25, 0.25, 0.25]
