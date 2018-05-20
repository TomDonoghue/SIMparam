"""  """

import numpy as np

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

            while _check_duplicate(cur_cen, [it[0] for it in oscs]):
                cur_cen = np.random.choice(CEN_FREQS, p=PROBS)

            cur_amp = np.random.choice(AMP_OPTS, p=AMP_PROBS)
            cur_bw = np.random.choice(BW_OPTS, p=BW_PROBS)

            oscs.append([cur_cen, cur_amp, cur_bw])

        oscs = [item for sublist in oscs for item in sublist]

        yield oscs


def _check_duplicate(cur_cen, all_cens, window=1):
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
    for ch in range(cur_cen-window, cur_cen+window+1):
        if ch in all_cens:
            return True

    return False
