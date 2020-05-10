"""Utility & helper functions for testing FOOOF on simulated data."""

import pickle

import numpy as np

from paths import DATA_PATH

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


def save_sim_data(file_name, freqs, psds,  sim_params):
    """Save out generated simulations & parameter definitions"""

    np.savez(DATA_PATH + file_name + '.npz', freqs, psds)
    with open(DATA_PATH + file_name + '.p', 'wb') as f_obj:
        pickle.dump(sim_params, f_obj)


def load_sim_data(file_name):
    """Load previously generated simulations & parameter definitions."""

    temp = np.load(DATA_PATH + file_name + '.npz')
    freqs, psds = temp['arr_0'], temp['arr_1']
    with open(DATA_PATH + file_name + '.p', 'rb') as f_obj:
        sim_params = pickle.load(f_obj)

    return freqs, psds, sim_params
