import os
from utils import iolib


# find project root and specify url where data is located
root = os.path.join(os.path.dirname(__file__), os.pardir)
dropbox = 'https://dl.dropboxusercontent.com/u/3937470/'

# create local folders to download data into
cfdpath = os.path.join(root, 'data', 'cfd')
pivpath = os.path.join(root, 'data', 'piv')
inputpath = os.path.join(root, 'data', 'input')
for path in [cfdpath, pivpath, inputpath]:
    if not os.path.exists(path):
        os.makedirs(path)

# files to download
pivfiles = ['piv.vti']
inputfiles = ['ccs_center.stl', 'ccs_left.stl', 'ccs_right.stl',
              'ocs_left.stl', 'ocs_right.stl', 'surface.stl',
              'geometry.pdf', 'challenge_instructions.txt']
cfdfiles = ['case0.vtu', 'case1.vtu', 'case2.vtu',
            'case3.vtu', 'case4.vtu', 'case5.vtu',
            'cfd_setup.txt']

# download piv data
print '\r\nDownloading PIV data...'
for pivfile in pivfiles:
    iolib.download_data(dropbox + '/visc11/piv/' + pivfile,
                        os.path.join(pivpath, pivfile))

# download input data
print '\r\nDownloading input data...'
for inputfile in inputfiles:
    iolib.download_data(dropbox + '/visc11/input/' + inputfile,
                        os.path.join(inputpath, inputfile))

# download cfd data
print '\r\nDownloading CFD data...'
for cfdfile in cfdfiles:
    if os.path.splitext(cfdfile)[1] == '.txt':
        iolib.download_data(dropbox + '/visc11/cfd/' + cfdfile,
                            os.path.join(cfdpath, cfdfile))
    else:
        iolib.download_data(dropbox + '/visc11/cfd/' + cfdfile + '.gz',
                            os.path.join(cfdpath, cfdfile), True)
