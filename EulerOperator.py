from HalfEdge import *

def addFaceToSolid(s: Solid):
    '''在Solid中添加一个Face'''
    f = Face(s)
    s.sfaces.append(f)
    return f

def addLoopToFace(f: Face):
    '''在Face中添加一个Loop'''
    l = Loop(f)
    f.flout = l
    return l

def makeEdge(v1: Vertex, v2: Vertex, l: Loop=None) -> Edge:
    '''以v1出发生成一条边'''
    e = Edge()
    e.he1 = HalfEdge(l)
    e.he2 = HalfEdge(l)
    e.he1.vtx = v1        # 生成给定点出发的半边
    e.he2.vtx = v2        # 生成新顶点出发的半边
    e.he2.prv = e.he1
    e.he1.nxt = e.he2
    e.he1.edg = e
    e.he2.edg = e
    return e

def mvfs(xyz=np.array([0.0, 0.0, 0.0])):
    '''定义一个Solid, Face, Vertex'''
    # 从一个Vertex建立新的一个Solid
    s = Solid()
    f = addFaceToSolid(s)
    l = addLoopToFace(f)
    v = Vertex(xyz)

    s.sverts.append(v)
    return s, v         # 返回最终的solid与vertex

def mev(l: Loop, v1: Vertex, xyz=np.array([0.0, 0.0, 0.0])):
    '''定义一个新Vertex并与一给定点形成边'''
    v2 = Vertex(xyz)   # 按坐标生成新顶点

    # 创建两条新的半边，注册至loop
    e = makeEdge(v1, v2, l)
    he1 = e.he1
    he2 = e.he2

    # 边的创建与记录需要更新

    if l.ledge == None:
        # 若先前未有环，则初始化一个
        l.ledge = v1.vedge = he1
        v2.vedge = he2
        he1.prv = he2
        he2.nxt = he1
    else:
        # 若已有环，则先获得指向指定节点的半边
        v1.vedge = he1

        halfedge_to_v1 = l.ledge
        while(halfedge_to_v1.nxt.vtx != v1):
            halfedge_to_v1 = halfedge_to_v1.nxt

        # 插入两条新的半边
        he2.nxt = halfedge_to_v1.nxt
        halfedge_to_v1.nxt.prv = he2
        halfedge_to_v1.nxt = he1
        he1.prv = halfedge_to_v1

    l.lface.fsolid.sedges.append(e)
    l.lface.fsolid.sverts.append(v2)
    
    # print(f'{l.lface.fsolid.sverts[-1].vcoord}' + '\n')
    return he1

def mef(l: Loop, v1: Vertex, v2: Vertex, he: HalfEdge=None):
    '''以两个给顶点定义一条新的边，同时定义一个新的面'''

    face_new = addFaceToSolid(l.lface.fsolid)
    loop_new = addLoopToFace(face_new)

    # 对于面，补全圈
    if he != None:
        l.ledge = he
    halfedge_to_v1 = l.ledge
    while(halfedge_to_v1.nxt.vtx != v1):
        halfedge_to_v1 = halfedge_to_v1.nxt
    halfedge_to_v2 = l.ledge    
    while(halfedge_to_v2.nxt.vtx != v2):
        halfedge_to_v2 = halfedge_to_v2.nxt


    e = makeEdge(v1, v2, l)

    # 将两条半边分别加入不同圈
    e.he2.wloop = loop_new
    e.he2.nxt = halfedge_to_v1.nxt
    halfedge_to_v1.nxt.prv = e.he2      # 顺时针圈
    e.he1.prv = halfedge_to_v1
    halfedge_to_v1.nxt = e.he1          # 逆时针圈
    e.he1.nxt = halfedge_to_v2.nxt
    halfedge_to_v2.nxt.prv = e.he1
    halfedge_to_v2.nxt = e.he2          # 顺时针圈
    e.he2.prv = halfedge_to_v2
    v1.vedge = e.he1                    # 逆时针圈

    # 更改逆时针圈所注册的Loop
    halfedge_to_v2.wloop = loop_new
    halfedge_to_v2 = halfedge_to_v2.nxt
    while(halfedge_to_v2.nxt.vtx != v2):
        halfedge_to_v2.wloop = loop_new
        halfedge_to_v2 = halfedge_to_v2.nxt
    loop_new.ledge = halfedge_to_v2

    l.lface.fsolid.sedges.append(e)
    return e.he2

