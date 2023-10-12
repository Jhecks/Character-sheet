# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CharacterSheet.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(780, 0, 20, 551))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 0, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Forte")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 40, 781, 511))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTheme = QtWidgets.QMenu(self.menubar)
        self.menuTheme.setObjectName("menuTheme")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSelect_file = QtWidgets.QAction(MainWindow)
        self.actionSelect_file.setObjectName("actionSelect_file")
        self.actionLight_theme_2 = QtWidgets.QAction(MainWindow)
        self.actionLight_theme_2.setCheckable(True)
        self.actionLight_theme_2.setObjectName("actionLight_theme_2")
        self.actionLight_theme = QtWidgets.QAction(MainWindow)
        self.actionLight_theme.setObjectName("actionLight_theme")
        self.actionDark_theme_2 = QtWidgets.QAction(MainWindow)
        self.actionDark_theme_2.setCheckable(True)
        self.actionDark_theme_2.setObjectName("actionDark_theme_2")
        self.menuFile.addAction(self.actionSelect_file)
        self.menuTheme.addAction(self.actionLight_theme_2)
        self.menuTheme.addAction(self.actionDark_theme_2)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTheme.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Character sheet"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTheme.setTitle(_translate("MainWindow", "Settings"))
        self.actionSelect_file.setText(_translate("MainWindow", "Select file"))
        self.actionLight_theme_2.setText(_translate("MainWindow", "Light theme"))
        self.actionLight_theme.setText(_translate("MainWindow", "Light theme"))
        self.actionDark_theme_2.setText(_translate("MainWindow", "Dark theme"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())