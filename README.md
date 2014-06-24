Virtual Intracranial Stenting Challenge 2011
============================================

Author: Arjan Geers (ajgeers@gmail.com)


About
-----

This repository contains Python scripts to reproduce the plots in:

Cito S, Geers AJ, Arroyo MP, Palero VR, Pallarés J, Vernet A, Blasco J, San Román L, Fu W, Qiao A, Janiga G, Miura Y, Ohta M, Mendina M, Usera G, and Frangi AF. Accuracy and Reproducibility of Patient-Specific Hemodynamics Models of Stented Intracranial Aneurysms: Report on the Virtual Intracranial Stenting Challenge 2011. Under review.


The Challenge
---------

Since 2006, the yearly Virtual Intracranial Stenting Challenge (VISC) has been a unique platform evaluating the inter-group reproducibility of computational fluid dynamics (CFD) simulations of stented aneurysms.

The 2011 edition of VISC was organized by Salvatore Cito and Arjan Geers. Preliminary results were presented at the 8th International Interdisciplinary Cerebrovascular Symposium (ICS) 2011, Shanghai, China.

The subject of the challenge was an aneurysm located at the anterior communicating artery.

![geometry](figs/example/geometry.png)


Challenge participants were invited to simulate the steady-state velocity field in the aneurysm assuming blood to be an incompressible Newtonian fluid and the vessel wall to be rigid with a no-slip boundary condition.

The velocity field had to be assessed for the untreated aneurysm (case 0) and for the aneurysm virtually treated with five different configurations of high-porosity stents (cases 1 to 5).

As input data, we provided surface meshes of the vascular geometry and the deployed stents, and flow rate boundary conditions for all inlets and outlets.

The simulated velocity field of case 0 was validated with particle velocimetry imaging (PIV) measurements.

For more details, we kindly refer to the journal publication.


Data
----
Data from the challenge are available on FigShare.

1. DOI. Input data provided to the participants:
    * Surface mesh of the vascular geometry in STL format
    * Surface meshes of the deployed stents in STL format
    * Instructions (including flow rate boundary conditions, blood viscosity and density, stent configurations, etc.)
2. DOI. PIV image in vtkImageData format
3. DOI. CFD solutions from one of the participants (group E) in vtkUnstructuredGrid format

Notes:

1. For all data, the unit of length is millimeters.
2. The vascular and stent geometries and the PIV image were placed in the same coordinate system. They were positioned such that the xy-plane at z = 0 mm approximately sliced the main flow jet into the aneurysm along its axis.


Instructions
------------

To run the scripts, follow these instructions.

Create a directory, cd into it, and clone the repository:
```sh
mkdir visc11
cd visc11
git clone [git-repo-url]
```

Run download_data.py to download the data from FigShare:
```sh
python code/download_data.py
```

Run any of the other scripts to generate plots. For example,
```sh
python code/streamplot_xyplane.py
```

generates for each case a streamplot and saves it in PDF format.
```sh
open figs/streamplot_xyplane/case1.pdf
```

should give:



Dependencies
------------

The scripts in this repository were successfully run with:
- [Python] 2.7
- [NumPy] 1.8
- [matplotlib] 1.3
- [VTK] 5.10

An easy way of installing these dependencies is to install [Anaconda]. Make sure to add VTK with `conda install vtk`.

[Python]:www.python.org
[NumPy]:www.numpy.org
[matplotlib]:matplotlib.org
[VTK]:www.vtk.org
[Anaconda]:https://store.continuum.io/cshop/anaconda


License
-------

BSD 2-Clause