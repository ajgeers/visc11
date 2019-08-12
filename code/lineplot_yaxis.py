"""Plot the xy-velocity along the y-axis for all cfd datasets and the piv
image."""

import os
import vtk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from matplotlib.ticker import MaxNLocator
from utils import iolib
from utils import vtklib


def extract_vxy_vs_y(polyline):
    """Extract xy-velocity vs. y data from polyline parallel to y-axis"""
    numberofpoints = polyline.GetNumberOfPoints()
    vxy_unsorted = np.zeros(shape=(numberofpoints, 2))
    vxyarray = polyline.GetPointData().GetArray('Vxy_mm_s')
    for i in range(numberofpoints):
        vxy_unsorted[i, 0] = polyline.GetPoint(i)[1]
        vxy_unsorted[i, 1] = vxyarray.GetValue(i)
    vxy = vxy_unsorted[vxy_unsorted[:, 0].argsort()]  # sort by y
    return vxy


#==============================================================================

root = os.path.join(os.path.dirname(__file__), os.pardir)
path = os.path.join(root, 'figs', 'lineplot_yaxis')
if not os.path.exists(path):
    os.makedirs(path)

# set inset properties
inset_xlim = [[0.65, 2.15], [1.1, 2.6],
              [0.95, 2.45], [1.1, 2.6],
              [0.95, 2.45], [0.85, 2.35]]  # x width is 1.5
inset_ylim = [[42.5, 49.5], [10.5, 17.5],
              [22.5, 29.5], [7.5, 14.5],
              [32.5, 39.5], [14.5, 21.5]]  # y width is 7
inset_kwargs = [dict(loc1=2, loc2=4),
                dict(loc1=1, loc2=3),
                dict(loc1=1, loc2=4),
                dict(loc1=1, loc2=3),
                dict(loc1=1, loc2=4),
                dict(loc1=1, loc2=3)]

cases = ['case' + str(i).zfill(1) for i in range(6)]
for j, case in enumerate(cases):

    print(case)

    # initiate figure with inset axes
    fig = plt.figure()
    ax = fig.add_subplot(111)
    axins = zoomed_inset_axes(ax,
                              zoom=4,
                              loc=6,
                              bbox_to_anchor=(0.07, 0.6),
                              bbox_transform=ax.transAxes)

    # plot piv with case0
    if case == 'case0':

        # read piv image; extract polyline along y-axis; extract vxy vs. y data
        piv = iolib.readvti(os.path.join(root, 'data', 'piv', 'piv.vti'))
        yaxis = vtklib.slicedataset(piv, [0, 0, 0], [1, 0, 0])
        vxy = extract_vxy_vs_y(yaxis)

        # plot piv data
        ax.plot(vxy[:, 0], vxy[:, 1], c='k', ls='', marker='o', markersize=6)
        axins.plot(vxy[:, 0], vxy[:, 1], c='k', ls='', marker='o', markersize=6)

    # read cfd data; extract polyline along y-axis; extract vxy vs. y data
    cfd = iolib.readvtu(os.path.join(root, 'data', 'cfd', case + '.vtu'))
    xyplane = vtklib.slicedataset(cfd, [0, 0, 0], [0, 0, 1])
    yaxis = vtklib.slicedataset(xyplane, [0, 0, 0], [1, 0, 0])
    vxy = extract_vxy_vs_y(yaxis)

    # plot line
    ax.plot(vxy[:, 0], vxy[:, 1], c='black', ls='-')
    axins.plot(vxy[:, 0], vxy[:, 1], c='black', ls='-')

    # axis properties
    ax.set_xlim(-9, 5)
    ax.set_ylim(0, 51)
    ax.set_xlabel('y [mm]', fontsize=36)
    ax.set_ylabel('$\mathregular{v_{xy}}$ [mm/s]', fontsize=36)
    plt.setp(ax.get_xticklabels(), fontsize=26)
    plt.setp(ax.get_yticklabels(), fontsize=26)

    # inset properties
    axins.set_xlim(inset_xlim[j][0], inset_xlim[j][1])
    axins.set_ylim(inset_ylim[j][0], inset_ylim[j][1])
    plt.setp(axins.get_xticklabels(), fontsize=14)
    plt.setp(axins.get_yticklabels(), fontsize=14)
    mark_inset(ax, axins, facecolor='None', **inset_kwargs[j])

    # Set max ticks of x-axis of inset. Command doesn't explicitly refer to
    # inset, but it's the currently active axis.
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=5))

    # write figure
    fig.savefig(os.path.join(path, case + '.pdf'), bbox_inches="tight")
    plt.close()
