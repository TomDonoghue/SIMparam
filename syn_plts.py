"""  """

import numpy as np
from scipy.stats import sem

import seaborn as sns
import matplotlib.pyplot as plt

###################################################################################################
###################################################################################################

def plot_errors(dat, title='Data', avg='mean', err='sem'):

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
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Noise Levels')
    ax.set_ylabel('Error')

    # Set the top and right side frame & ticks off
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Set linewidth of remaining spines
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)

def plot_errors_violin(dat, title=None, y_label=None):

    fig = plt.figure(figsize=[8, 6])

    ax = sns.violinplot(data=dat.T, cut=0, scale='area', color='#2a60b7', saturation=0.75)#, bw=2)

    plt.xticks([0, 1, 2, 3, 4],
               [0.0, 0.025, 0.050, 0.075, 0.100]);

    # Titles & Labels
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Noise Levels', fontsize=14)
    if not y_label:
        y_label = 'Error'
    ax.set_ylabel(y_label, fontsize=14)

    # Set the top and right side frame & ticks off
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Set linewidth of remaining spines
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
