# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TraitEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TraitEdit(object):
    def setupUi(self, TraitEdit):
        TraitEdit.setObjectName("TraitEdit")
        TraitEdit.resize(420, 450)
        self.centralwidget = QtWidgets.QWidget(TraitEdit)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 2)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.gridLayout.addWidget(self.deleteButton, 9, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 2)
        self.name = QtWidgets.QComboBox(self.centralwidget)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 2, 0, 1, 2)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 9, 0, 1, 1)
        self.notes = QtWidgets.QTextBrowser(self.centralwidget)
        self.notes.setObjectName("notes")
        self.gridLayout.addWidget(self.notes, 8, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.type = QtWidgets.QLineEdit(self.centralwidget)
        self.type.setObjectName("type")
        self.gridLayout.addWidget(self.type, 4, 0, 1, 2)
        self.source = QtWidgets.QLineEdit(self.centralwidget)
        self.source.setObjectName("source")
        self.gridLayout.addWidget(self.source, 6, 0, 1, 2)
        TraitEdit.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TraitEdit)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 420, 21))
        self.menubar.setObjectName("menubar")
        self.menuChange_source = QtWidgets.QMenu(self.menubar)
        self.menuChange_source.setObjectName("menuChange_source")
        TraitEdit.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TraitEdit)
        self.statusbar.setObjectName("statusbar")
        TraitEdit.setStatusBar(self.statusbar)
        self.actionISO = QtWidgets.QAction(TraitEdit)
        self.actionISO.setObjectName("actionISO")
        self.menubar.addAction(self.menuChange_source.menuAction())

        self.retranslateUi(TraitEdit)
        QtCore.QMetaObject.connectSlotsByName(TraitEdit)
        TraitEdit.setTabOrder(self.name, self.notes)
        TraitEdit.setTabOrder(self.notes, self.closeButton)
        TraitEdit.setTabOrder(self.closeButton, self.deleteButton)

    def retranslateUi(self, TraitEdit):
        _translate = QtCore.QCoreApplication.translate
        TraitEdit.setWindowTitle(_translate("TraitEdit", "MainWindow"))
        self.label_3.setText(_translate("TraitEdit", "Notes"))
        self.deleteButton.setText(_translate("TraitEdit", "Delete"))
        self.label_4.setText(_translate("TraitEdit", "Source"))
        self.closeButton.setText(_translate("TraitEdit", "Close"))
        self.label_2.setText(_translate("TraitEdit", "Name"))
        self.label.setText(_translate("TraitEdit", "Type"))
        self.menuChange_source.setTitle(_translate("TraitEdit", "Change source"))
        self.actionISO.setText(_translate("TraitEdit", "ISO"))
