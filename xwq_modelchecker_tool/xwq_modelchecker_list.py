# -*- coding: UTF-8 -*-
mcCommandsList = [
    # 三角面
    {
        "func": "triangular_faces",
        "label": "Triangles",
        "type": "topology",
        "defaultChecked": False,
        "tip": "是否存在三角面"
    },
    # 多边面
    {
        "func": "ngon_faces",
        "label": "Ngons",
        "type": "topology",
        "defaultChecked": False,
        "tip": "是否存在多边面"
    },
    # 开口边
    {
        "func": "open_edges",
        "label": "Open Edges",
        "type": "topology",
        "defaultChecked": False,
        "tip": "是否存在开口边"
    },
    # 极点
    {
        "func": "have_poles",
        "label": "Poles",
        "type": "topology",
        "defaultChecked": False,
        "tip": "是否存在极点（一个点连接大于5个面）"
    },
    # 硬边
    {
        "func": "hard_edges",
        "label": "Hard Edges",
        "type": "topology",
        "defaultChecked": False,
        "tip": "是否存在硬边"
    },
    # 零面积面
    {
        "func": "zero_area_faces",
        "label": "Zero Area Faces",
        "type": "topology",
        "defaultChecked": False,
        "tip": "是否存在零面积面"
    },
    # 零长度边
    {
        "func": "zero_length_edges",
        "label": "Zero Length Edges",
        "type": "topology",
        "defaultChecked": False,
        "tip": "是否存在零长度边"
    },
    # 非流形边
    {
        "func": "none_manifold_edges",
        "label": "None Manifold Edges",
        "type": "topology",
        "defaultChecked": False,
        "tip": "是否存在非流形边"
    },
    # 星点
    {
        "func": "starlike",
        "label": "Starlike",
        "type": "topology",
        "defaultChecked": False,
        "tip": "是否存在星点"
    },
    # 重叠uv
    {
        "func": "self_penetrating_uv",
        "label": "Self Penetrating UV",
        "type": "UV",
        "defaultChecked": False,
        "tip": "是否存在自重叠UV"
    },
    # 丢失UV
    {
        "func": "missing_uv",
        "label": "Missing UV",
        "type": "UV",
        "defaultChecked": False,
        "tip": "是否丢失UV"
    },
    # 跨界uv
    {
        "func": "cross_border_uv",
        "label": "Cross Border UV",
        "type": "UV",
        "defaultChecked": False,
        "tip": "是否存在UV越界"
    },
    # uv范围
    {
        "func": "uv_range",
        "label": "UV Range",
        "type": "UV",
        "defaultChecked": False,
        "tip": "是否存在UV超出范围"
    },
    # 层级
    {
        'func': 'layers',
        'label': 'Layers',
        'type': 'general',
        'defaultChecked': False,
        "tip": "是否存在层级"
    },
    # 历史
    {
        'func': 'history',
        'label': 'History',
        'type': 'general',
        'defaultChecked': False,
        "tip": "是否存在未删除历史"
    },
    # 材质
    {
        'func': 'shaders',
        'label': 'Shaders',
        'type': 'general',
        'defaultChecked': False,
        "tip": "是否使用默认材质"
    },
    # 冻结变换
    {
        'func': 'unfrozen_transforms',
        'label': 'Unfrozen Transforms',
        'type': 'general',
        'defaultChecked': False,
        "tip": "是否未冻结变换"
    },
    # 中心枢轴
    {
        'func': 'uncentered_pivots',
        'label': 'Uncentered Pivots',
        'type': 'general',
        'defaultChecked': False,
        "tip": "是否未中心枢轴归零"
    },
    # 空组
    {
        'func': 'empty_groups',
        'label': 'Empty Groups',
        'type': 'general',
        'defaultChecked': False,
        "tip": "是否存在空组"
    },
]
