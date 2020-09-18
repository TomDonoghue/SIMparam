"""Utility & helper functions for testing FOOOF on simulated data."""

import pickle
from os.path import join as pjoin

import numpy as np

from paths import DATA_PATH

from fooof.utils.io import load_fooofgroup

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


def save_sim_data(file_name, folder, freqs, psds, sim_params):
    """Save out generated simulations & parameter definitions"""

    path_name = pjoin(DATA_PATH, folder, file_name)

    np.savez(path_name + '.npz', freqs, psds)
    with open(path_name + '.p', 'wb') as f_obj:
        pickle.dump(sim_params, f_obj)


def load_sim_data(file_name, folder):
    """Load previously generated simulations & parameter definitions."""

    path_name = pjoin(DATA_PATH, folder, file_name)

    temp = np.load(path_name + '.npz', allow_pickle=True)
    freqs, psds = temp['arr_0'], temp['arr_1']
    with open(path_name + '.p', 'rb') as f_obj:
        sim_params = pickle.load(f_obj)

    return freqs, psds, sim_params


def save_model_data(file_name, folder, fgs):
    """Save out model fit data."""

    path_name = pjoin(DATA_PATH, folder)

    for ind, fg in enumerate(fgs):
        fg.save(file_name + '_models_' + str(ind), path_name, save_results=True)


def load_model_data(file_name, folder, n_conds):
    """Load previously fit model data."""

    path_name = pjoin(DATA_PATH, folder)
    fgs = [load_fooofgroup(file_name + '_models_' + str(ind), path_name) \
        for ind in range(n_conds)]

    return fgs
