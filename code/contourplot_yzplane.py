"""Contour plots of the out-of-plane velocity (i.e. x-velocity) on the yz-slice. The
slices are obtained by slicing the CFD datasets (vtu format) with the yz-plane
at x = 3 mm.

"""

import os
import vtk
import numpy as np
import matplotlib.pyplot as plt
from utils import iolib
from utils import vtklib


def slice_edge(yzslice):
    """Extract edge of yzslice"""
    edge = vtklib.extractfeatureedges(yzslice)

    # number of points and cells
    numberofpoints = edge.GetNumberOfPoints()
    numberofcells = edge.GetNumberOfCells()

    # obtain pointids and sort them by connectivity
    for i in range(numberofcells):
        start = edge.GetCell(i).GetPointIds().GetId(0)
        end = edge.GetCell(i).GetPointIds().GetId(1)
        if i==0:
            connectivity = {start: end}
        else:
            connectivity.update({start: end})
    currentpoint = 0
    points_sorted = [currentpoint]
    for j in range(len(connectivity)):
        currentpoint = connectivity[currentpoint]
        points_sorted.append(currentpoint)

    # obtain list of xyz's sorted by connectivity
    edgex = np.zeros(numberofpoints + 1)
    edgey = np.zeros(numberofpoints + 1)
    edgez = np.zeros(numberofpoints + 1)
    for i, pointid in enumerate(points_sorted):
        edgex[i] = edge.GetPoint(pointid)[0]
        edgey[i] = edge.GetPoint(pointid)[1]
        edgez[i] = edge.GetPoint(pointid)[2]

    return edgex, edgey, edgez


def contourplot(yzslice, ofile='contourplot.pdf', zmin=0, zmax=1,
               ymin=0, ymax=1, hidelabels=False):
    """Create contourplot on yzslice"""
    yzslice = vtklib.triangulate(yzslice)

    # data size
    numberofpoints = yzslice.GetNumberOfPoints()
    numberofcells = yzslice.GetNumberOfCells()

    # nparrays for y, z, vx
    y = np.empty(numberofpoints)
    z = np.empty(numberofpoints)
    vx = np.empty(numberofpoints)
    for i in range(numberofpoints):
        y[i] = yzslice.GetPoint(i)[1]
        z[i] = yzslice.GetPoint(i)[2]
        vx[i] = yzslice.GetPointData().GetArray('Vx_mm_s').GetValue(i)

    # array defining pointids per triangle
    triangles = np.empty(shape=(numberofcells, 3))
    for i in range(numberofcells):
        cellpointids = yzslice.GetCell(i).GetPointIds()
        for j in range(cellpointids.GetNumberOfIds()):
            triangles[i, j] = cellpointids.GetId(j)

    # extract edge coordinates of yzslice
    edgex, edgey, edgez = slice_edge(yzslice)

    # initialize figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # plot filled contours and add slice edge
    cplot = ax.tricontourf(z, y, triangles, vx,
                           levels=np.linspace(-5, 5, 21),
                           cmap='RdBu_r', extend='both')
    ax.plot(edgez, edgey, c='k', lw=2)

    # set axes labels and ticks
    ax.set_xlim(zmin, zmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('z [mm]', fontsize=36)
    ax.set_ylabel('y [mm]', fontsize=36)
    plt.setp(ax.get_xticklabels(), fontsize=32)
    plt.setp(ax.get_yticklabels(), fontsize=32)
    if hidelabels:
        # do not show axes labels and ticks
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    # write figure
    ax.set_aspect('equal')
    ax.set_rasterization_zorder(2.0)  # rasterize contour, vector rest
    fig.savefig(ofile, bbox_inches="tight", dpi=200)
    plt.close(fig)


#==============================================================================

root = os.path.join(os.path.dirname(__file__), os.pardir)
path = os.path.join(root, 'figs', 'contourplot_yzplane')
if not os.path.exists(path):
    os.makedirs(path)

cases = ['case' + str(i).zfill(1) for i in range(6)]
for case in cases:

    print(case)

    # read cfd data and extract the yzslice
    cfd = iolib.readvtu(os.path.join(root, 'data', 'cfd', case + '.vtu'))
    yzslice = vtklib.slicedataset(cfd, [3, 0, 0], [1, 0, 0])
    yzslice = vtklib.extractclosestpointregion(yzslice, [3, 0, 0])

    contourplot(yzslice, ofile=os.path.join(path, case + '.pdf'),
                zmin=-6, zmax=6, ymin=-7, ymax=5, hidelabels=True)
