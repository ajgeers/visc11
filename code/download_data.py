import os
from utils import iolib


# find project root and specify url where data is located
root = os.path.join(os.path.dirname(__file__), os.pardir)
figshare = 'http://files.figshare.com/'

# create local folders to download data into
cfdpath = os.path.join(root, 'data', 'cfd')
pivpath = os.path.join(root, 'data', 'piv')
inputpath = os.path.join(root, 'data', 'input')
for path in [cfdpath, pivpath, inputpath]:
    if not os.path.exists(path):
        os.makedirs(path)

# location of files on FigShare
pivurls = ['1538421/piv.vti']
inputurls = ['1538408/ccs_center.stl', '1538407/ccs_left.stl',
             '1538409/ccs_right.stl', '1538411/ocs_left.stl',
             '1538412/ocs_right.stl', '1538410/surface.stl',
             '1545323/geometry.pdf', '1561674/challenge_instructions.txt']
cfdurls = ['1540213/case0.vtu', '1540218/case1.vtu', '1540220/case2.vtu',
            '1540219/case3.vtu', '1540222/case4.vtu', '1540221/case5.vtu',
            '1540206/cfd_setup.txt']

# download piv data
print '\r\nDownloading PIV data...'
for pivurl in pivurls:
    pivfilename = pivurl.split('/')[1]
    iolib.download_data(figshare + pivurl,
                        os.path.join(pivpath, pivfilename))

# download input data
print '\r\nDownloading input data...'
for inputurl in inputurls:
    inputfilename = inputurl.split('/')[1]
    iolib.download_data(figshare + inputurl,
                        os.path.join(inputpath, inputfilename))

# download cfd data
print '\r\nDownloading CFD data...'
for cfdurl in cfdurls:
    cfdfilename = cfdurl.split('/')[1]
    if os.path.splitext(cfdfilename)[1] == '.txt':
        iolib.download_data(figshare + cfdurl,
                            os.path.join(cfdpath, cfdfilename))
    else:
        iolib.download_data(figshare + cfdurl + '.gz',
                            os.path.join(cfdpath, cfdfilename), True)
