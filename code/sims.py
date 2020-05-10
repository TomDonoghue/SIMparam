"""Simulation functions for testing FOOOF on simulated data."""

import numpy as np
from scipy import stats

from fooof.sim.gen import gen_aperiodic, gen_periodic, gen_noise

from settings import *

###################################################################################################
###################################################################################################

def gen_ap_def():
    """Generator for plausible aperiodic parameters for simulated power spectra."""

    while True:

        ap_params = [None, None]

        ap_params[0] = np.random.choice(OFF_OPTS, p=OFF_PROBS)
        ap_params[1] = np.random.choice(EXP_OPTS, p=EXP_PROBS)

        yield ap_params


def gen_ap_knee_def(knee_val):
    """Generator for plausible aperiodic parameters, with a knee value, for simulated power spectra."""

    while True:

        ap_params = [None, knee_val, None]

        ap_params[0] = np.random.choice(OFF_OPTS, p=OFF_PROBS)
        ap_params[2] = np.random.choice(EXP_OPTS, p=EXP_PROBS)

        yield ap_params


def gen_ap_kn_def():
    """Generator for plausible aperiodic parameters, with knees, for simulated power spectra."""

    while True:

        ap_params = [None, None, None]

        ap_params[0] = np.random.choice(OFF_OPTS, p=OFF_PROBS)
        ap_params[1] = np.random.choice(KNE_OPTS, p=KNE_PROBS)
        ap_params[2] = np.random.choice(EXP_OPTS, p=EXP_PROBS)

        yield ap_params


def gen_peak_def(n_peaks_to_gen):
    """Generator for plausible peak parameters for simulated power spectra.

    Parameters
    ----------
    n_peaks_to_gen : int, optional
        Number of peaks to generate. If None, picked at random from {0, 1, 2}.

    Yields
    ------
    peaks : list of list of [float, float, float], or []
        Peak definitions.
    """

    # Generate peak definitions
    while True:

        peaks = []

        if n_peaks_to_gen is None:
            n_peaks = np.random.choice(N_PEAK_OPTS, p=N_PEAK_PROBS)
        else:
            n_peaks = n_peaks_to_gen

        for peak in range(n_peaks):

            cur_cen = np.random.choice(CF_OPTS, p=CF_PROBS)

            while check_duplicate(cur_cen, [it[0] for it in peaks]):
                cur_cen = np.random.choice(CF_OPTS, p=CF_PROBS)

            cur_pw = np.random.choice(PW_OPTS, p=PW_PROBS)
            cur_bw = np.random.choice(BW_OPTS, p=BW_PROBS)

            peaks.append([cur_cen, cur_pw, cur_bw])

        peaks = [item for sublist in peaks for item in sublist]

        yield peaks


def check_duplicate(cur_cen, all_cens, window=2):
    """Check if a candidate center frequency is too close to an existing one.

    Parameters
    ----------
    cur_cen : float
        Candidate center frequency to check.
    all_cens : list of float
        List of all existing center frequencies.
    window : int, optional, default: 2
        Window, in Hz, around existing peak around which new peaks cannot be added.

    Returns
    -------
    bool
        Whether the candidate center frequency is already included.
    """

    if len(all_cens) == 0:
        return False
    for cen in all_cens:
        if cur_cen >= cen-window and cur_cen <= cen+window:
            return True

    return False


def gen_skew_peak(freqs, cen, height, scale, skew):
    """Generate a skewed peak.

    Parameters
    ----------
    freqs : 1d array
        Frequency vector to create peak values from.
    cen : float
        Center of the peak. Equivalent to the center frequency.
    height : float
        Height of the peak. Equivalent to the power.
    scale : float
        Width of the peak. Equivalent to the bandwidth.
    skew : float
        Skewness of the peak. Has no equivalent in symmetric peaks.

    Returns
    -------
    ys : 1d array
        Values that define the skewed peak.

    Notes
    -----
    Asymetric peaks parameters are organized as [CEN, HEIGHT, SCALE, SKEW]
    This is done to match the layout of (symmetric) peak parameters.
    """

    ys = stats.skewnorm.pdf(freqs, skew, cen, scale)

    # Scale to (0, 1), then apply power transform
    ys = (ys / np.abs(ys).max()) * height

    return ys


def gen_skew_peaks(freqs, params):
    """Generate skewed peaks.

    Parameters
    ----------
    freqs : 1d array
        Frequency vector to create peak values from.
    params : list of list of float
        Parameter definition(s) for the skewed peak(s).
        Length of params is number of peaks
        Each embedded list should be length 4, as [cen, height, scale, skew].

    Returns
    -------
    ys : 1d array
        Values that define the skewed peak(s).

    Notes
    -----
    Asymetric peaks parameters are organized as [CEN, HEIGHT, SCALE, SKEW]
    This is done to match the layout of (symmetric) peak parameters.
    """

    ys = np.zeros_like(freqs)

    for cur_params in params:
        ys = ys + gen_skew_peak(freqs, *cur_params)

    return ys


def gen_power_vals_fn(freqs, ap_kwargs, pe_kwargs, noise_kwargs,
                      ap_func=gen_aperiodic,
                      pe_func=gen_periodic,
                      noise_func=gen_noise):
    """Generate a simulated power spectrum, using the specified functions & parameters.

    Parameters
    ----------
    freqs : 1d array
        Frequency vector to create peak values from.
    ap_kwargs, pe_kwargs, noise_kwargs : dict
        Dictionaries of parameters for the aperiodic, periodic, and noise components.
    ap_func, pe_func, noise_func : callable
        Functions that define the aperiodic, periodic and noise components.

    Returns
    -------
    powers : 1d array
        Simulated values for the power spectrum.

    # Note: possible ToDo item: make group version of the gen_power_vals function.
    """

    aperiodic = ap_func(freqs, **ap_kwargs)
    peaks = pe_func(freqs, **pe_kwargs)
    noise = noise_func(freqs, **noise_kwargs)

    powers = np.power(10, aperiodic + peaks + noise)

    return powers
