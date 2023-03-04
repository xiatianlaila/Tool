# -*- coding: UTF-8 -*-
import maya.api.OpenMaya as om
import maya.cmds as cmds


# 判断Maya版本
release = cmds.about(version=True)
if 'Preview' in release:
    version = 2023
else:
    version = int(cmds.about(version=True))

# 判断三角面
def triangular_faces(list, select_mesh):
    triangular_faces = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        face_iter = om.MItMeshPolygon(select_iter.getDagPath())
        object_name = select_iter.getDagPath().getPath()
        while not face_iter.isDone():
            num_of_edges = face_iter.getEdges()
            if len(num_of_edges) == 3:
                face_index = face_iter.index()
                component_name = str(object_name) + '.f[' + str(face_index) +']'
                triangular_faces.append(component_name)
            else:
                pass
            if version < 2020:
                face_iter.next(None)
            else:
                face_iter.next()
        select_iter.next()
    return triangular_faces

# 多边面
def ngon_faces(list, select_mesh):
    ngon_faces = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        face_iter = om.MItMeshPolygon(select_iter.getDagPath())
        object_name = select_iter.getDagPath().getPath()
        while not face_iter.isDone():
            num_of_edges = face_iter.getEdges()
            if len(num_of_edges) > 4:
                face_index = face_iter.index()
                component_name = str(object_name) + '.f[' + str(face_index) +']'
                ngon_faces.append(component_name)

            if version < 2020:
                face_iter.next(None)
            else:
                face_iter.next()
        select_iter.next()
    return ngon_faces

# 开口边
def open_edges(list, select_mesh):
    open_edges = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        edge_iter = om.MItMeshEdge(select_iter.getDagPath())
        object_name = select_iter.getDagPath().getPath()
        while not edge_iter.isDone():
            if edge_iter.numConnectedFaces() < 2:
                edge_index = edge_iter.index()
                component_name = str(object_name) + '.e[' + str(edge_index) + ']'
                open_edges.append(component_name)

            edge_iter.next()
        select_iter.next()
    return open_edges

# 极点 一个点连接了多余5个面
def have_poles(list, select_mesh):
    poles = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        vertex_iter = om.MItMeshVertex(select_iter.getDagPath())
        object_name = select_iter.getDagPath().getPath()
        while not vertex_iter.isDone():
            if vertex_iter.numConnectedFaces() > 5:
                vertex_index = vertex_iter.index()
                component_name = str(object_name) + '.vtx[' + str(vertex_index) + ']'
                poles.append(component_name)

            vertex_iter.next()
        select_iter.next()
    return poles

# 硬边
def hard_edges(list, select_mesh):
    hard_edges = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        edge_iter = om.MItMeshEdge(select_iter.getDagPath())
        object_name = select_iter.getDagPath().getPath()
        while not edge_iter.isDone():
            if edge_iter.isSmooth == False and edge_iter.onBoundary() == False:
                edge_index = edge_iter.index()
                component_name = str(object_name) + '.e[' + str(edge_index) + ']'
                hard_edges.append(component_name)

            edge_iter.next()
        select_iter.next()
    return hard_edges

# 零面积面
def zero_area_faces(list, select_mesh):
    zero_area_faces = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        face_iter = om.MItMeshPolygon(select_iter.getDagPath())
        object_name = select_iter.getDagPath().getPath()
        while not face_iter.isDone():
            face_area = face_iter.getArea()
            if face_area < 0.00000001:
                face_index = face_iter.index()
                component_name = str(object_name) + '.f[' + str(face_index) + ']'
                zero_area_faces.append(component_name)

            if version < 2020:
                face_iter.next(None)
            else:
                face_iter.next()
        select_iter.next()
    return zero_area_faces

# 零长度边
def zero_length_edges(list, select_mesh):
    zero_length_edges = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        edge_iter = om.MItMeshEdge(select_iter.getDagPath())
        object_name = select_iter.getDagPath().getPath()
        while not edge_iter.isDone():
            if edge_iter.length() <= 0.00000001:
                component_name = str(object_name) + '.f[' + str(edge_iter.index()) + ']'
                zero_length_edges.append(component_name)
            edge_iter.next()
        select_iter.next()
    return zero_length_edges


# 非流形边
def none_manifold_edges(list, select_mesh):
    none_manifold_edges = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        edge_iter = om.MItMeshEdge(select_iter.getDagPath())
        object_name = select_iter.getDagPath().getPath()
        while not edge_iter.isDone():
            if edge_iter.numConnectedFaces() > 2:
                edge_index = edge_iter.index()
                component_name = str(object_name) + '.e[' + str(edge_index) + ']'
                none_manifold_edges.append(component_name)
            edge_iter.next()
        select_iter.next()
    return none_manifold_edges


def starlike(list, select_mesh):
    starlike = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        poly_iter = om.MItMeshPolygon(select_iter.getDagPath())
        object_name = select_iter.getDagPath().getPath()
        while not poly_iter.isDone():
            if poly_iter.isStarlike() == False:
                poly_index = poly_iter.index()
                componentName = str(object_name) + '.e[' + str(poly_index) + ']'
                starlike.append(componentName)
            if version < 2020:
                poly_iter.next(None)
            else:
                poly_iter.next()
        select_iter.next()
    return starlike

