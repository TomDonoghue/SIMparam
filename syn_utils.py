"""  """

import numpy as np

from fooof.analysis import get_band_peak_group

###################################################################################################
###################################################################################################

# Define the number of oscillation probabilities
N_OSCS_OPTS = [0, 1, 2]
N_OSCS_PROBS = [1/3, 1/3, 1/3]

# Load the distribution of center frequencies to use
CF_OPTS = np.load('freqs.npy')
CF_PROBS = np.load('probs.npy')

# Define the power and bandwidth possibilities and probabilities
AMP_OPTS = [0.15, 0.20, 0.25, 0.5]
AMP_PROBS = [0.25, 0.25, 0.25, 0.25]
BW_OPTS = [1.5, 2.5, 4]
BW_PROBS = [1/3, 1/3, 1/3]

# Define the background parameter options and probabilities
OFF_OPTS = [0]
OFF_PROBS = [1]
SL_OPTS = [0.5, 1, 1.5, 2]
SL_PROBS = [0.25, 0.25, 0.25, 0.25]

# Define the background parameter options and probabilities
OFF_OPTS = [0]
OFF_PROBS = [1]
SL_OPTS = [0.5, 1, 1.5, 2]
SL_PROBS = [0.25, 0.25, 0.25, 0.25]

###################################################################################################
###################################################################################################

def print_settings(opts, probs, param):
    """   """

    print('Parameter definition for', param, '\n')
    print('\tValue \t Probability')
    for opt, prob in zip(opts, probs):
        print('\t{} \t {:2.1f}%'.format(opt, prob*100))


def gen_bg_def():
    """Generator for plausible background parameters for synthetic power spectra. """

    while True:

        bg_params = [None, None]

        bg_params[0] = np.random.choice(OFF_OPTS, p=OFF_PROBS)
        bg_params[1] = np.random.choice(SL_OPTS, p=SL_PROBS)

        yield bg_params


def gen_osc_def(n_oscs_to_gen):
    """Generator for plausible oscillation parameters for synthetic power spectra.

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

            cur_amp = np.random.choice(AMP_OPTS, p=AMP_PROBS)
            cur_bw = np.random.choice(BW_OPTS, p=BW_PROBS)

            oscs.append([cur_cen, cur_amp, cur_bw])

        oscs = [item for sublist in oscs for item in sublist]

        yield oscs


def get_ground_truth(syn_params):
    """   """

    gauss_truths = []
    bg_truths = []

    for ind, params in enumerate(syn_params):
        gauss_truths.append([psd_params.gaussian_params for psd_params in params])
        bg_truths.append([psd_params.background_params for psd_params in params])

    gauss_truths = np.squeeze(np.array(gauss_truths))
    bg_truths = np.array(bg_truths)

    return gauss_truths, bg_truths


def get_fit_data(fgs):
    """   """

    # Extract data of interest from FOOOF fits
    osc_fits = []; bg_fits = []; err_fits = []; r2_fits = []; n_oscs = []

    for fg in fgs:
        osc_fits.append(get_band_peak_group(fg.get_all_data('gaussian_params'), [3, 40], len(fg)))
        bg_fits.append(fg.get_all_data('background_params'))
        err_fits.append(fg.get_all_data('error'))
        r2_fits.append(fg.get_all_data('r_squared'))
        n_oscs.append([fres.gaussian_params.shape[0] for fres in fg])

    osc_fits = np.array(osc_fits)
    bg_fits = np.array(bg_fits)
    err_fits = np.array(err_fits)
    r2_fits = np.array(r2_fits)
    n_oscs = np.array(n_oscs)

    return osc_fits, bg_fits, err_fits, r2_fits, n_oscs


def check_duplicate(cur_cen, all_cens, window=2):
    """Check if a candidate center frequency has already been chosen.

    Parameters
    ----------
    cur_cen : float
        xx
    all_cens : list of float
        xx
    window : int, optional
        xx

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
