from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton

from PyUi_Files.AddSpell import Ui_AddSpellData
from PyUi_Files.AddTraitOrFeat import Ui_AddTraitOrFeatData
from PyUi_Files.EditSpell import Ui_EditSpellData
from PyUi_Files.EditTraitOrFeat import Ui_EditTraitOrFeatData

import requests
from bs4 import BeautifulSoup


def addOrEditSpell(self):
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_AddSpellData()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Add Spell')

    self.ui.inputHTML.textChanged.connect(self.addOrEdit_changeHtml)
    self.ui.displayData.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
    self.ui.displayData.setOpenLinks(False)

    self.ui.search.clicked.connect(self.addOrEdit_search)

    self.ui.school.addItems(self.spell_data.spell_schools)
    self.ui.school.setCurrentText('')
    self.ui.subschool.addItems(self.spell_data.spell_subschools)
    self.ui.subschool.setCurrentText('')

    self.ui.save.clicked.connect(self.addOrEditSpell_save)

    self.window.show()


def check_web_site(self, url):
    if 'www.d20pfsrd.com' in url:
        response = requests.get(url)
        if response.status_code == 404:
            return '404'

        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', class_='page-center')

        soup_string = str(div)
        soup_string = soup_string[soup_string.find('<h1>'):]
        soup_string = soup_string[:soup_string.find('<div class="section15">')]

        new_soap = BeautifulSoup(soup_string, 'html.parser')
        return new_soap

    elif 'www.aonprd.com' in url:
        return 'aon'
    else:
        return 'other'


def addOrEdit_search(self):
    url = self.ui.url.text()
    new_soap = self.check_web_site(url)
    if new_soap == '404':
        self.addOrEdit_show_error()
        return
    self.ui.inputHTML.setPlainText(new_soap.prettify())
    self.ui.displayData.setHtml(new_soap.prettify())


def addOrEdit_changeHtml(self):
    self.ui.displayData.setHtml(self.ui.inputHTML.toPlainText())


def addOrEditSpell_save(self):
    if self.ui.displayData.toPlainText() == '':
        self.window.close()
        return
    if self.ui.name.text() == '' or self.ui.school.currentText() == '':
        self.addOrEditSpell_show_warning()
        return
    if self.ui.subschool.currentText() == '':
        if self.addOrEditSpell_show_warning_subschool() == 'Edit':
            return

    keys = ['name', 'school', 'subschool', 'full_text']
    input_data = [self.ui.name.text().rstrip(), self.ui.school.currentText(),
                  self.ui.subschool.currentText(), str(self.ui.inputHTML.toPlainText()).replace('\n', '')]
    input_data_dict = dict(zip(keys, input_data))
    self.spell_data.update_spell_data(input_data_dict)
    self.window.close()


def addOrEditSpell_show_warning(self):
    msg = QMessageBox()
    msg.setWindowIcon(QtGui.QIcon(self.icon_path))
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please add/or name and school of the spell")
    msg.setWindowTitle("Warning")
    msg.exec_()


def addOrEditSpell_show_warning_subschool(self):
    msg = QMessageBox()
    msg.setWindowIcon(QtGui.QIcon(self.icon_path))
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please check if this spell doesn't have a subschool\n"
                "Usually it is indicated in parentheses after the name of the school")
    msg.setWindowTitle("Warning")

    sure_button = QPushButton('I am sure')
    edit_button = QPushButton('Edit spell')

    msg.addButton(sure_button, QMessageBox.AcceptRole)
    msg.addButton(edit_button, QMessageBox.RejectRole)
    msg.setWindowModality(Qt.ApplicationModal)
    result = msg.exec_()

    if result == QMessageBox.AcceptRole:
        return 'Approve'
    elif result == QMessageBox.RejectRole:
        return 'Edit'


def addOrEdit_show_error(self):
    msg = QMessageBox()
    msg.setWindowIcon(QtGui.QIcon(self.icon_path))
    msg.setIcon(QMessageBox.Critical)
    msg.setText("404 Page Not Found\nTry another link or check the link you've entered")
    msg.setWindowTitle("Error")
    msg.exec_()


def addOrEditFeat(self):
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_AddTraitOrFeatData()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Add Feat')
    self.ui.inputHTML.textChanged.connect(self.addOrEdit_changeHtml)
    self.ui.displayData.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
    self.ui.displayData.setOpenLinks(False)

    self.ui.search.clicked.connect(self.addOrEdit_search)

    self.ui.type.addItems(self.spell_data.feat_types)
    self.ui.type.setEditable(True)
    self.ui.type.setCurrentText('')
    self.ui.source.addItems(self.spell_data.feat_sources)
    self.ui.source.setEditable(True)
    self.ui.source.setCurrentText('')


    self.ui.save.clicked.connect(self.addOrEditFeat_save)

    self.window.show()


