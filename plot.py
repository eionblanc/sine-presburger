import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from best_approximate import *
from decision import *

def approximate_mesh(deg1, deg2=None, deg1_color='tab:orange', deg1_ann=True,
                     vals=[], zones=[], filedir=None, filename=None, filetype=None):
    fig,ax = plt.subplots(figsize=(15,4))
    if not deg2:
        deg2 = deg1
    for x in range(deg2+1):
        s = np.sin(x)
        if x <= deg1:
            # Plot coarser approximates
            color = deg1_color
            h = 1.
            if deg1_ann:
                ax.annotate(str(x), (s,1.1), horizontalalignment="center", verticalalignment="center")
        else:
            # Plot finer approximates
            color = 'b'
            h = .8
        ax.plot((s,s), (-h,h), color)
    # Shade zones
    for a,b in zones:
        if max(a,b) <= deg1:
            color = deg1_color
            hp = 0.0775
        else:
            color = 'mediumblue'
            hp = 0.165
        ax.axvspan(np.sin(a), np.sin(b)-0.006, ymin=hp, ymax=1.-hp, alpha=0.1, color=color)
    # Plot particular values
    for val in vals:
        s = np.sin(val)
        if val <= deg1:
            h = 1.1
        elif val <= deg2:
            h = 0.9
        else:
            h = 0.7
            if deg1 == deg2:
                ax.plot((s,s), (-0.8,0.8), 'olivedrab')
                h += 0.2
            else:
                ax.plot((s,s), (-0.6,0.6), 'olivedrab')
        ax.annotate(str(val), (s,h), horizontalalignment="center", verticalalignment="center")
    # Manage plot
    ax.set_xlim(left=-1.,right=1.)
    ax.set_ylim(bottom=-1.2,top=1.2)
    ax.set_yticks([])
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_position('center')
    ax.set_axisbelow(False)
    ax.tick_params(length=10, direction='inout')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.75))
    # Save figure
    if not filedir:
        filedir = './plots/'
    if not filename:
        if not filetype:
            filetype = 'pdf'
        filename = 'mesh-{}'.format(deg1) + ('-{}'.format(deg2) if deg2 != deg1 else '') + '.' + filetype
    fig.savefig(filedir+filename, bbox_inches='tight')
    return

def diff_approx_mesh(x1, x2, d, e, y1=None, y2=None,
                     filedir=None, filename=None, filetype=None):
    s1 = np.sin(x1)
    s2 = np.sin(x2)
    if s1 > s2:
        tmp = x2
        x2 = x1
        x1 = tmp
        tmp = s2
        s2 = s1
        s1 = tmp
    if not (y1 and y2):
        y1,y2 = diff_approx(x1,x2,d,e)
    # Plot mesh up to first bound
    fig,ax = plt.subplots(figsize=(15,4))
    for x in range(min(d,e)+1):
        s = np.sin(x)
        color = 'orange'
        h = 1.
        ax.plot((s,s), (-h,h), color)
    # Plot mesh up to second bound
    for x in range(min(d,e)+1,max(d,e)+1):
        s = np.sin(x)
        color = 'peachpuff'
        h = 1.
        ax.plot((s,s), (-h,h), color)
    # Plot y1, y2 and difference as zone
    sy1 = np.sin(y1)
    sy2 = np.sin(y2)
    ax.plot((sy1,sy1), (-1.,1.), 'mediumblue')
    ax.annotate(str(y1), (sy1,1.1), horizontalalignment="right", verticalalignment="center")
    ax.plot((sy2,sy2), (-1.,1.), 'mediumblue')
    ax.annotate(str(y2), (sy2,1.1), horizontalalignment="left", verticalalignment="center")
    a = min(sy1,sy2)
    b = max(sy1,sy2)
    hp = 0.08
    ax.axvspan(a, b, ymin=hp, ymax=1.-hp, alpha=0.1, color='b')
    # Plot x1, x2, and difference as zone
    ax.plot((s1,s1), (-1.,1.), 'green')
    if min(np.abs(s1-sy1),np.abs(s1-sy2),np.abs(s2-sy1),np.abs(s2-sy2)) < 0.05:
        ah = -1.1
    else:
        ah = 1.1
    ax.annotate(str(x1), (s1,ah), horizontalalignment="right", verticalalignment="center")
    ax.plot((s2,s2), (-1.,1.), 'green')
    ax.annotate(str(x2), (s2,ah), horizontalalignment="left", verticalalignment="center")
    hp = 0.08
    ax.axvspan(s1, s2, ymin=hp, ymax=1.-hp, alpha=0.1, color='seagreen')
    # Manage plot
    ax.set_xlim(left=-1.,right=1.)
    ax.set_ylim(bottom=-1.2,top=1.2)
    ax.set_yticks([])
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_position('center')
    ax.set_axisbelow(False)
    ax.tick_params(length=10, direction='inout')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.75))
    # Save figure
    if not filedir:
        filedir = './plots/'
    if not filename:
        if not filetype:
            filetype = 'pdf'
        filename = 'diffmesh-{}-{}.'.format(x1,x2) + filetype
    fig.savefig(filedir+filename, bbox_inches='tight')
    return

def level_sets(eps, cons, R, L_term, osc_Lsin_term,
               xa=-5, xb=5, ya=-5, yb=10, flip=False,
               filedir=None, filetype=None, filename=None):
    # Initialize plot
    fig,ax = plt.subplots(figsize=(6,5))
    mpl.rcParams['lines.color'] = 'k'
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler('color', ['k'])
    x = np.linspace(xa, xb, 10**3)
    y = np.linspace(ya, yb, 10**3)
    x, y = np.meshgrid(x, y)
    plt.axhline(0, alpha=0.1)
    plt.axvline(0, alpha=0.1)
    
    # Plot level sets
    for val in lincombspace(eps, cons, R):
        plt.contour(x, y, L_term(x,y), [val], colors='tab:orange', alpha=0.7, linestyles='-')
    for val in [R, -R]:
        plt.contour(x, y, L_term(x,y), [val], colors='tab:orange', alpha=1, linestyles='-')
    # Plot inequality boundary
    plt.contour(x, y, L_term(x,y) - osc_Lsin_term(x,y), [0], colors='mediumblue')
    # Plot feasible set
    if flip:
        C = ['b', 'white']
    else:
        C = ['white', 'b']
    plt.contourf(x, y, L_term(x,y) - osc_Lsin_term(x,y), 1, colors=C, alpha=0.1)

    # Create legend
    osc_Lsin_term = mlines.Line2D([], [], color='mediumblue', linestyle='-',
                                  markersize=10, label=r'oscillatory $\mathcal{L}_{\sin}$-term')
    feasible_region = mlines.Line2D([], [], color='b', marker='s', linestyle='None',
                                    markersize=10, alpha=0.2, label='feasible region')
    level_sets = mlines.Line2D([], [], color='tab:orange', linestyle='-',
                               markersize=10, label='level sets')
    plt.legend(handles=[osc_Lsin_term, feasible_region, level_sets],
               loc='upper left', prop={'size': 12})
    # Save figure
    if not filedir:
        filedir = './plots/'
    if not filename:
        if not filetype:
            filetype = 'pdf'
        filename = 'Lsin-inequality.' + filetype
    fig.savefig(filedir+filename, bbox_inches='tight')
    return