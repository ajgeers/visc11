"""Contour plots with streamlines superimposed of the in-plane velocity
(xy-velocity) on the xy-slice. The slices are obtained by slicing the CFD
datasets (vtu format) with the xy-plane at z = 0 mm.

"""

import os
import vtk
import numpy as np
import matplotlib.pyplot as plt
from utils import iolib
from utils import vtklib


def streamplot(cfd, ofile='streamplot.pdf', zloc=0.0, xmin=0, xmax=1,
               ymin=0, ymax=1, gridspacing=1.0, streamlinedensity=1,
               hidelabels=False):
    """Contour plot with streamlines superimposed on the xy-slice at z = zloc

    Input: Unstructured grid with Vx_mm_s, Vy_mm_s and Vxy_mm_s pointdata
    Output: Plot saved as PDF

    To create the contourplot, the cfd dataset is sliced with a plane. From this
    slice we extract the x- and y-coordinates, vxy, and a list with for each
    triangle the indices of the three points that make up the triangle, ordered
    in anticlockwise manner.

    To create the streamplot, the cfd dataset is probed with an evenly spaced
    grid. The argument gridspacing controls the resolution. Note that
    undersampling might lead to non-zero vxy values outside the flow domain and,
    thus, to streamlines running outside of it. The argument streamlinedensity
    controls the closeness of streamlines. When streamlinedensity=1, the domain
    is divided into a 25x25 grid; density linearly scales this grid.

    In the paper, we also show plots of vxy vs. y. Therefore, a line
    corresponding to the y-axis is added to the streamplot.

    """

    #==========================================================================
    # Slice CFD dataset
    #==========================================================================

    # slice cfd dataset with xy-plane
    xyslice = vtklib.slicedataset(cfd, [0, 0, zloc], [0, 0, 1])
    xyslice = vtklib.triangulate(xyslice)
    numberofcells = xyslice.GetNumberOfCells()
    numberofpoints = xyslice.GetNumberOfPoints()

    #==========================================================================
    # Contour plot
    #==========================================================================

    # initialize figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # nparrays for x, y, vxy
    x = np.empty(numberofpoints)
    y = np.empty(numberofpoints)
    vxy = np.empty(numberofpoints)
    vxyarray = xyslice.GetPointData().GetArray('Vxy_mm_s')
    for i in range(numberofpoints):
        x[i] = xyslice.GetPoint(i)[0]
        y[i] = xyslice.GetPoint(i)[1]
        vxy[i] = vxyarray.GetValue(i)

    # array defining pointids per triangle
    triangles = np.empty(shape=(numberofcells, 3))
    for i in range(numberofcells):
        cellpointids = xyslice.GetCell(i).GetPointIds()
        for j in range(cellpointids.GetNumberOfIds()):
            triangles[i, j] = cellpointids.GetId(j)

    # plot filled contours
    cplot = ax.tricontourf(x, y, triangles, vxy,
                           levels=np.linspace(0, 100, 101),
                           cmap='RdBu_r', extend='both', zorder=-1)

    #==========================================================================
    # Stream plot
    #==========================================================================

    # evenly spaced grid
    xgrid, ygrid = np.mgrid[xmin:xmax+gridspacing:gridspacing,
                            ymin:ymax+gridspacing:gridspacing]
    xsize, ysize = xgrid.shape

    # convert evenly spaced grid to vtkPoints object
    probepoints = vtk.vtkPoints()
    probepoints.SetNumberOfPoints(xsize * ysize)
    probepointid = 0
    for i in range(xsize):
        for j in range(ysize):
            probepointx = xgrid[i, j]
            probepointy = ygrid[i, j]
            probepointz = zloc
            probepoint = (probepointx, probepointy, probepointz)
            probepoints.SetPoint(probepointid, probepoint)
            probepointid += 1
    probe = vtk.vtkPolyData()
    probe.SetPoints(probepoints)

    # probe the cfd result with evenly spaced grid
    prober = vtk.vtkProbeFilter()
    prober.SetInput(probe)
    prober.SetSource(cfd)
    prober.Update()
    xyslicegrid = prober.GetOutput()

    # create nparrays for vx and vy with same shape as xgrid and ygrid
    vxarray = xyslicegrid.GetPointData().GetArray('Vx_mm_s')
    vyarray = xyslicegrid.GetPointData().GetArray('Vy_mm_s')
    vx = np.empty(shape=(xsize, ysize))
    vy = np.empty(shape=(xsize, ysize))
    pointid = 0
    for i in range(xsize):
        for j in range(ysize):
            vx[i, j] = vxarray.GetValue(pointid)
            vy[i, j] = vyarray.GetValue(pointid)
            pointid += 1

    # streamline width is a function of vxy magnitude
    speed = np.sqrt(vx*vx + vy*vy)
    lw = 5 * speed / speed.max()

    # plot streamlines; arrays need to be transposed
    ax.streamplot(xgrid.T, ygrid.T, vx.T, vy.T, density=streamlinedensity,
                  color='.5', linewidth=lw.T)

    # draw y-axis
    ax.axvline(0, ymin, ymax, color='w', ls='-', lw=2, zorder=10)

    #==========================================================================
    # Set plot properties and write plot
    #==========================================================================

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
    ax.set_rasterization_zorder(0)  # raster contourplot, vector rest
    fig.savefig(ofile, bbox_inches="tight", dpi=200)
    plt.close()


#==============================================================================

root = os.path.join(os.path.dirname(__file__), os.pardir)
path = os.path.join(root, 'figs', 'streamplot_xyplane')
if not os.path.exists(path):
    os.makedirs(path)

cases = ['case' + str(i).zfill(1) for i in range(6)]
for case in cases:

    print case

    cfd = iolib.readvtu(os.path.join(root, 'data', 'cfd', case + '.vtu'))

    streamplot(cfd, ofile=os.path.join(path, case + '.pdf'),
               zloc=0, xmin=-6, xmax=6, ymin=-7, ymax=5,
               gridspacing=0.005, streamlinedensity=2, hidelabels=True)