def kemr(l: Loop, v1: Vertex, v2: Vertex):
    '''消去环中的一条边，生成一个内环'''
    loop_new = Loop(l.lface)
    l.lface.floops.append(loop_new)

    # 获取圈中指向v1, v2的半边
    halfedge_to_v1 = l.ledge
    while(halfedge_to_v1.nxt.vtx != v1 or halfedge_to_v1.nxt.nxt.vtx != v2):
        halfedge_to_v1 = halfedge_to_v1.nxt
    halfedge_to_v2 = l.ledge    
    while(halfedge_to_v2.nxt.vtx != v2 or halfedge_to_v2.nxt.nxt.vtx != v1):
        halfedge_to_v2 = halfedge_to_v2.nxt

    halfedge_from_v1 = halfedge_to_v1.nxt
    halfedge_from_v2 = halfedge_to_v2.nxt
    halfedge_from_v1.prv.nxt = halfedge_from_v2.nxt
    halfedge_from_v2.nxt.prv = halfedge_from_v1.prv
    halfedge_from_v2.prv.nxt = halfedge_from_v1.nxt
    halfedge_from_v1.nxt.prv = halfedge_from_v2.prv

    halfedge_to_v2 = halfedge_to_v2.nxt
    while(halfedge_to_v2.nxt.vtx != v2):
        halfedge_to_v2 = halfedge_to_v2.nxt
        halfedge_to_v2.wloop = loop_new
    loop_new.ledge = halfedge_to_v2

    l.lface.fsolid.sedges.remove(halfedge_from_v1.edg)

def kfmrh(f1: Face, f2: Face):
    '''删除一个面，并将其定义为另一个面的内环'''
    f1.fsolid.sfaces.remove(f2)
    # f2.flout.ledge = f2.flout.ledge.edg.he1
    # f1.floops.append(f2.flout)
    pass

def sweep(s: Solid, direction: np.ndarray):
    count_list = []
    count_list.append(len(s.sverts))

    for face in s.sfaces[1:4]:
        # 四次mev
        loop = face.flout
        he = loop.ledge
        v = he.vtx
        mev(loop, he.vtx, he.vtx.vcoord+direction)
        while(he.nxt.vtx != v):
            he = he.nxt
            mev(loop, he.vtx, he.vtx.vcoord+direction)

        # 四次mef
        count_list.append(len(s.sverts))
        count = count_list[-1] - count_list[-2]
        loop = face.flout
        he = loop.ledge
        for i in range(count):
            next_he = mef(he.wloop, he.nxt.nxt.vtx, he.prv.vtx, he)
            he = next_he.nxt.nxt

    inner_loops = []
    for edge in s.sedges:
        he = edge.he1
        # 处理外圈
        if edge.he1.vtx == s.sverts[count_list[0]]:
            if edge.he2.vtx == s.sverts[count_list[0]+1]:
                outer_loop = edge.he1.wloop
        elif edge.he2.vtx == s.sverts[count_list[0]]:
            if edge.he1.vtx == s.sverts[count_list[0]+1]:
                outer_loop = edge.he2.wloop
        
        # 处理两个内圈
        if edge.he1.vtx == s.sverts[count_list[1]]:
            if edge.he2.vtx == s.sverts[count_list[1]+1]:
                inner_loops.append(edge.he1.wloop)
        elif edge.he2.vtx == s.sverts[count_list[1]]:
            if edge.he1.vtx == s.sverts[count_list[1]+1]:
                inner_loops.append(edge.he2.wloop)

        if edge.he1.vtx == s.sverts[count_list[2]]:
            if edge.he2.vtx == s.sverts[count_list[2]+1]:
                inner_loops.append(edge.he1.wloop)
        elif edge.he2.vtx == s.sverts[count_list[2]]:
            if edge.he1.vtx == s.sverts[count_list[2]+1]:
                inner_loops.append(edge.he2.wloop)
    
    # 将内圈代表的Face从Solid中删去，并作为外圈的内环
    for inner_loop in inner_loops:
        kfmrh(outer_loop.lface, inner_loop.lface)
        outer_loop.lface.floops.append(inner_loop)

    return s
