from PyUi_Files.AbilityEdit import Ui_AbilityEdit
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics


def add_ability(self, ability=None, button_clicked=False):
    gridLayout = self.gridLayout_11
    self.abilityCount += 1
    self.abilityIndex += 1
    new_position = ((self.abilityCount - 1) // 5 + 1, (self.abilityCount - 1) % 5 + 2)
    name = f'button №{self.abilityIndex}'
    button = QtWidgets.QPushButton(self.widget)
    button.setObjectName(name)
    button_text = ''
    if ability:
        if ability.name or ability.type:
            button_text = f"{ability.name}"
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
    button.clicked.connect(self.clicked_ability_button)
    self.abilityList.append(button)
    if button_clicked:
        self.data_frame.specialAbilities.add_special_ability()
        button.click()


def clicked_ability_button(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.abilityList)):
        if self.abilityList[i].objectName() == object_name:
            index = i
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_AbilityEdit()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Edit Special Ability')

    self.ui.name.setText(self.data_frame.specialAbilities.list[index].name)
    self.ui.type.setText(self.data_frame.specialAbilities.list[index].type)
    self.ui.notes.setPlainText(self.data_frame.specialAbilities.list[index].notes)

    self.ui.name.textEdited.connect(lambda: self.ability_name_updated(index))
    self.ui.type.textEdited.connect(lambda: self.ability_type_updated(index))
    self.ui.notes.textChanged.connect(lambda: self.ability_notes_updated(index))
    self.ui.closeButton.clicked.connect(lambda: self.window.close())
    self.ui.deleteButton.clicked.connect(lambda: self.ability_delete(index))

    self.window.show()
    position = self.pos()
    position.setX(self.pos().x() + 280)
    position.setY(self.pos().y() + 370)
    self.window.move(position)


def ability_name_updated(self, index):
    self.data_frame.specialAbilities.list[index].name = self.sender().text()
    font_metrics = QFontMetrics(self.abilityList[index].font())
    text_width = font_metrics.width(self.data_frame.specialAbilities.list[index].name)
    button_width = self.abilityList[index].width()

    if text_width > button_width:
        self.abilityList[index].setStyleSheet(
            self.abilityList[index].styleSheet() + " " + "QPushButton { text-align: left; } "
                                                         "QToolTip { color: #ffffff; background-color: #000000; border: 1px solid white; }")
        self.abilityList[index].setToolTip(self.data_frame.specialAbilities.list[index].name)
    self.abilityList[index].setText(f'{self.data_frame.specialAbilities.list[index].name}')


def ability_type_updated(self, index):
    self.data_frame.specialAbilities.list[index].type = self.sender().text()


def ability_notes_updated(self, index):
    self.data_frame.specialAbilities.list[index].notes = self.sender().toPlainText()


def ability_delete(self, index, reset=False):
    grid_layout = self.gridLayout_11
    self.data_frame.specialAbilities.delete_special_ability([index])
    if not reset:
        self.window.close()
    grid_layout.removeWidget(self.abilityList[index])
    self.abilityList[index].deleteLater()
    del self.abilityList[index]
    self.reset_abilities_positions()
    self.abilityCount -= 1


def reset_abilities_positions(self):
    gridLayout = self.gridLayout_11
    index = 0
    for button in self.abilityList:
        index += 1
        new_position = (((index - 1) // 5) + 1, ((index - 1) % 5) + 2)
        gridLayout.removeWidget(button)
        gridLayout.addWidget(button, new_position[0], new_position[1])
