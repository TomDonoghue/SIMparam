"""Plotting functions for testing FOOOF on simulated data."""

import numpy as np
from scipy.stats import sem

import seaborn as sns
import matplotlib.pyplot as plt

from settings import FIGS_PATH, SAVE_EXT

###################################################################################################
###################################################################################################

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

        save_name = FIGS_PATH + save_name + '_error' + SAVE_EXT
        plt.savefig(save_name, bbox_inches='tight')


def plot_errors_violin(data, title=None, x_axis='nlvs', y_label=None,
                       plt_log=False, ylim=None, save_fig=False, save_name=None):
    """Plots errors across distributions of fit data, as full distributions (as violin plot)."""

    fig = plt.figure(figsize=[8, 6])

    if plt_log:
        data = np.log10(data)

        # Remap any infs (coming from value 0) back to value of 0
        data[np.isinf(data)] = 0

    ax = sns.violinplot(data=data.T, cut=0, scale='area', linewidth=2.5,
                        color='#0c69ff', saturation=0.75)

    # Overlay extra dots on the median values, to make them bigger
    plt.plot([0, 1, 2, 3, 4], np.nanmedian(data, 1),
             '.', c='white', ms=20, alpha=1)

    # X-ticks & label for noise levels or # of peaks
    if x_axis == 'nlvs':
        plt.xticks([0, 1, 2, 3, 4], [0.00, 0.025, 0.050, 0.100, 0.150]);
        ax.set_xlabel('Noise Levels')
    if x_axis == 'n_peaks':
        plt.xticks([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]);
        ax.set_xlabel('Number of Peaks')

    if plt_log:
        q1, q2 = plt.yticks()
        plt.yticks(q1, [aa for aa in np.power(10, q1)]);

    if ylim is not None:
        plt.ylim(ylim)

    if title:
        ax.set_title(title)
    if not y_label:
        y_label = 'Error'
    ax.set_ylabel(y_label)

    plot_style(ax)

    if save_fig:

        save_name = FIGS_PATH + save_name + '_sim_error' + SAVE_EXT
        plt.savefig(save_name, bbox_inches='tight')


def plot_n_peaks_bubbles(data, save_fig=False):
    """Plot a comparison plot of # of peaks generated, vs. # of peaks fit."""

    fig = plt.figure(figsize=[6, 6])
    ax = plt.gca()
    for ke, va in data.items():
        plt.plot(ke[0], ke[1], '.', markersize=va/10, color='blue')
    plt.xticks(list(range(0, 5)), list(range(0, 5)));

    # Titles & Labels
    ax.set_title('Multiple Peak Fits')
    ax.set_xlabel('Number of Simulated Peaks')
    ax.set_ylabel('Number of Fit Peaks')

    # Set the plot style
    plot_style(ax)

    if save_fig:

        save_name = FIGS_PATH + 'MultiplePeakFits' + SAVE_EXT
        plt.savefig(save_name, bbox_inches='tight')


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
