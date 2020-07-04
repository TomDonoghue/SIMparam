"""Analysis functions for testing FOOOF on simulated data."""

from collections import Counter

import numpy as np

from fooof.analysis import get_band_peak_fg

###################################################################################################
###################################################################################################

def calc_errors(truths, models, approach='abs'):
    """Calculate the error of model reconstructions with respect to ground truth.

    Error metrics available in `approach`: {'abs', 'sqrd'}
    """

    if approach == 'abs':
        errors = np.abs(truths - models)
    elif approach == 'sqrd':
        errors = (truths - models)**2
    else:
        raise ValueError('Approach not understood.')

    return errors


def get_ground_truth(sim_params):
    """Extract settings used to generated data (ground truth values)."""

    pe_truths = []
    ap_truths = []

    for ind, params in enumerate(sim_params):
        pe_truths.append([psd_params.periodic_params for psd_params in params])
        ap_truths.append([psd_params.aperiodic_params for psd_params in params])

    pe_truths = np.squeeze(np.array(pe_truths))
    ap_truths = np.array(ap_truths)

    return pe_truths, ap_truths


def get_fit_data(fgs, f_range=[3, 35]):
    """Extract fit results fit to simulated data."""

    # Extract data of interest from FOOOF fits
    peak_fits = []; ap_fits = []; err_fits = []; r2_fits = []; n_peaks = []

    for fg in fgs:
        peak_fits.append(get_band_peak_fg(fg, f_range, attribute='gaussian_params'))
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
