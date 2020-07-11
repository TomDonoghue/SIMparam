"""Settings for testing FOOOF on simulated data."""

import pkg_resources

import numpy as np

from fooof.data import FOOOFSettings

###################################################################################################
###################################################################################################

## PROJECT SETTINGS

# Set up list of folder names
FOLDER_NAMES = ['01_one-peak', '02_multi-peak', '03_knee',
                '04_mv-ap', '05_mv-peI', '06_mv-peII']

## FOOOF SETTINGS

FOOOF_SETTINGS = FOOOFSettings(
    peak_width_limits=[1, 8],
    max_n_peaks=6,
    min_peak_height=0.1,
    peak_threshold=2.0,
    aperiodic_mode='fixed')

FOOOF_SETTINGS_KNEE = FOOOFSettings(
    peak_width_limits=[1, 8],
    max_n_peaks=6,
    min_peak_height=0.1,
    peak_threshold=2.0,
    aperiodic_mode='knee')

## POWER SPECTRUM SIMULATIONS

# Set the number of power spectra (per condition)
N_PSDS = 1000

# Simulation Settings
F_RANGE = [2, 40]
F_RES = 0.25
F_RANGE_LONG = [1, 100]
F_RES_LONG = 0.5

# Set the condition values
NLVS = [0.0, 0.025, 0.050, 0.10, 0.15]
N_PEAKS = [0, 1, 2, 3, 4]
KNEES = [0, 1, 10, 25, 100]
RDSYMS = [0.5, 0.625, 0.75, 0.875, 1.0]
SKEWS = [0, 5, 10, 25, 50]

# Set the default noise levels
NLV = 0.01

# Define the number of peaks options and probabilities
N_PEAK_OPTS = [0, 1, 2]
N_PEAK_PROBS = [1/3, 1/3, 1/3]

# Load the distribution of center frequencies to use
CF_OPTS = np.load(pkg_resources.resource_filename(__name__, 'data/freqs.npy'))
CF_PROBS = np.load(pkg_resources.resource_filename(__name__, 'data/probs.npy'))

# Define the power and bandwidth options and probabilities
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

## TIME SERIES SIMULATIONS

# Time series simulation settings
N_SECONDS = 10
FS = 500

## PLOTTING

# Plot limits
YLIMS_AP = [-5.75, 0.]
YLIMS_KN = np.log10([0.00075, 10000])
YLIMS_CF = [-5.2, 1.75]
YLIMS_PW = [-4.25, 0]
YLIMS_BW = [-2.9, 0.6]

YTICKS_CF = [0.0001, 0.001, 0.01, 0.1, 1, 10]
YTICKS_PW = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10]
YTICKS_BW = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10]
