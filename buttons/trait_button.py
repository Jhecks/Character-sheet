from PyQt5.QtWidgets import QMessageBox

from PyUi_Files.TraitEdit import Ui_TraitEdit
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFontMetrics


def add_trait(self, trait=None, button_clicked=False):
    gridLayout = self.gridLayout_26
    self.traitCount += 1
    self.traitIndex += 1
    new_position = ((self.traitCount - 1) // 5 + 1, (self.traitCount - 1) % 5 + 2)
    name = f'button №{self.traitIndex}'
    button = QtWidgets.QPushButton(self.widget_2)
    button.setObjectName(name)
    if trait:
        button_text = f"{trait.name}"
    else:
        button_text = 'Click me'

    font_metrics = QFontMetrics(button.font())
    text_width = font_metrics.width(button_text)
    button_width = button.width()

    if text_width > button_width:
        button.setStyleSheet("QPushButton { text-align: left; } "
                             "QToolTip { color: #ffffff; background-color: #000000; border: 1px solid white; }")
        button.setToolTip(button_text)
    button.setText(button_text)
    gridLayout.addWidget(button, new_position[0], new_position[1])
    button.clicked.connect(self.clicked_trait_button)
    self.traitList.append(button)
    if button_clicked:
        self.data_frame.traits.add_trait()
        button.click()


def clicked_trait_button(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.traitList)):
        if self.traitList[i].objectName() == object_name:
            index = i
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_TraitEdit()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Edit Trait')

    self.ui.name.setEditable(True)
    self.ui.name.addItems(self.spell_data.trait_names)
    self.ui.name.setCurrentText(self.data_frame.traits.list[index].name)
    self.ui.type.setReadOnly(True)
    self.ui.type.setText(self.data_frame.traits.list[index].type)
    self.ui.source.setReadOnly(True)
    self.ui.source.setText(self.data_frame.traits.list[index].source)
    self.ui.notes.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
    self.ui.notes.setOpenLinks(False)
    self.ui.notes.setHtml(self.data_frame.traits.list[index].notes)

    self.ui.name.currentIndexChanged.connect(
        lambda: self.trait_name_updated(self.ui.name.currentIndex(), index, self.ui.name.currentText()))
    self.ui.source.textChanged.connect(
        lambda: self.trait_source_updated(self.ui.name.currentIndex(), index, self.ui.source.text()))
    self.ui.closeButton.clicked.connect(lambda: self.window.close())
    self.ui.deleteButton.clicked.connect(lambda: self.trait_delete(index))

    position = self.pos()
    position.setX(self.pos().x() + 280)
    position.setY(self.pos().y() + 370)
    self.window.move(position)
    self.window.show()


def trait_name_updated(self, trait_name_index, index, text):
    data = self.spell_data.get_trait_data_from_index(trait_name_index)
    self.data_frame.traits.list[index].name = text
    actions = self.ui.menuChange_source.actions()
    for action in actions:
        self.ui.menuChange_source.removeAction(action)
    if data:
        if type(data['source']) is list:
            i = 0
            if self.ui.source.text() in data['source']:
                i = data['source'].index(self.ui.source.text())
            self.ui.type.setText(data['type'][i])
            self.ui.source.setText(data['source'][i])
            self.ui.notes.setHtml(data['description'][i])
            self.data_frame.traits.list[index].type = data['type'][i]
            self.data_frame.traits.list[index].source = data['source'][i]
            self.data_frame.traits.list[index].notes = data['description'][i]

            for source_data in data['source']:
                action = QtWidgets.QAction(source_data, self)
                self.ui.menuChange_source.addAction(action)
                action.triggered.connect(lambda checked, text=source_data: self.ui.source.setText(text))
        else:
            self.ui.type.setText(data['type'])
            self.ui.source.setText(data['source'])
            self.ui.notes.setHtml(data['description'])
            self.data_frame.traits.list[index].type = data['type']
            self.data_frame.traits.list[index].source = data['source']
            self.data_frame.traits.list[index].notes = data['description']

    font_metrics = QFontMetrics(self.traitList[index].font())
    text_width = font_metrics.width(self.data_frame.traits.list[index].name)
    button_width = self.traitList[index].width()

    if text_width > button_width:
        self.traitList[index].setStyleSheet(
            self.traitList[index].styleSheet() + " " + "QPushButton { text-align: left; } "
                                                       "QToolTip { color: #ffffff; background-color: #000000; border: 1px solid white; }")
        self.traitList[index].setToolTip(self.data_frame.traits.list[index].name)
    self.traitList[index].setText(f'{self.data_frame.traits.list[index].name}')
    print(f'{self.data_frame.traits.list[index].name}\n'
          f'{self.data_frame.traits.list[index].type}\n'
          f'{self.data_frame.traits.list[index].source}\n'
          f'{self.data_frame.traits.list[index].notes}')


def trait_source_updated(self, trait_name_index, index, text):
    data = self.spell_data.get_trait_data_from_index(trait_name_index)
    for i in range(len(data['source'])):
        if data['source'][i] == text:
            self.ui.type.setText(data['type'][i])
            self.ui.notes.setHtml(data['description'][i])
    self.data_frame.traits.list[index].source = text
    self.data_frame.traits.list[index].description = self.ui.notes.toHtml()


def trait_delete(self, index, reset=False):
    grid_layout = self.gridLayout_26
    self.data_frame.traits.delete_traits([index])
    if not reset:
        self.window.close()
    grid_layout.removeWidget(self.traitList[index])
    self.traitList[index].deleteLater()
    del self.traitList[index]
    self.reset_traits_positions()
    self.traitCount -= 1


def reset_traits_positions(self):
    gridLayout = self.gridLayout_26
    index = 0
    for button in self.traitList:
        index += 1
        new_position = (((index - 1) // 5) + 1, ((index - 1) % 5) + 2)
        gridLayout.removeWidget(button)
        gridLayout.addWidget(button, new_position[0], new_position[1])
