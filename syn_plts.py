"""Plotting functions for Synthetic FOOOF testing."""

import numpy as np
from scipy.stats import sem

import seaborn as sns
import matplotlib.pyplot as plt

###################################################################################################
###################################################################################################

def plot_errors(dat, title='Data', avg='mean', err='sem'):
    """Plots errors across distributions of fit data, as central tendency & an error bar."""

    n_groups = len(dat)

    fig = plt.figure(figsize=[4, 5])
    ax = plt.gca()

    if avg == 'mean': avg_func = np.nanmean
    if avg == 'median': avg_func = np.nanmedian

    if err == 'sem': err_func = sem

    plt.errorbar(np.arange(1, n_groups+1), avg_func(dat, 1), yerr=err_func(dat, 1), xerr=None, fmt='.',
                 markersize=22, capsize=10, elinewidth=2, capthick=2)

    ax.set_xlim([0.5, n_groups+0.5])

    # Titles & Labels
    ax.set_title(title)
    ax.set_xlabel('Noise Levels')
    ax.set_ylabel('Error')

    # Set plot style
    plot_style(ax)


def plot_errors_violin(dat, title=None, x_axis='nlvs', y_label=None, save_fig=False, save_name=None):
    """Plots errors across distributions of fit data, as full distributions (as violin plot)."""

    fig = plt.figure(figsize=[8, 6])

    ax = sns.violinplot(data=dat.T, cut=0, scale='area', linewidth=2.5, color='#0c69ff', saturation=0.75)

    # X-ticks & label for noise levels or # of peaks
    if x_axis == 'nlvs':
        plt.xticks([0, 1, 2, 3, 4], [0.00, 0.025, 0.050, 0.100, 0.150]);
        ax.set_xlabel('Noise Levels')
    if x_axis == 'n_oscs':
        plt.xticks([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]);
        ax.set_xlabel('Number of Peaks')

    # Titles & Labels
    if title:
        ax.set_title(title)
    if not y_label:
        y_label = 'Error'
    ax.set_ylabel(y_label)

    ## Aesthetics
    plot_style(ax)

    if save_fig:

        save_name = 'plts/' + save_name + '_syn_error.pdf'
        plt.savefig(save_name, bbox_inches='tight', dpi=300)


def plot_n_oscs_bubbles(dat, save_fig=False):
    """Plot a comparison plot of # of peaks generated, vs. # of peaks fit."""

    fig = plt.figure(figsize=[6, 6])
    ax = plt.gca()
    for ke, va in dat.items():
        plt.plot(ke[0], ke[1], '.', markersize=va/10, color='blue')
    plt.xticks(list(range(0, 5)), list(range(0, 5)));

    # Titles & Labels
    ax.set_title('Multiple Peak Fits')
    ax.set_xlabel('Number of Simulated Peaks')
    ax.set_ylabel('Number of Fit Peaks')

    # Set the plot style
    plot_style(ax)

    if save_fig:

        save_name = 'plts/MultiplePeakFits.pdf'
        plt.savefig(save_name, bbox_inches='tight', dpi=300)


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
