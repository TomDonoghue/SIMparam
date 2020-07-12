"""Plotting functions for testing FOOOF on simulated data."""

import numpy as np
from scipy.stats import sem

import seaborn as sns
import matplotlib.pyplot as plt

from fooof.plts.utils import check_ax

from paths import FIGS_PATH, SAVE_EXT
from settings import NLVS, N_PEAKS, KNEES, SKEWS, RDSYMS

###################################################################################################
###################################################################################################

def get_ax():
    """Helper function for sizing plots"""

    return check_ax(None, figsize=(6, 5))


def plot_single_data(data, title=None, ylabel='Error', ax=None, save_fig=False, save_name=None):
    """Plot a single vector of data in 1-dimensional scatter plot."""

    if not ax:
        _, ax = plt.subplots(figsize=[2, 4])

    ax.plot(np.ones(len(data)), data, '.', markersize=12)

    ax.set_xticks([])
    ax.set_ylabel(ylabel)

    if ylabel == 'Error':
        ax.set_ylim([0, max(data)+0.10*max(data)])

    if title:
        ax.set_title(title)

    plot_style(ax)

    if save_fig:

        save_name = FIGS_PATH + save_name + SAVE_EXT
        plt.savefig(save_name, bbox_inches='tight')


def plot_errors(data, title='Data', avg='mean', err='sem', save_fig=False, save_name=None):
    """Plots errors across distributions of fit data, as central tendency & an error bar."""

    n_groups = len(data)

    fig = plt.figure(figsize=[4, 5])
    ax = plt.gca()

    if avg == 'mean':
        avg_func = np.nanmean
    if avg == 'median':
        avg_func = np.nanmedian

    if err == 'sem': err_func = sem

    plt.errorbar(np.arange(1, n_groups+1), avg_func(data, 1),
                 xerr=None, yerr=err_func(data, 1), markersize=22,
                 fmt='.', capsize=10, elinewidth=2, capthick=2)

    ax.set_xlim([0.5, n_groups+0.5])

    # Titles & Labels
    ax.set_title(title)
    ax.set_xlabel('Noise Levels')
    ax.set_ylabel('Error')

    # Set plot style
    plot_style(ax)

    if save_fig:

        save_name = FIGS_PATH + save_name + SAVE_EXT
        plt.savefig(save_name, bbox_inches='tight')


def plot_errors_violin(data, title=None, x_axis='nlvs', y_label=None, yticks=None,
                       plt_log=False, ylim=None, ax=None, save_fig=False, save_name=None):
    """Plots errors across distributions of fit data, as full distributions (as violin plot)."""

    if not ax:
        fig = plt.figure(figsize=[8, 6])

    if plt_log:

        # Log data & remap any infs (coming from value 0) back to value of 0
        data = np.log10(data)
        data[np.isinf(data)] = 0

    # Create the violinplot
    ax = sns.violinplot(data=data.T, cut=0, scale='area', linewidth=2.5,
                        color='#0c69ff', saturation=0.75, ax=ax)

    # Overlay extra dots on the median values, to make them bigger
    ax.plot(np.arange(0, data.shape[0]), np.nanmedian(data, 1),
            '.', c='white', ms=20, alpha=1)

    # X-ticks & label for noise levels or # of peaks
    ax.set_xticks(np.arange(0, data.shape[0]))
    if x_axis == 'nlvs':
        ax.set_xticklabels(NLVS)
        ax.set_xlabel('Noise Levels')
    elif x_axis == 'n_peaks':
        ax.set_xticklabels(N_PEAKS);
        ax.set_xlabel('Number of Peaks')
    elif x_axis == 'knees':
        ax.set_xticklabels(KNEES)
        ax.set_xlabel('Knee Value')
    elif x_axis == 'skew':
        ax.set_xticklabels(SKEWS)
        ax.set_xlabel('Skew Value')
    elif x_axis == 'rdsym':
        ax.set_xticklabels(RDSYMS)
        ax.set_xlabel('Oscillation Asymmetry')
    elif x_axis is None:
        ax.set_xticks([])
    else:
        raise ValueError('x_axis setting not understood.')

    if plt_log:

        # Update the label representation
        cur_tick_locs = ax.get_yticks()
        cur_tick_labels = ax.get_yticklabels()
        ytick_locs = cur_tick_locs if not yticks else np.log10(yticks)
        ytick_labels = np.power(10, cur_tick_locs) if not yticks else yticks
        ax.set_yticks(ytick_locs)
        ax.set_yticklabels(ytick_labels)

    if ylim is not None:
        ax.set_ylim(ylim)

    if title:
        ax.set_title(title)
    if not y_label:
        y_label = 'Error'
    ax.set_ylabel(y_label)

    plot_style(ax)

    if save_fig:

        save_name = FIGS_PATH + save_name + SAVE_EXT
        plt.savefig(save_name, bbox_inches='tight')


