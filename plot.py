import numpy as np
import matplotlib.pyplot as plt

def approximate_mesh(deg1, deg2=None, vals=[], zones=[], filedir=None, filename=None):
    fig,ax = plt.subplots(figsize=(12,4))
    if not deg2:
        deg2 = deg1
    for x in range(deg2):
        s = np.sin(x)
        if x <= deg1:
            # Plot coarser approximates
            colorstyle = 'tab:orange'
            h = 1.
            ax.annotate(str(x), (s,1.1), horizontalalignment="center", verticalalignment="center")
        else:
            # Plot finer approximates
            colorstyle = 'b'
            h = .8
        ax.plot((s,s), (-h,h), colorstyle)
    # Plot particular values
    for val in vals:
        s = np.sin(val)
        ax.plot((s,s), (-0.6,0.6), 'darkgoldenrod')
        ax.annotate(str(val), (s,0.7), horizontalalignment="center", verticalalignment="center")
    # Manage plot
    ax.set_xlim(left=-1.,right=1.)
    ax.set_ylim(bottom=-1.2,top=1.2)
    ax.set_yticks([])
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_position('center')
    # Shade zones
    for a,b in zones:
        ax.axvspan(np.sin(a), np.sin(b)-0.007, ymin=0.08, ymax=0.92, alpha=0.2, color='darkorange')
    # Save figure
    if not filedir:
        filedir = './plots/'
    if not filename:
        filename = 'mesh-{}'.format(deg1) + ('-{}'.format(deg2) if deg2 != deg1 else '') + '.png'
    fig.savefig(filedir+filename, bbox_inches='tight')
    return