def addOrEditFeat_save(self):
    if self.ui.displayData.toPlainText() == '':
        self.window.close()
        return
    if self.ui.name.text() == '' or self.ui.type.currentText() == '':
        self.addOrEditFeat_show_warning()
        return

    keys = ['name', 'type', 'full_text']
    input_data = [self.ui.name.text().rstrip(), self.ui.type.currentText(),
                  str(self.ui.inputHTML.toPlainText()).replace('\n', '')]
    input_data_dict = dict(zip(keys, input_data))
    self.spell_data.update_feat_data(input_data_dict)
    self.window.close()


def addOrEditFeat_show_warning(self):
    msg = QMessageBox()
    msg.setWindowIcon(QtGui.QIcon(self.icon_path))
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please add/or name and type of the feat")
    msg.setWindowTitle("Warning")
    msg.exec_()


def addOrEditTrait(self):
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_AddTraitOrFeatData()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Add Trait')
    self.ui.inputHTML.textChanged.connect(self.addOrEdit_changeHtml)
    self.ui.displayData.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
    self.ui.displayData.setOpenLinks(False)

    self.ui.search.clicked.connect(self.addOrEdit_search)

    self.ui.type.addItems(self.spell_data.trait_types)
    self.ui.type.setEditable(True)
    self.ui.type.setCurrentText('')

    self.ui.save.clicked.connect(self.addOrEditTrait_save)

    self.window.show()


def addOrEditTrait_save(self):
    if self.ui.displayData.toPlainText() == '':
        self.window.close()
        return
    if self.ui.name.text() == '' or self.ui.type.currentText() == '':
        self.addOrEditTrait_show_warning()
        return

    keys = ['name', 'type', 'full_text']
    input_data = [self.ui.name.text().rstrip(), self.ui.type.currentText(),
                  str(self.ui.inputHTML.toPlainText()).replace('\n', '')]
    input_data_dict = dict(zip(keys, input_data))
    self.spell_data.update_trait_data(input_data_dict)
    self.window.close()


def addOrEditTrait_show_warning(self):
    msg = QMessageBox()
    msg.setWindowIcon(QtGui.QIcon(self.icon_path))
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please add/or name and type of the trait")
    msg.setWindowTitle("Warning")
    msg.exec_()


def editSpellData(self):
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_EditSpellData()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Edit Spell')

    self.ui.name.setEditable(True)
    self.ui.name.addItems(self.spell_data.spell_names)
    self.ui.name.setCurrentText('')
    self.ui.school.addItems(self.spell_data.spell_schools)
    self.ui.school.setCurrentText('')
    self.ui.subschool.addItems(self.spell_data.spell_subschools)
    self.ui.subschool.setCurrentText('')
    self.ui.displayData.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
    self.ui.displayData.setOpenLinks(False)

    self.ui.search.clicked.connect(self.addOrEdit_search)
    self.ui.inputHTML.textChanged.connect(self.addOrEdit_changeHtml)

    self.ui.name.currentIndexChanged.connect(lambda: self.editSpellData_name_updated(self.ui.name.currentIndex(),
                                                                                     self.ui.name.currentText()))
    self.ui.save.clicked.connect(lambda: self.editSpellData_save())
    self.ui.delete_2.clicked.connect(lambda: self.editSpellData_delete())

    self.window.show()


def editSpellData_name_updated(self, spell_name_index, text):
    data = self.spell_data.get_spell_data_from_index(spell_name_index)
    self.ui.name.setCurrentText(data['name'])
    self.ui.school.setCurrentText(data['school'])
    self.ui.subschool.setCurrentText(data['subschool'])
    self.ui.inputHTML.setPlainText(data['description'])
    self.ui.displayData.setHtml(data['description'])


def editSpellData_save(self):
    if self.ui.displayData.toPlainText() == '':
        self.window.close()
        return
    if self.ui.name.currentText() == '' or self.ui.school.currentText() == '':
        self.addOrEditSpell_show_warning()
        return
    if self.ui.subschool.currentText() == '':
        if self.addOrEditSpell_show_warning_subschool() == 'Edit':
            return

    keys = ['name', 'school', 'subschool', 'full_text']
    input_data = [self.ui.name.currentText().rstrip(), self.ui.school.currentText(),
                  self.ui.subschool.currentText(), str(self.ui.inputHTML.toPlainText()).replace('\n', '')]
    input_data_dict = dict(zip(keys, input_data))
    self.spell_data.update_spell_data(input_data_dict, update=True)
    self.window.close()
