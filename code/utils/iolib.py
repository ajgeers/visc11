import vtk
from urllib.request import urlopen
import zlib
import sys


def download_data(url, destination, decompress=False, chunksize=(16*1024)):
    """Download file from url to destination

    The file is read and written in chunks of chunksize to avoid overloading
    computer memory. Progress status is printed for each chunk.

    For files compressed with gzip, we use zlib to decompress the chunks
    as they are streaming in.

    """
    # open url and extract file size
    response = urlopen(url)
    file_size = int(response.getheader('Content-Length'))

    if decompress:
        # create decompression object for decompressing data streams
        decompression_object = zlib.decompressobj(16 + zlib.MAX_WBITS)

    file_size_dl = 0
    with open(destination, 'wb') as ofile:
        while True:

            # read data chunk, break when end of file is reached
            chunk = response.read(chunksize)
            if not chunk: break

            # write (decompressed) data chunk
            if decompress:
                chunk_decompressed = decompression_object.decompress(chunk)
                ofile.write(chunk_decompressed)
                chunk_decompressed = decompression_object.flush()
            else:
                ofile.write(chunk)

            # variables for print progress status
            file_size_dl += len(chunk)  # amount already downloaded
            file_name = url.split('/')[-1]
            bytes_per_MB = 1024.**2
            operation = 'Downloading '
            if decompress: operation += 'and decompressing '

            # print progress status
            status = (operation + '{:s}     '.format(file_name) +
                      '{:.1f} / '.format(file_size_dl / bytes_per_MB) +
                      '{:.1f} MB '.format(file_size / bytes_per_MB) +
                      '[{:.1f}%]'.format(file_size_dl * 100. / file_size) +
                      1000 * chr(8))  # hack to erase previous line
            sys.stdout.write(status)
        sys.stdout.write('\n')


def readvti(path):
    """Read VTI-files, i.e. images in VTK XML format."""
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()


def readvtu(path):
    """Read VTU-files, i.e. unstructured grids in VTK XML format."""
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()
