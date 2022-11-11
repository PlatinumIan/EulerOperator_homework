import numpy as np

class Solid(object):
    def __init__(self) -> None:
        self.prevs = None   # previous solid
        self.nexts = None   # next solid
        self.sfaces = []    # list of faces
        self.sedges = []    # list of edges
        self.sverts = []    # list of vertices
    
class Face(object):
    def __init__(self, s=None) -> None:
        self.prevf = None   # previous face
        self.nextf = None   # next face
        self.flout: Loop = None   # outer loop
        self.floops = []    # list of loops
        self.fsolid: Solid = s     # back to solid

class Loop(object):
    def __init__(self, f=None) -> None:
        self.prevl = None   # previous loop
        self.nextl = None   # next loop
        self.ledge: HalfEdge = None   # ring of halfedges
        self.lface: Face = f      # back to face

class HalfEdge(object):
    def __init__(self, l=None) -> None:
        self.prv: HalfEdge = None     # previous halfedge
        self.nxt: HalfEdge = None     # next halfedge
        self.edg: Edge = None     # parent edge
        self.vtx: Vertex = None     # starting vertex
        self.wloop: Loop = l      # back to loop

class Vertex(object):
    def __init__(self, xyz=np.array([0.0, 0.0, 0.0])) -> None:
        self.prevv = None   # previous vertex
        self.nextv = None   # next vertex
        self.vcoord: np.ndarray = xyz  # coordinates
        self.vedge: HalfEdge = None   # to halfedge

class Edge(object):
    def __init__(self) -> None:
        self.preve = None   # previous edge
        self.nexte = None   # next edge
        self.he1: HalfEdge = None     # halfedge 1
        self.he2: HalfEdge = None     # halfedge 2
