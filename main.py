import sys
import os

import tkinter
from tkinter import filedialog
from PyQt5 import QtWidgets
from enum import Enum

import CharacterSheet
import xmlParser

import qdarktheme


class Themes(Enum):
    dark = 0
    light = 1


class MainWindow(QtWidgets.QMainWindow, CharacterSheet.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.actualTheme = None
        self.setupUi(self)
        self.setDarkTheme()

        self.actionLight_theme_2.triggered.connect(self.setLightTheme)
        self.actionDark_theme_2.triggered.connect(self.setDarkTheme)
        self.menuFile.triggered.connect(self.selectFile)

    def setDarkTheme(self):
        qdarktheme.setup_theme()
        self.actionDark_theme_2.setChecked(True)
        self.actionLight_theme_2.setChecked(False)
        self.actualTheme = Themes.dark

    def setLightTheme(self):
        qdarktheme.setup_theme('light')
        self.actionDark_theme_2.setChecked(False)
        self.actionLight_theme.setChecked(True)
        self.actualTheme = Themes.light

    def selectFile(self):
        tkinter.Tk().withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        xmlParser.xml_parser(file_path)
        print(file_path)


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()

    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)


if __name__ == '__main__':
    main()
