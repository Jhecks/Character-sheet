# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TraitEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TraitEdit(object):
    def setupUi(self, TraitEdit):
        TraitEdit.setObjectName("TraitEdit")
        TraitEdit.resize(332, 299)
        self.centralwidget = QtWidgets.QWidget(TraitEdit)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 6, 0, 1, 1)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.gridLayout.addWidget(self.deleteButton, 6, 1, 1, 1)
        self.notes = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.notes.setObjectName("notes")
        self.gridLayout.addWidget(self.notes, 5, 0, 1, 2)
        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 3, 0, 1, 2)
        self.type = QtWidgets.QLineEdit(self.centralwidget)
        self.type.setObjectName("type")
        self.gridLayout.addWidget(self.type, 1, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        TraitEdit.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TraitEdit)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 332, 21))
        self.menubar.setObjectName("menubar")
        TraitEdit.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TraitEdit)
        self.statusbar.setObjectName("statusbar")
        TraitEdit.setStatusBar(self.statusbar)

        self.retranslateUi(TraitEdit)
        QtCore.QMetaObject.connectSlotsByName(TraitEdit)

    def retranslateUi(self, TraitEdit):
        _translate = QtCore.QCoreApplication.translate
        TraitEdit.setWindowTitle(_translate("TraitEdit", "MainWindow"))
        self.label_2.setText(_translate("TraitEdit", "Name"))
        self.closeButton.setText(_translate("TraitEdit", "Close"))
        self.deleteButton.setText(_translate("TraitEdit", "Delete"))
        self.label_3.setText(_translate("TraitEdit", "Notes"))
        self.label.setText(_translate("TraitEdit", "Type"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TraitEdit = QtWidgets.QMainWindow()
    ui = Ui_TraitEdit()
    ui.setupUi(TraitEdit)
    TraitEdit.show()
    sys.exit(app.exec_())