# 自重叠uv
def self_penetrating_uv(list, select_mesh):
    self_penetrating_uv = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        # 对面分组并选择
        convert_to_faces = cmds.ls(cmds.polyListComponentConversion(shape, toFace=True), fl=True)
        # 得到重叠的uv面
        overlapping = cmds.polyUVOverlap(convert_to_faces, oc =True)
        if overlapping is not None:
            for obj in overlapping:
                self_penetrating_uv.append(obj)
    return self_penetrating_uv

# 丢失uv
def missing_uv(list, select_mesh):
    missing_uv = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        face_iter = om.MItMeshPolygon(select_iter.getDagPath())
        object_name =select_iter.getDagPath().getPath()
        while not face_iter.isDone():
            if face_iter.hasUVs() == False:
                component_name = str(object_name) + '.f[' + str(face_iter.index()) + ']'
                missing_uv.append(component_name)
            if version < 2020:
                face_iter.next(None)
            else:
                face_iter.next()
        select_iter.next()
    return missing_uv

# 越界UV
def cross_border_uv(list, select_mesh):
    cross_border_uv = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        face_iter = om.MItMeshPolygon(select_iter.getDagPath())
        object_name =select_iter.getDagPath().getPath()
        while not face_iter.isDone():
            U = None
            V = None
            UVs = face_iter.getUVs()
            for index, each_uvs in enumerate(UVs):
                if index == 0:
                    for each_uv in each_uvs:
                        if U == None:
                            U = int(each_uv)
                        if U != int(each_uv):
                            component_name = str(object_name) + '.f[' + str(face_iter.index()) + ']'
                            cross_border_uv.append(component_name)
                if index == 1:
                    for each_uv in each_uvs:
                        if V == None:
                            V = int(each_uv)
                        if V != int(each_uv):
                            component_name = str(object_name) + '.f[' + str(face_iter.index()) + ']'
                            cross_border_uv.append(component_name)
            if version < 2020:
                face_iter.next(None)
            else:
                face_iter.next()
        select_iter.next()
    return cross_border_uv


def uv_range(list, select_mesh):
    uv_range = []
    select_iter = om.MItSelectionList(select_mesh)
    while not select_iter.isDone():
        face_iter = om.MItMeshPolygon(select_iter.getDagPath())
        object_name =select_iter.getDagPath().getPath()
        while not face_iter.isDone():
            # 获得所有的uvSet
            UVs = face_iter.getUVs()
            # enumerate()同时列出数据和数据下标
            for index, each_uvs in enumerate(UVs):
                if index == 0:
                    for each_uv in each_uvs:
                        if each_uv < 0 or each_uv > 10:
                            component_name = str(object_name) + '.f[' + str(face_iter.index()) + ']'
                            uv_range.append(component_name)
                            break
                if index == 1:
                    for each_uv in each_uvs:
                        if each_uv < 0:
                            component_name = str(object_name) + '.f[' + str(face_iter.index()) + ']'
                            uv_range.append(component_name)
                            break
            if version < 2020:
                face_iter.next(None)
            else:
                face_iter.next()
        select_iter.next()
    return uv_range

# 是否有层级
def layers(list, select_mesh):
    layers = []
    for obj in list:
        layer = cmds.listConnections(obj, type="displayLayer")
        if layer is not None:
            layers.append(obj)
    return layers

# 存在历史
def history(list, select_mesh):
    history = []
    for obj in list:
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shape is not None:
            if cmds.nodeType(shape[0]) == "mesh":
                history_size = len(cmds.listHistory(shape))
                if history_size > 1:
                    history.append(obj)
    return history

# 是否用的默认材质
def shaders(list, select_mesh):
    shaders = []
    for obj in list:
        shading_groups = None
        shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if cmds.nodeType(shape[0]) == "mesh":
            if shape is not None:
                shading_groups = cmds.listConnections(shape, type="shadingEngine")
            if not shading_groups[0] == "initialShadingGroup":
                shaders.append(obj)
    return shaders

# 未冻结变换
def unfrozen_transforms(list, select_mesh):
    unfrozen_transforms = []
    for obj in list:
        translation = cmds.xform(obj, q=True, worldSpace=True, translation=True)
        rotation = cmds.xform(obj, q=True, worldSpace=True, rotation=True)
        scale = cmds.xform(obj, q=True, worldSpace=True, scale=True)
        if not translation == [0.0, 0.0, 0.0] or not rotation == [0.0, 0.0, 0.0] or not scale == [0.0, 0.0, 0.0]:
            unfrozen_transforms.append(obj)
    return unfrozen_transforms

# 未中心枢轴
def uncentered_pivots(list, select_mesh):
    uncentered_pivots = []
    for obj in list:
        if cmds.xform(obj, q=True, worldSpace=True, rotatePivot=True) != [0, 0, 0]:
            uncentered_pivots.append(obj)
    return uncentered_pivots
# 空组
def empty_groups(list, select_mesh):
    empty_groups = []
    for obj in list:
        children = cmds.listRelatives(obj, allDescendents=True)
        if children is None:
            empty_groups.append(obj)
    return empty_groups