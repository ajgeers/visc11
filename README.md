Virtual Intracranial Stenting Challenge 2011
============================================

Author: Arjan Geers (ajgeers@gmail.com)


About
-----

This is a repository with Python scripts to reproduce some of the plots in:

Cito S, Geers AJ, Arroyo MP, Palero VR, Pallarés J, Vernet A, Blasco J, San Román L, Fu W, Qiao A, Janiga G, Miura Y, Ohta M, Mendina M, Usera G, and Frangi AF. Accuracy and Reproducibility of Patient-Specific Hemodynamics Models of Stented Intracranial Aneurysms: Report on the Virtual Intracranial Stenting Challenge 2011. Annals of Biomedical Engineering, 43(1):154–167, 2015.


The Challenge
-------------

Since 2006, the yearly Virtual Intracranial Stenting Challenge (VISC) has been a unique platform evaluating the inter-group reproducibility of computational fluid dynamics (CFD) simulations of stented aneurysms.

The 2011 edition of VISC was organized by Salvatore Cito and Arjan Geers. Preliminary results were presented at the 8th International Interdisciplinary Cerebrovascular Symposium (ICS) 2011, Shanghai, China.

The subject of the challenge was an aneurysm located at the anterior communicating artery. This is the vascular geometry with labels for inlets/outlets and regions-of-interest:

![](figs/example/geometry.png?raw=true)

Challenge participants were invited to simulate the steady-state velocity field in the aneurysm assuming blood to be an incompressible Newtonian fluid and the vessel wall to be rigid with a no-slip boundary condition.

The velocity field had to be assessed for the untreated aneurysm (case 0) and for the aneurysm virtually treated with five different configurations of high-porosity stents (cases 1 to 5). The stent configurations were composed of open cell and closed cell stents, as can be seen in this image:

![](figs/example/stent_configurations.png?raw=true)

As input data, we provided the challenge participants with surface meshes of the vascular geometry and the deployed stents, blood properties, and flow rate boundary conditions for all inlets and outlets.

The simulated velocity field of case 0 was validated with particle imaging velocimetry (PIV) measurements.

For more details, please check the journal publication.


Data
----

Three sets of data are available on [FigShare]:

1. [Dataset 1]. Input data provided to the participants:
    * STL surface mesh (in mm) of vascular geometry
    * STL surface meshes (in mm) of deployed stent geometries
    * Image of vascular and stent geometries with labels for inlets/outlets and regions-of-interest
    * Instructions to challenge participants, including flow rate boundary conditions and blood properties
2. [Dataset 2]. PIV dataset:
    * PIV dataset (in mm) stored in a vtkImageData object
3. [Dataset 3]. CFD solutions from one of the participants (research group E):
    * CFD solutions of all cases stored in vtkUnstructuredGrid objects
    * Details on the mesh and CFD set-up

If you download the data directly from FigShare and wish to run the scripts, please copy [Dataset 1] to `data/input`, [Dataset 2] to `data/piv`, and [Dataset 3] to `data/cfd`. The gz-files in `data/cfd` will need to be decompressed.

However, by far the easiest way to download the data is to run `code/download_data.py`, cross your fingers, and watch the data folder getting populated automatically.



Instructions
------------

To run the scripts, follow these instructions.

Clone the repository and cd into it:
```sh
git clone https://github.com/ajgeers/visc11
cd visc11
```

Download the data from FigShare:
```sh
python code/download_data.py
```

Run any of the other scripts to generate plots. For example,
```sh
python code/contourplot_xyplane.py
```

generates for each of the six cases and the piv image a velocity contourplot on the xy-plane and saves it in PDF format.

For case 1, these are the outputs of, from left to right, `code/streamplot_xyplane.py`, `code/contourplot_xyplane.py`, `code/contourplot_yzplane.py` and `code/lineplot_yaxis.py`:

![](figs/example/streamplot_xyplane.png?raw=true)
![](figs/example/contourplot_xyplane.png?raw=true)
![](figs/example/contourplot_yzplane.png?raw=true)
![](figs/example/lineplot_yaxis.png?raw=true)

Notes:
* Six research groups participated in the challenge. In the paper, we showed the results from all groups together in the plots generated with `code/lineplot_yaxis.py`.
* `code/streamplot_xyplane.py` takes relatively long to run.
* The data in `input/` is not needed for making the plots.


Dependencies
------------

The scripts in this repository were successfully run with:
- [Python] 2.7
- [NumPy] 1.8
- [matplotlib] 1.3
- [VTK] 5.10

An easy way of installing these dependencies is to install [Anaconda]. Make sure to add VTK with `conda install vtk`.

[Python]:http://www.python.org
[NumPy]:http://www.numpy.org
[matplotlib]:http://matplotlib.org
[VTK]:http://www.vtk.org
[Anaconda]:https://store.continuum.io/cshop/anaconda
[FigShare]:http://figshare.com/authors/Arjan_J_Geers/403823
[Dataset 1]:http://dx.doi.org/10.6084/m9.figshare.1060443
[Dataset 2]:http://dx.doi.org/10.6084/m9.figshare.1060453
[Dataset 3]:http://dx.doi.org/10.6084/m9.figshare.1060464


License
-------

BSD 2-Clause