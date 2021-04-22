import numpy as np
import matplotlib.pyplot as plt

def approximate_mesh(deg1, deg2=None, vals=[], zones=[], filedir=None, filename=None):
    fig,ax = plt.subplots(figsize=(12,4))
    if not deg2:
        deg2 = deg1
    for x in range(deg2+1):
        s = np.sin(x)
        if x <= deg1:
            # Plot coarser approximates
            color = 'tab:orange'
            h = 1.
            ax.annotate(str(x), (s,1.1), horizontalalignment="center", verticalalignment="center")
        else:
            # Plot finer approximates
            color = 'b'
            h = .8
        ax.plot((s,s), (-h,h), color)
    # Shade zones
    for a,b in zones:
        if max(a,b) <= deg1:
            color = 'darkorange'
            hp = 0.0775
        else:
            color = 'mediumblue'
            hp = 0.165
        ax.axvspan(np.sin(a), np.sin(b)-0.007, ymin=hp, ymax=1.-hp, alpha=0.2, color=color)
    # Plot particular values
    for val in vals:
        s = np.sin(val)
        if val > deg2:
            ax.plot((s,s), (-0.6,0.6), 'gold')
            h = 0.7
        else:
            h = 0.9
        ax.annotate(str(val), (s,h), horizontalalignment="center", verticalalignment="center")
    # Manage plot
    ax.set_xlim(left=-1.,right=1.)
    ax.set_ylim(bottom=-1.2,top=1.2)
    ax.set_yticks([])
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_position('center')
    # Save figure
    if not filedir:
        filedir = './plots/'
    if not filename:
        filename = 'mesh-{}'.format(deg1) + ('-{}'.format(deg2) if deg2 != deg1 else '') + '.png'
    fig.savefig(filedir+filename, bbox_inches='tight')
    return