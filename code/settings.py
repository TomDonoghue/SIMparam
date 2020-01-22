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

# Define the number of oscillation probabilities
N_OSCS_OPTS = [0, 1, 2]
N_OSCS_PROBS = [1/3, 1/3, 1/3]

# Load the distribution of center frequencies to use
CF_OPTS = np.load(pkg_resources.resource_filename(__name__, 'data/freqs.npy'))
CF_PROBS = np.load(pkg_resources.resource_filename(__name__, 'data/probs.npy'))

# Define the power and bandwidth possibilities and probabilities
PW_OPTS = [0.15, 0.20, 0.25, 0.4]
PW_PROBS = [0.25, 0.25, 0.25, 0.25]
BW_OPTS = [1.0, 2.0, 3.0]
BW_PROBS = [1/3, 1/3, 1/3]

# Define the background parameter options and probabilities
OFF_OPTS = [0]
OFF_PROBS = [1]
EXP_OPTS = [0.5, 1, 1.5, 2]
EXP_PROBS = [0.25, 0.25, 0.25, 0.25]
