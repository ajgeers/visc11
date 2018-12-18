import os
from utils import iolib


# find project root and specify url to FigShare
root = os.path.join(os.path.dirname(__file__), os.pardir)
figshare = 'https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/'

# create local folders to download data into
cfdpath = os.path.join(root, 'data', 'cfd')
pivpath = os.path.join(root, 'data', 'piv')
inputpath = os.path.join(root, 'data', 'input')
for path in [cfdpath, pivpath, inputpath]:
    if not os.path.exists(path):
        os.makedirs(path)

# location of files on FigShare
pivurls = ['3196046/piv.vti']
inputurls = ['3195839/ccs_center.stl', '3195833/ccs_left.stl',
             '3195851/ccs_right.stl', '3195878/ocs_left.stl',
             '3195890/ocs_right.stl', '3195863/surface.stl',
             '3196049/geometry.pdf', '1561674/challenge_instructions.txt']
cfdurls = ['3196028/case0.vtu', '3196031/case1.vtu', '3196034/case2.vtu',
           '3196037/case3.vtu', '3196040/case4.vtu', '3196043/case5.vtu',
           '3196025/cfd_setup.txt']

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
