"""Utility & helper functions for testing FOOOF on simulated data."""

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


def gen_ap_def():
    """Generator for plausible aperiodic parameters for simulated power spectra."""

    while True:

        ap_params = [None, None]

        ap_params[0] = np.random.choice(OFF_OPTS, p=OFF_PROBS)
        ap_params[1] = np.random.choice(EXP_OPTS, p=EXP_PROBS)

        yield ap_params


def gen_osc_def(n_oscs_to_gen):
    """Generator for plausible oscillation parameters for simulated power spectra.

    Parameters
    ----------
    n_oscs : int, optional
        Number of oscillations to generate. If None, picked at random from {0, 1, 2}.

    Yields
    ------
    oscs : list of list of [float, float, float], or []
        Oscillation definitions.
    """

    # Generate oscillation definitions
    while True:

        oscs = []

        if n_oscs_to_gen is None:
            n_oscs = np.random.choice(N_OSCS_OPTS, p=N_OSCS_PROBS)
        else:
            n_oscs = n_oscs_to_gen

        for osc in range(n_oscs):

            cur_cen = np.random.choice(CF_OPTS, p=CF_PROBS)

            while check_duplicate(cur_cen, [it[0] for it in oscs]):
                cur_cen = np.random.choice(CF_OPTS, p=CF_PROBS)

            cur_pw = np.random.choice(PW_OPTS, p=PW_PROBS)
            cur_bw = np.random.choice(BW_OPTS, p=BW_PROBS)

            oscs.append([cur_cen, cur_pw, cur_bw])

        oscs = [item for sublist in oscs for item in sublist]

        yield oscs


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
    """Extract fit results fit to simulated data."""

    # Extract data of interest from FOOOF fits
    osc_fits = []; ap_fits = []; err_fits = []; r2_fits = []; n_oscs = []

    for fg in fgs:
        osc_fits.append(get_band_peak_group(fg.get_params('gaussian_params'), [3, 35], len(fg)))
        ap_fits.append(fg.get_params('aperiodic_params'))
        err_fits.append(fg.get_params('error'))
        r2_fits.append(fg.get_params('r_squared'))
        n_oscs.append([fres.gaussian_params.shape[0] for fres in fg])

    osc_fits = np.array(osc_fits)
    ap_fits = np.array(ap_fits)
    err_fits = np.array(err_fits)
    r2_fits = np.array(r2_fits)
    n_oscs = np.array(n_oscs)

    return osc_fits, ap_fits, err_fits, r2_fits, n_oscs


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
