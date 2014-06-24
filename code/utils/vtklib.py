import vtk


def extractboundaryedge(surface, feature_edges=False):
    """Extract boundary edges of a surface mesh."""
    edge = vtk.vtkFeatureEdges()
    edge.SetInput(surface)
    if not feature_edges:
        edge.FeatureEdgesOff()
    edge.Update()
    return edge.GetOutput()


def extractclosestpointregion(polydata, point=[0, 0, 0]):
    """Extract region closest to specified point."""
    connect = vtk.vtkPolyDataConnectivityFilter()
    connect.SetInput(polydata)
    connect.SetExtractionModeToClosestPointRegion()
    connect.SetClosestPoint(point)
    connect.Update()
    return connect.GetOutput()


def slicedataset(dataset, point, normal):
    """Slice through a vtkDataSet object with a plane defined by point and
    normal."""
    cutplane = vtk.vtkPlane()
    cutplane.SetOrigin(point)
    cutplane.SetNormal(normal)
    cutter = vtk.vtkCutter()
    cutter.SetInput(dataset)
    cutter.SetCutFunction(cutplane)
    cutter.Update()
    return cutter.GetOutput()


def triangulate(surface):
    """Triangulate a surface mesh."""
    trianglefilter = vtk.vtkTriangleFilter()
    trianglefilter.SetInput(surface)
    trianglefilter.Update()
    return trianglefilter.GetOutput()
