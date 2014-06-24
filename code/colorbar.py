"""Create colorbars corresponding to the contour and stream plots"""

import os
from utils import plotlib


root = os.path.join(os.path.dirname(__file__), os.pardir)
path = os.path.join(root, 'figs', 'colorbar')
if not os.path.exists(path):
    os.makedirs(path)

plotlib.colorbar(path=os.path.join(path, 'contourplot_xyplane.pdf'),
                 vmin=0,
                 vmax=100,
                 unit='[mm/s]',
                 colors='RdBu_r',
                 nlevels=21)

plotlib.colorbar(path=os.path.join(path, 'contourplot_yzplane.pdf'),
                 vmin=-5,
                 vmax=5,
                 unit='[mm/s]',
                 colors='RdBu_r',
                 nlevels=21)

plotlib.colorbar(path=os.path.join(path, 'streamplot_xyplane.pdf'),
                 vmin=0,
                 vmax=100,
                 unit='[mm/s]',
                 colors='RdBu_r')
