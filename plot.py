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
    fig,ax = plt.subplots(figsize=(15,4))
    
    # Plot mesh up to first bound
    h = 1.
    for x in range(min(d,e)+1):
        s = np.sin(x)
        ax.plot((s,s), (-h,h), 'orange')
    # Plot mesh up to second bound
    h = 1.
    for x in range(min(d,e)+1,max(d,e)+1):
        s = np.sin(x)
        ax.plot((s,s), (-h,h), 'peachpuff')
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

def graph_level_sets(inequalities, xlim=(-10,10), ylim=(-10,10),
                     G=3, title=None, legend_loc='upper left',
                     filedir=None, filename=None, filetype=None):
    """
    Graph multiple L_sin-inequalities with level sets and feasible region.
    :param inequalities: list of dicts with each dictionary corresponding to an
        inequality with values for 'L-term', 'osc-term', 'eps', and 'R'.
    """
    # Initialize plot
    fig,ax = plt.subplots(figsize=(8,6))
    mpl.rcParams['lines.color'] = 'k'
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler('color', ['k'])
    x = np.linspace(xlim[0], xlim[1], 10**G)
    y = np.linspace(ylim[0], ylim[1], 10**G)
    x, y = np.meshgrid(x, y)
    plt.axhline(0, alpha=0.1)
    plt.axvline(0, alpha=0.1)

    # Plot inequalities
    for phi in inequalities:
        # Level sets
        for c in lincombspace(phi['eps'], phi['L-term'](0,0), phi['R']):
            plt.contour(x, y, phi['L-term'](x,y), [c],
                        colors='tab:orange', linestyles='-', alpha=0.7)
        # Oscillatory boundary
        plt.contour(x, y, phi['L-term'](x,y) - phi['osc-term'](x,y), [0], colors='mediumblue')
    
    # Plot feasible region
    def feasible(x, y):
        z = np.full((len(x), len(y)), True)
        for phi in inequalities:
            z &= (phi['L-term'](x,y) < phi['osc-term'](x,y))
        return z
    plt.contourf(x, y, feasible(x,y), 1, colors=['white', 'b'], alpha=0.3)

    # Create legend
    osc_Lsin_term = mlines.Line2D([], [], color='mediumblue', linestyle='-',
                                  markersize=10, label=r'oscillatory $\mathcal{L}_{\sin}$-term')
    feasible_region = mlines.Line2D([], [], color='b', marker='s', linestyle='None',
                                    markersize=10, alpha=0.2, label='feasible region')
    level_sets = mlines.Line2D([], [], color='tab:orange', linestyle='-',
                               markersize=10, label='level sets')
    plt.legend(handles=[osc_Lsin_term, feasible_region, level_sets],
               loc=legend_loc, prop={'size': 10})
    if title:
        plt.title(title)
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    
    # Save figure
    if not filedir:
        filedir = './plots/'
    if not filename:
        filename = 'Lsin-inequalities'
    if not filetype:
        filetype = 'pdf'
    fig.savefig(filedir + filename + '.' + filetype, bbox_inches='tight')
    return

def project_level_sets(inequality, divisibilities, d, n,
                       filedir=None, filename=None, filetype=None):
    """
    Graph single L_sin-inequality with level sets and feasible region, incorporating
    divisibility predicates and projecting onto a single coordinate.
    :param inequality: dict corresponding to an inequality with values for
        'L-term', 'osc-term', 'eps', and 'R'.
    :param divisibilities: list of dicts, where each dictionary corresponds to a
        divisibility predicate with values for 
    :param d: int number of variables
    :param n: int variable index for projection
    """
    zero_tuple = [0 for i in range(d)]
    one_tuple = (1 if i+1==n else 0 for i in range(d))
    q_n = inequality['L-term'](*one_tuple) - inequality['L-term'](*zero_tuple)
    N = divisibility_N(divisibilities, n)
    Ia = -inequality['R'] - N*np.abs(q_n)
    # Set of level set values
    S = lincombspace(inequality['eps'], inequality['L-term'](*zero_tuple), inequality['R'], Ia)
    
    # Create plot
    fig,ax = plt.subplots(figsize=(15,4))
    
    # Fill zones for oscillation and divisibility handling
    h = 1.
    ah = h + 0.1
    hp = 0.08
    ax.axvspan(-inequality['R'], inequality['R'], ymin=hp, ymax=1.-hp,
               alpha=0.1, color='seagreen')
    ax.axvspan(1.2*Ia, -inequality['R'], ymin=hp, ymax=1.-hp,
               alpha=0.1, color='b')
    
    # Plot level set values
    h = 0.9
    for c in S:
        ax.plot((c,c), (-h,h), 'tab:orange')

    # Plot zone lines
    h = 1.
    ax.plot((Ia,Ia), (-h,h), 'tab:orange')
    ax.annotate(str(Ia), (Ia,ah), horizontalalignment="right", verticalalignment="center")
    ax.plot((-inequality['R'],-inequality['R']), (-h,h), 'mediumblue', linestyle='--')
    xx = np.linspace(-inequality['R'], inequality['R'], 100)
    ax.plot(xx, 0.1*np.sin(inequality['R']*np.pi*xx), 'mediumblue', linestyle='--')
    ax.annotate(str(-inequality['R']), (-inequality['R'],ah),
                horizontalalignment="right", verticalalignment="center")
    ax.plot((inequality['R'],inequality['R']), (-h,h), 'green')
    ax.annotate(str(inequality['R']), (inequality['R'],ah),
                horizontalalignment="left", verticalalignment="center")
    ax.annotate(r'$x_{n}$'.format(n=n), (1.125*inequality['R'],-0.125),
                horizontalalignment="center", verticalalignment="center", fontsize=13)
    
    # Finalize plot
    ax.set_xlim(left=1.2*Ia, right=1.2*inequality['R'])
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
        filename = 'single_L_sin-inequality_projected_dim-{}'.format(d)
    if not filetype:
        filetype = 'pdf'
    fig.savefig(filedir + filename + '.' + filetype, bbox_inches='tight')