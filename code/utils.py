"""Utility & helper functions for testing FOOOF on simulated data."""

from collections import Counter

import numpy as np

from fooof.analysis import get_band_peak_group

from settings import *

###################################################################################################
###################################################################################################

def print_settings(opts, probs, param):
    """Print out parameter settings."""

    print('Parameter definition for', param, '\n')
    print('\tValue \t Probability')
    for opt, prob in zip(opts, probs):
        print('\t{} \t {:2.1f}%'.format(opt, prob*100))


def print_list(lst):
    """Print out a formatted list."""

    print(['{:1.4f}'.format(item) for item in lst])


def calc_errors(truths, models, approach='abs'):
    """Calculate the error of model reconstructions with respect to ground truth.
    approach: 'abs' or 'sqrd'
    """

    if approach == 'abs':
        errors = np.abs(truths - models)
    elif approach == 'sqrd':
        errors = (truths - models)**2
    else:
        raise ValueError('Approach not understood.')

    return errors


def gen_ap_def():
    """Generator for plausible aperiodic parameters for simulated power spectra."""

    while True:

        ap_params = [None, None]

        ap_params[0] = np.random.choice(OFF_OPTS, p=OFF_PROBS)
        ap_params[1] = np.random.choice(EXP_OPTS, p=EXP_PROBS)

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


def get_ground_truth(sim_params):
    """Extract settings used to generated data (ground truth values)."""

    gauss_truths = []
    ap_truths = []

    for ind, params in enumerate(sim_params):
        gauss_truths.append([psd_params.gaussian_params for psd_params in params])
        ap_truths.append([psd_params.aperiodic_params for psd_params in params])

    gauss_truths = np.squeeze(np.array(gauss_truths))
    ap_truths = np.array(ap_truths)

    return gauss_truths, ap_truths


def get_fit_data(fgs):
    """Extract fit results fit to simulated data.
    This version extracts the single highest peak for each spectrum.
    """

    # Extract data of interest from FOOOF fits
    peak_fits = []; ap_fits = []; err_fits = []; r2_fits = []; n_peaks = []

    for fg in fgs:
        peak_fits.append(get_band_peak_group(fg.get_params('gaussian_params'), [3, 35], len(fg)))
        ap_fits.append(fg.get_params('aperiodic_params'))
        err_fits.append(fg.get_params('error'))
        r2_fits.append(fg.get_params('r_squared'))
        n_peaks.append([fres.gaussian_params.shape[0] for fres in fg])

    peak_fits = np.array(peak_fits)
    ap_fits = np.array(ap_fits)
    err_fits = np.array(err_fits)
    r2_fits = np.array(r2_fits)
    n_peaks = np.array(n_peaks)

    return peak_fits, ap_fits, err_fits, r2_fits, n_peaks


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


def count_peak_conditions(n_fit_peaks, conditions):
    """Count the number of fit peaks, across simulated conditions."""

    # Grab all flattened data for conditions
    conds = np.array([[nn] * n_fit_peaks.shape[1] for nn in conditions]).flatten()

    # Grab data for number of peaks fit
    n_fit_peaks = n_fit_peaks.flatten()

    # Collect together # simulated & # fit, for plotting
    data = []
    for aa, bb in zip(conds, n_fit_peaks):
        data.append((aa, bb))
    n_peak_counter = Counter(data)

    return n_peak_counter


def harmonic_mapping(fg):
    """Get all peaks from a FOOOFGroup and compute harmonic mapping on the CFs."""

    f_mapping = []
    for f_res in fg:
        cfs = f_res.peak_params[:, 0]
        if len(cfs) > 0:
            f_mapping.append(list(cfs / cfs[0]))

    return f_mapping
