# Dependencies
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import pandas as pd
import numpy as np
#from matplotlib.axes._subplots import AxesSubplot

from matplotlib import rc, rcParams
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator, FixedLocator, FixedFormatter
rc('xtick', labelsize=15) 
rc('ytick', labelsize=15) 
rc("lines", markeredgewidth=2.0)
rc("axes", linewidth=2.0)
rc('font', family='serif')
rcParams["font.size"] = 15
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'


from typing import Literal, Optional

from .aggregation import compute_gradepyramid
from .extraction import create_ordinalcats_ascensions

def plot_gradepyramid(df: pd.DataFrame, 
                      aggtype: Literal['sum', 'count'] = 'sum',
                      gradesystem: Literal['french', 'usa'] = 'french',
                      ax = None, 
                      legend: bool = False):
    """
    Plot the grade pyramid as a matplotlib figure.
    """

    # Compute the grade pyramid
    pyrm = compute_gradepyramid(df, aggtype=aggtype, gradesystem=gradesystem)

    # Determine the grade column
    gradecol = 'grade_{}'.format(gradesystem)

    # Perform bookkeeping
    ascensions = create_ordinalcats_ascensions()
    category_colors = plt.get_cmap('viridis')(np.linspace(0.0, 1., len(ascensions.categories)))
    labels = pyrm[gradecol]

    # Create a figure in case it was not specified
    if ax == None:
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)
    
    # Draw the grade pyramid (as a horizonal bar chart with annotations)
    for aa, color in zip(ascensions.categories, category_colors):
        # Subset the pyramid data to one ascension type
        data = pyrm[pyrm['ascension_type'] == aa]
        
        widths = data['sends']
        starts = data['sends_cumsum'] - widths
        
        # Actual plotting
        ax.barh(data[gradecol], widths, left=starts, height=0.85,
                label=aa, color=color, edgecolor='k')
        
        xcenters = starts + widths / 2
        
        # Get the colors our to determine annotation color
        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            if c != int(0):
                ax.text(x, y, str(int(c)), ha='center', va='center',
                        color=text_color)
    
    # Make the figure meaningful   
    if legend:
        ax.legend(ncol=len(ascensions.categories),
                  bbox_to_anchor=(0, 1),
                  loc='lower left', fontsize='large')
    
    ax.set_xlabel('Total routes climbed', fontsize='large')
    ax.set_ylabel('Climbing grade ({} system)'.format(gradesystem), fontsize='large')
    
    if gradesystem == 'french':
        ax.set_ylim(['4c', '7c'])
    elif gradesystem == 'usa':
        ax.set_ylim(['5.7', '5.13a'])
    
    ax.set_xlim([0, pyrm['sends_cumsum'].max() + 2])
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    
    return ax

def plot_doublegradepyramid(df: pd.DataFrame, 
                            aggtype: Literal['sum', 'count'] = 'sum',
                            gradesystem: Literal['french', 'usa'] = 'french',
                            ):
    """
    Plot the grade pyramid as a matplotlib figure for both toprope and lead climbing.
    """

    # Create the matplotlib figure
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    fig.subplots_adjust(wspace=0)

    # Populate the figure
    ax1 = plot_gradepyramid(df[df['style'] == 'lead'], aggtype=aggtype, gradesystem=gradesystem, ax=ax1)
    ax2 = plot_gradepyramid(df[df['style'] == 'toprope'], aggtype=aggtype, gradesystem=gradesystem, ax=ax2)

    # Needed for additional metrics
    pyrmlead = compute_gradepyramid(df[df['style'] == 'lead'], aggtype=aggtype, gradesystem=gradesystem)
    pyrmtop = compute_gradepyramid(df[df['style'] == 'toprope'], aggtype=aggtype, gradesystem=gradesystem)

    # Beautify the figure
    ax1.invert_xaxis()
    ax1.set_title('Lead climbing - {} routes'.format(pyrmlead['sends'].sum()))
    ax2.set_title('Toprope climbing - {} routes'.format(pyrmtop['sends'].sum()))

    ax2.yaxis.set_label_position('right')
    ax2.yaxis.tick_right()

    ax2.legend(ncol=len(create_ordinalcats_ascensions().categories),
            bbox_to_anchor=(0, -0.12),
            loc='best', fontsize='large')

    xmax = max([ax1.get_xlim()[1], ax2.get_xlim()[1]])
    ax1.set_xlim([xmax, 0]); ax2.set_xlim([0, xmax])

    ax1.xaxis.set_major_locator(MultipleLocator(5))
    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    
    ax2.xaxis.set_major_locator(MultipleLocator(5))
    ax2.xaxis.set_minor_locator(MultipleLocator(1))

    return fig