def plot_n_peaks_bubbles(data, ms_val=10, x_label='n_peaks', save_fig=False, save_name=None):
    """Plot a comparison plot of # of peaks generated, vs. # of peaks fit.

    data : Counter object
    """

    fig = plt.figure(figsize=[6, 6])
    ax = plt.gca()

    # Create a mapping between condition label and ordinal label for the plt
    conds = {val : ind for ind, val in \
             enumerate(sorted(set([val[0] for val in data.keys()])))}

    # Add data to the plot, plotting as the size of the plotted circle
    for ke, va in data.items():
        plt.plot(conds[ke[0]], ke[1], '.', markersize=va/ms_val, color='blue')

    # Label with x-axis with labels using condition labels at ordinal locations
    plt.xticks(list(conds.values()), list(conds.keys()))

    # Titles & Labels
    ax.set_title('Multiple Peak Fits')
    ax.set_ylabel('Number of Fit Peaks')
    if x_label == 'n_peaks':
        ax.set_xlabel('Number of Simulated Peaks')
    elif x_label == 'nlvs':
        ax.set_xlabel('Noise Levels')
    elif x_label == 'knee':
        ax.set_xlabel('Knee Value')
    elif x_label == 'skew':
        ax.set_xlabel('Peak Skew Value')
    elif x_label == 'rdsym':
        ax.set_xlabel('Oscillation Asymmetry')
    else:
        raise ValueError('x_label setting not understood.')

    ticks = list(set([val[1] for val in data.keys()]))
    ax.set_yticks(ticks)
    ax.set_yticklabels(ticks)

    # Set the plot style
    plot_style(ax)

    if save_fig:

        save_name = FIGS_PATH + save_name + SAVE_EXT
        plt.savefig(save_name, bbox_inches='tight')


def plot_harmonics(data, title=None, ax=None):
    """Create a scatter of harmonic frequency mapping."""

    if not ax:
        _, ax = plt.subplots(figsize=[2, 4])

    # Create x-axis data, with small jitter for visualization purposes
    x_data = np.ones_like(data) + np.random.normal(0, 0.025, data.shape)

    # Plot the data
    ax.scatter(x_data, data, s=36, alpha=0.5)

    # Sort out ticks
    ax.set_xticks([1])
    ax.set_yticks([2, 3])
    ax.set_xticklabels(["Peaks"], {'fontsize' : 12})
    ax.set_yticklabels(["f-1", "f-2"], {'fontsize' : 12})

    # Set plot limits
    ax.set_xlim([0.9, 1.1])
    ax.set_ylim([1, 3.2])

    # Add title, if provided
    if title:
        ax.set_title(title)

    plot_style(ax)


#### PLOT STYLING ####

def plot_style(ax):
    """Set the aesthetic styling for a plot."""

    # Set word sizes
    ax.title.set_size(20)
    ax.xaxis.label.set_size(16)
    ax.yaxis.label.set_size(16)
    ax.tick_params(axis='both', which='major', labelsize=14)

    # Set the top and right side frame & ticks off
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Set linewidth of remaining spines
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
