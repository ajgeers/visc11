"""Contour plots of the in-plane velocity (xy-velocity) on the xy-slice. The
slices are obtained by slicing the CFD datasets (vtu format) with the xy-plane
at z = 0 mm. To create a corresponding contour plot for the PIV dataset, we
sample the PIV image with the CFD xy-slice of case 0.

We discarded the x < 6 mm region of the PIV image from data analysis, because we
considered the particularly low velocity values in that region to be the result
of an imaging artifact. For the contour plots, the lower value of the x plot
range was therefore set to x = -6. Only a small part of 'artifact' is still
visible in the upper left corner. As described in the paper's Discussion,
slight inaccuracies in the refractive index matching between glass and fluid can
lead to inaccuracies in the measured velocity field, most notably in regions
where the normal on the glass surface is nearly perpendicular to the optical
axis. Near x = 6 mm, outlet 2 branched off from the right ACA-A1 (the aneurysm's
parent vessel), which could explain the imaging artifacts we are seeing.

"""

import os
import vtk
import numpy as np
import matplotlib.pyplot as plt
from utils import iolib
from utils import vtklib


def samplepiv(piv, xyslice):
    """Sample piv image with xyslice"""
    prober = vtk.vtkProbeFilter()
    prober.SetInput(xyslice)
    prober.SetSource(piv)
    prober.Update()
    return prober.GetOutput()


def contourplot(xyslice, ofile='contourplot.pdf', xmin=0, xmax=1,
                ymin=0, ymax=1, hidelabels=False):
    """Create contourplot on xyslice"""
    xyslice = vtklib.triangulate(xyslice)

    # data size
    numberofpoints = xyslice.GetNumberOfPoints()
    numberofcells = xyslice.GetNumberOfCells()

    # nparrays for x, y, vxy
    x = np.empty(numberofpoints)
    y = np.empty(numberofpoints)
    vxy = np.empty(numberofpoints)
    for i in range(numberofpoints):
        x[i] = xyslice.GetPoint(i)[0]
        y[i] = xyslice.GetPoint(i)[1]
        vxy[i] = xyslice.GetPointData().GetArray('Vxy_mm_s').GetValue(i)

    # array defining pointids per triangle
    triangles = np.empty(shape=(numberofcells, 3))
    for i in range(numberofcells):
        cellpointids = xyslice.GetCell(i).GetPointIds()
        for j in range(cellpointids.GetNumberOfIds()):
            triangles[i, j] = cellpointids.GetId(j)

    # initialize figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # plot filled contours
    cplot = ax.tricontourf(x, y, triangles, vxy,
                           levels=np.linspace(0, 100, 21),
                           cmap='RdBu_r', extend='both')

    # set axes labels and ticks
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('x [mm]', fontsize=36)
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
path = os.path.join(root, 'figs', 'contourplot_xyplane')
if not os.path.exists(path):
    os.makedirs(path)

datasets = ['case' + str(i).zfill(1) for i in range(6)] + ['piv']
for dataset in datasets:

    print dataset

    if dataset == 'piv':
        # read piv image and probe with cfd xyslice of case 0
        piv = iolib.readvti(os.path.join(root, 'data', 'piv', dataset + '.vti'))
        cfd = iolib.readvtu(os.path.join(root, 'data', 'cfd', 'case0.vtu'))
        xyslice_cfd = vtklib.slicedataset(cfd, [0, 0, 0], [0, 0, 1])
        xyslice = samplepiv(piv, xyslice_cfd)
    else:
        # read cfd data and extract xyslice
        cfd = iolib.readvtu(os.path.join(root, 'data', 'cfd', dataset + '.vtu'))
        xyslice = vtklib.slicedataset(cfd, [0, 0, 0], [0, 0, 1])

    contourplot(xyslice, ofile=os.path.join(path, dataset + '.pdf'),
                xmin=-6, xmax=6, ymin=-7, ymax=5, hidelabels=True)
