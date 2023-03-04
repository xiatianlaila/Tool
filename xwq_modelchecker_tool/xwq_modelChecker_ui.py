# -*- coding: UTF-8 -*-
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from shiboken2 import wrapInstance
from functools import partial

import sys
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import xwq_modelchecker_tool.xwq_modelchecker_list as mcl
reload(mcl)
import xwq_modelchecker_tool.xwq_modelchecker_func as mfunc
reload(mfunc)


def maya_main_window():
    '''
    Returns:返回Maya主窗口作为Python对象
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class ModelCheckerDialog(QtWidgets.QMainWindow):
    version = '1.0.0'
    # 获取文件中储存的列表
    commands_list = mcl.mcCommandsList
    # Initializes a new, empty MSelectionList object
    selection_mesh_list = om.MSelectionList()
    # 声明
    type_widget = {}
    type_layout = {}
    type_header_layout = {}
    type_button = {}
    collapse_button = {}

    command = {}
    command_widget = {}
    command_layout = {}
    command_label = {}
    command_checkbox = {}
    command_run_button = {}
    select_error_nodes_button = {}

    def __init__(self, parent=maya_main_window()):
        super(ModelCheckerDialog, self).__init__(parent)

        self.setWindowTitle("模型检查工具" + " " + self.version)
        # 根据不同平台进行不同的配置
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)  # 删除 ‘？’ 号
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setMinimumSize(350, 710)
        self.setMaximumSize(800, 710)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.select_label = QtWidgets.QLabel("模型名称:")
        self.select_lineedit = QtWidgets.QLineEdit("")
        self.select_lineedit.setReadOnly(True)
        self.select_button = QtWidgets.QPushButton("选 择")

        self.report_label = QtWidgets.QLabel("输出日志 :")
        self.report_output_textedit = QtWidgets.QTextEdit()

        self.report_clear_button = QtWidgets.QPushButton("清 空")
        self.report_run_all_checked_button = QtWidgets.QPushButton("Run All Checked")

        self.check_all_button = QtWidgets.QPushButton("全 选")
        self.uncheck_all_button = QtWidgets.QPushButton("全 不 选")
        self.invert_check_button = QtWidgets.QPushButton("反 选")

        self.report_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.select_label.setStyleSheet("font-size: 12px; font-weight:450;")
        self.report_output_textedit.setStyleSheet("background-color: #1e1f22; font-size: 15px")
        self.select_button.setStyleSheet("background-color: #5662e8; color: #ffffff; font-size: 12px;")
        self.report_clear_button.setStyleSheet("background-color: #5662e8; color: #ffffff; font-size: 12px;")
        self.report_run_all_checked_button.setStyleSheet("background-color: #5662e8; color: #ffffff; font-size: 12px;")
        self.check_all_button.setStyleSheet("background-color: #5662e8; color: #ffffff; font-size: 12px;")
        self.uncheck_all_button.setStyleSheet("background-color: #5662e8; color: #ffffff; font-size: 12px;")
        self.invert_check_button.setStyleSheet("background-color: #5662e8; color: #ffffff; font-size: 12px;")

    def create_layouts(self):
        # 使用一个作为所有这些其他窗口部件父对象的QWidget，以及通过使用布局管理器管理这些子窗口部件的大小和位置
        main_layout = QtWidgets.QWidget(self)
        self.setCentralWidget(main_layout)

        columns_layout = QtWidgets.QHBoxLayout(main_layout)
        report_layout = QtWidgets.QVBoxLayout()
        checks_layout = QtWidgets.QVBoxLayout()

        columns_layout.addLayout(checks_layout)
        columns_layout.addLayout(report_layout)

        select_layout = QtWidgets.QHBoxLayout()
        checks_layout.addLayout(select_layout)

        self.select_label.setMaximumWidth(60)
        self.select_lineedit.setMaximumWidth(200)
        self.select_lineedit.setPlaceholderText("请选择需要检查的模型")
        self.select_lineedit.setStyleSheet("background-color: #1e1f22")
        self.select_button.setMaximumWidth(60)

        select_layout.addWidget(self.select_label)
        select_layout.addWidget(self.select_lineedit)
        select_layout.addWidget(self.select_button)

        report_second_layout = QtWidgets.QHBoxLayout()
        report_second_layout.addWidget(self.report_label)
        report_layout.addLayout(report_second_layout)

        self.report_clear_button.setMaximumWidth(150)
        report_second_layout.addWidget(self.report_clear_button)

        self.report_output_textedit.setMaximumWidth(600)
        report_layout.addWidget(self.report_output_textedit)
        report_layout.addWidget(self.report_run_all_checked_button)

        self.resize(800, 710)

        types = self.get_types(self.commands_list)
        # 根据types创建weight
        for i in types:
            self.type_widget[i] = QtWidgets.QWidget()
            self.type_layout[i] = QtWidgets.QVBoxLayout()
            self.type_header_layout[i] = QtWidgets.QHBoxLayout()
            self.type_button[i] = QtWidgets.QPushButton(i)
            # 如果sys.version_info.major返回值是2 使用的是Py2 如果是3 使用的是Py3
            if sys.version_info.major >= 3:
                # 特殊字符
                text = '\u2193'
            else:
                text = u'\u2193'.encode('utf-8')
            self.collapse_button[i] = QtWidgets.QPushButton(text)
            self.collapse_button[i].setStyleSheet("background-color: #404249;")
            self.collapse_button[i].setMaximumWidth(30)
            self.collapse_button[i].clicked.connect(partial(self.toggle_ui, i))
            self.type_button[i].setStyleSheet(
                "background-color: #3a406e; text-transform: uppercase; color: #c9cdfb; font-size: 18px; font-weight:550;")
            self.type_button[i].clicked.connect(partial(self.check_by_types, i))
            self.type_header_layout[i].addWidget(self.type_button[i])
            self.type_header_layout[i].addWidget(self.collapse_button[i])
            self.type_widget[i].setLayout(self.type_layout[i])
            checks_layout.addLayout(self.type_header_layout[i])
            checks_layout.addWidget(self.type_widget[i])

        # 创建button
        for i in self.commands_list:
            name = i["func"]
            label = i["label"]
            types = i["type"]
            tip = i["tip"]
            checkeval = i["defaultChecked"]

            self.command_widget[name] = QtWidgets.QWidget()
            self.command_widget[name].setMaximumHeight(40)
            self.command_layout[name] = QtWidgets.QHBoxLayout()

            self.type_layout[types].addWidget(self.command_widget[name])
            self.command_widget[name].setLayout(self.command_layout[name])
            # 设置部件的相邻距离
            self.command_layout[name].setSpacing(5)
            self.command_layout[name].setContentsMargins(0, 0, 0, 0)
            # 设置内外边距
            self.command_widget[name].setStyleSheet("padding: 0px; margin: 0px;")
            self.command = name
            self.command_label[name] = QtWidgets.QLabel(label)
            self.command_label[name].setMinimumWidth(125)
            self.command_label[name].setToolTip(tip)
            self.command_label[name].setStyleSheet("QLabel{font-size: 12px;}" "QToolTip{background-color: #fff; font-size: 13px;}")

            self.command_checkbox[name] = QtWidgets.QCheckBox()
            self.command_checkbox[name].setStyleSheet("background-color: #ffffff; color: #000000")
            self.command_checkbox[name].setChecked(checkeval)
            self.command_checkbox[name].setMinimumWidth(13)

            self.command_run_button[name] = QtWidgets.QPushButton("Run")
            self.command_run_button[name].setStyleSheet("background-color: #5662e8; color: #ffffff;")
            self.command_run_button[name].setMinimumWidth(30)

            self.command_run_button[name].clicked.connect(partial(self.run_func, [i]))

            self.select_error_nodes_button[name] = QtWidgets.QPushButton("Select Error Nodes")
            # 设置为不可按
            self.select_error_nodes_button[name].setEnabled(False)
            self.select_error_nodes_button[name].setMinimumWidth(150)

            self.command_layout[name].addWidget(self.command_label[name])
            self.command_layout[name].addWidget(self.command_checkbox[name])
            self.command_layout[name].addWidget(self.command_run_button[name])
            self.command_layout[name].addWidget(self.select_error_nodes_button[name])
        # 平均分配Layout
        checks_layout.addStretch()

        checks_button_layout = QtWidgets.QHBoxLayout()
        checks_layout.addLayout(checks_button_layout)

        checks_button_layout.addWidget(self.check_all_button)
        checks_button_layout.addWidget(self.uncheck_all_button)
        checks_button_layout.addWidget(self.invert_check_button)

    def create_connections(self):
        self.select_button.clicked.connect(self.set_top_node)
        self.check_all_button.clicked.connect(self.check_all)
        self.uncheck_all_button.clicked.connect(self.uncheck_all)
        self.invert_check_button.clicked.connect(self.invert_check)
        self.report_run_all_checked_button.clicked.connect(self.sanity_check)
        self.report_clear_button.clicked.connect(self.report_output_textedit.clear)

    def get_types(self, input_list):
        all_types = []
        for i in input_list:
            all_types.append(i["type"])
        # 使用集合储存去除重复元素
        output_list = list(set(all_types))
        # 排序
        output_list.sort(reverse=True)
        a = output_list.pop(1)
        output_list.insert(2, a)
        return output_list

    def set_top_node(self):
        selection = cmds.ls(selection=True)
        self.select_lineedit.setText(selection[0])

    # 返回checkBox当前勾选状态
    def check_state(self):
        return self.command_checkbox[name].checkState()

    # 全选
    def check_all(self):
        for i in self.commands_list:
            name = i["func"]
            self.command_checkbox[name].setChecked(True)

    # 全不选
    def uncheck_all(self):
        for i in self.commands_list:
            name = i["func"]
            self.command_checkbox[name].setChecked(False)

    # 反选
    def invert_check(self):
        for i in self.commands_list:
            name = i["func"]
            self.command_checkbox[name].setChecked(not self.command_checkbox[name].isChecked())

    # 根据type选择
    def check_by_types(self, check_types):
        # 声明两个列表存储checkbox总数和已被勾选的数量
        checked_type_boxs_number = []
        type_boxs_number_number = []

        for i in self.commands_list:
            name = i["func"]
            types = i["type"]
            if types == check_types:
                type_boxs_number_number.append(name)
                if self.command_checkbox[name].isChecked():
                    checked_type_boxs_number.append(name)

        # 如果两个列表元素数量相等的话就全部设置为False，否则为True
        for i in type_boxs_number_number:
            if len(checked_type_boxs_number) == len(type_boxs_number_number):
                self.command_checkbox[i].setChecked(False)
            else:
                self.command_checkbox[i].setChecked(True)

    # 切换折叠UI
    def toggle_ui(self, i):
        # 利用widget组件的Visible属性设置
        state = self.type_widget[i].isVisible()

        if state:
            # 切换按钮样式
            if sys.version_info.major >= 3:
                text = u'\u21B5'
            else:
                text = u'\u21B5'.encode('utf-8')
            self.collapse_button[i].setText(text)
            self.type_widget[i].setVisible(not state)
            # 根据内容自适应大小
            # self.adjustSize()
        else:
            # 切换按钮样式
            if sys.version_info.major >= 3:
                text = u'\u2193'
            else:
                text = u'\u2193'.encode('utf-8')
            self.collapse_button[i].setText(text)
            self.type_widget[i].setVisible(not state)

    # 过滤节点
    def filter_nodes(self):
        nodes = []
        # 清空
        self.selection_mesh_list.clear()
        useful_nodes = []
        # 获取所有的transform对象
        all_nodes = cmds.ls(transforms=True)
        # 去除摄像机的transform
        for i in all_nodes:
            if not i in {"front", "persp", "top", "side"}:
                useful_nodes.append(i)

        selection = cmds.ls(selection=True)
        top_node = self.select_lineedit.text()
        if len(selection) > 0:
            nodes = selection
        elif self.select_lineedit.text() == "":
            nodes = useful_nodes
        else:
            # 判断给定的节点是否存在
            if cmds.objExists(top_node):
                # 获取此节点的所有子节点
                nodes = cmds.listRelatives(top_node, allDescendents=True, type="transform")
                print (nodes)
                # 没有子节点就等于top node
                if not nodes:
                    nodes = top_node
                nodes.append(top_node)
            # 不存在在Report栏中打印经过警告
            else:
                warning_output_text = "Object in Top Node doesn't exists\n"
                self.report_output_textedit.clear()
                # insertPlainText方法不会自动清空
                self.report_output_textedit.insertPlainText(warning_output_text)

        for node in nodes:
            # 获取所有dag节点的shape子节点
            shapes = cmds.listRelatives(node, shapes=True, type="mesh")
            # 将所有shape节点添加到列表
            if shapes:
                self.selection_mesh_list.add(node)
        return nodes

    # 运行函数
    def run_func(self, funcs):
        nodes = self.filter_nodes()
        self.report_output_textedit.clear()
        if len(nodes) == 0:
            self.report_output_textedit.insertPlainText("警告 - 没有节点可检查")
        else:
            for i in funcs:
                func = i["func"]
                label = i["label"]
                # 得到对应的函数并执行
                self.error_nodes = getattr(mfunc, func)(nodes, self.selection_mesh_list)

                if self.error_nodes:
                    self.report_output_textedit.insertHtml(
                        label + " -- <font color='#f23f43'>FAILED</font><br>"
                    )
                    for obj in self.error_nodes:
                        self.report_output_textedit.insertPlainText(
                            "    " + obj + "\n"
                        )
                    # 将错误节点对应的按钮设置为可按
                    self.select_error_nodes_button[func].setEnabled(True)
                    self.select_error_nodes_button[func].clicked.connect(partial(self.selection_error_nodes, self.error_nodes))
                    self.select_error_nodes_button[func].setStyleSheet("background-color: #404249;")
                    self.command_label[func].setStyleSheet("background-color: #f23f43; font-size: 12px;")
                else:
                    self.command_label[func].setStyleSheet("background-color: #248045; font-size: 12px;")
                    self.report_output_textedit.insertHtml(
                        label + " -- <font color='#248045'>SUCCESS</font><br>"
                    )
                    self.select_error_nodes_button[func].setEnabled(False)


    # 检查勾选框
    def sanity_check(self):
        self.report_output_textedit.clear()
        checked_funcs = []
        for i in self.commands_list:
            name = i["func"]
            if self.command_checkbox[name].isChecked():
                checked_funcs.append(i)
            else:
                self.command_label[name].setStyleSheet("background-color: none; font-size: 12px;")
                self.select_error_nodes_button[name].setStyleSheet("background-color: #2e3035;")
                self.select_error_nodes_button[name].setEnabled(False)
        if len(checked_funcs) == 0:
            print("您没有选择需要检查的项目!".decode('utf-8'))
            self.report_output_textedit.insertHtml("您没有选择需要检查的项目!".decode('utf-8'))
        else:
            self.run_func(checked_funcs)

    def selection_error_nodes(self, list):
        cmds.select(list)


if __name__ == "__main__":

    try:
        modelChecker_dialog.close()  # 关闭窗口
        modelChecker_dialog.deleteLater()  # 删除窗口
    except:
        pass
    modelChecker_dialog = ModelCheckerDialog()
    modelChecker_dialog.show()
    modelChecker_dialog.setStyleSheet("background-color: #2e3035;")
