from PyUi_Files.SpellLikeEdit import Ui_SpellLikeEdit
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics


def add_spell_like(self, spell=None, button_clicked=False):
    gridLayout = self.gridLayout_10
    self.spellLikeCount += 1
    self.spellLikeIndex += 1
    new_position = (((self.spellLikeCount - 1) // 7) + 1, ((self.spellLikeCount - 1) % 7) + 1)
    name = 'button № {}'.format(self.spellLikeIndex)
    button = QtWidgets.QPushButton(self.groupBox_14)
    button.setObjectName(name)
    if spell:
        if spell.prepared:
            button_text = f"{spell.name} ({spell.cast}/{spell.prepared})"
        else:
            button_text = f"{spell.name}"
        if spell.marked:
            button.setStyleSheet("QPushButton"
                                 "{"
                                 "background-color : grey;"
                                 "}")
    else:
        button_text = 'Click me'

    font_metrics = QFontMetrics(button.font())
    text_width = font_metrics.width(button_text)
    button_width = button.width()

    if text_width > button_width:
        button.setStyleSheet(button.styleSheet() + " " + "QPushButton { text-align: left; } "
                                                         "QToolTip { color: #ffffff; background-color: #000000; "
                                                         "border: 1px solid white; }")
        button.setToolTip(button_text)
    button.setText(button_text)
    gridLayout.addWidget(button, new_position[0], new_position[1])
    button.clicked.connect(self.clicked_spell_like_button)
    self.spellLikeList.append(button)
    if button_clicked:
        self.data_frame.spells.add_spell_like()
        button.click()


def clicked_spell_like_button(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.spellLikeList)):
        if self.spellLikeList[i].objectName() == object_name:
            index = i
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_SpellLikeEdit()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Edit Spell-Like')
    self.ui.description.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
    self.ui.description.setOpenLinks(False)

    self.ui.name.setEditable(True)
    self.ui.name.addItems(self.spell_data.spell_names)
    self.ui.name.setCurrentText(self.data_frame.spells.spellLikes[index].name)

    self.ui.level.setValue(self.data_frame.spells.spellLikes[index].level)

    self.ui.school.setEditable(True)
    self.ui.school.addItems(self.spell_data.spell_schools)
    self.ui.school.setCurrentText(self.data_frame.spells.spellLikes[index].school)
    self.ui.subschool.setEditable(True)
    self.ui.subschool.addItems(self.spell_data.spell_subschools)
    self.ui.subschool.setCurrentText(self.data_frame.spells.spellLikes[index].subschool)

    self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].prepared)
    self.ui.used.setValue(self.data_frame.spells.spellLikes[index].cast)
    self.ui.notes.setPlainText(self.data_frame.spells.spellLikes[index].notes)
    self.ui.description.setHtml(self.data_frame.spells.spellLikes[index].description)

    self.ui.name.currentIndexChanged.connect(lambda: print(f'Current spell name index: {self.ui.name.currentIndex()}'))
    self.ui.name.currentTextChanged.connect(lambda: self.spell_like_name_updated(index, self.ui.name.currentText()))
    self.ui.level.valueChanged.connect(lambda: self.spell_like_level_updated(index))
    self.ui.school.currentTextChanged.connect(
        lambda: self.spell_like_school_updated(index, self.ui.school.currentText()))
    self.ui.subschool.currentTextChanged.connect(
        lambda: self.spell_like_subschool_updated(index, self.ui.subschool.currentText()))
    self.ui.perDay.valueChanged.connect(lambda: self.spell_like_prepared_updated(index))
    self.ui.used.valueChanged.connect(lambda: self.spell_like_cast_updated(index))
    self.ui.notes.textChanged.connect(lambda: self.spell_like_notes_updated(index))

    self.spell_like_name_updated(index, self.ui.name.currentText())

    self.ui.closeButton.clicked.connect(lambda: self.window.close())
    self.ui.perDayButton.clicked.connect(lambda: self.increase_per_day(index))
    self.ui.usedButton.clicked.connect(lambda: self.increase_used(index))
    self.ui.clearButton.clicked.connect(lambda: self.clear_data(index))
    self.ui.markButton.clicked.connect(lambda: self.marked_spell_like(index))
    self.ui.atWillButton.clicked.connect(lambda: self.at_will(index))
    self.ui.deleteButton.clicked.connect(lambda: self.spell_like_delete(index))

    self.window.show()
    position = self.pos()
    position.setX(self.pos().x() + 120)
    position.setY(self.pos().y() + 250)
    self.window.move(position)


def increase_per_day(self, index):
    self.data_frame.spells.spellLikes[index].prepared += 1
    self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].prepared)


def increase_used(self, index):
    self.data_frame.spells.spellLikes[index].cast += 1
    self.ui.used.setValue(self.data_frame.spells.spellLikes[index].cast)


def clear_data(self, index):
    self.data_frame.spells.spellLikes[index].prepared = 0
    self.data_frame.spells.spellLikes[index].used = 0
    self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].prepared)
    self.ui.used.setValue(self.data_frame.spells.spellLikes[index].used)
    self.data_frame.spells.spellLikes[index].atWill = False


def marked_spell_like(self, index):
    if self.data_frame.spells.spellLikes[index].marked:
        self.spellLikeList[index].setStyleSheet("")
        self.data_frame.spells.spellLikes[index].marked = False
    else:
        self.spellLikeList[index].setStyleSheet("QPushButton"
                                                "{"
                                                "background-color : grey;"
                                                "}")
        self.data_frame.spells.spellLikes[index].marked = True


def at_will(self, index):
    if self.data_frame.spells.spellLikes[index].atWill:
        self.ui.perDay.setValue(0)
        self.data_frame.spells.spellLikes[index].atWill = False
    else:
        self.ui.perDay.setValue(99)
        self.data_frame.spells.spellLikes[index].atWill = True


def spell_like_delete(self, index, reset=False):
    grid_layout = self.gridLayout_10
    self.data_frame.spells.delete_spell_like([index])
    if not reset:
        self.window.close()
    grid_layout.removeWidget(self.spellLikeList[index])
    self.spellLikeList[index].deleteLater()
    del self.spellLikeList[index]
    self.reset_spell_like_position()
    self.spellLikeCount -= 1


def reset_spell_like_position(self):
    grid_layout = self.gridLayout_10
    index = 0
    for button in self.spellLikeList:
        index += 1
        new_position = (((index - 1) // 7) + 1, ((index - 1) % 7) + 1)
        grid_layout.removeWidget(button)
        grid_layout.addWidget(button, new_position[0], new_position[1])


def spell_like_name_updated(self, index, text):
    data = self.spell_data.check_spell_availability(text)
    self.data_frame.spells.spellLikes[index].name = text
    if data:
        self.ui.school.setCurrentText(data['school'])
        self.ui.subschool.setCurrentText(data['subschool'])
        self.ui.description.setHtml(data['description'])
        self.data_frame.spells.spellLikes[index].description = data['description']
    if self.data_frame.spells.spellLikes[index].prepared:
        button_text = '{} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                          self.data_frame.spells.spellLikes[index].cast,
                                          self.data_frame.spells.spellLikes[index].prepared)
    else:
        button_text = '{}'.format(self.data_frame.spells.spellLikes[index].name)

    font_metrics = QFontMetrics(self.spellLikeList[index].font())
    text_width = font_metrics.width(button_text)
    button_width = self.spellLikeList[index].width()

    if text_width > button_width:
        self.spellLikeList[index].setStyleSheet(
            self.spellLikeList[index].styleSheet() + " " + "QPushButton { text-align: left; } "
                                                           "QToolTip { color: #ffffff; background-color: #000000; border: 1px solid white; }")
        self.spellLikeList[index].setToolTip(button_text)
    self.spellLikeList[index].setText(button_text)


def spell_like_level_updated(self, index):
    self.data_frame.spells.spellLikes[index].level = self.sender().value()


def spell_like_school_updated(self, index, text):
    self.data_frame.spells.spellLikes[index].school = text


def spell_like_subschool_updated(self, index, text):
    self.data_frame.spells.spellLikes[index].subschool = text


def spell_like_prepared_updated(self, index):
    self.data_frame.spells.spellLikes[index].prepared = self.sender().value()
    if self.data_frame.spells.spellLikes[index].prepared:
        self.spellLikeList[index].setText(
            '{} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                self.data_frame.spells.spellLikes[index].cast,
                                self.data_frame.spells.spellLikes[index].prepared))
    else:
        self.spellLikeList[index].setText(
            '{}'.format(self.data_frame.spells.spellLikes[index].name))


def spell_like_cast_updated(self, index):
    self.data_frame.spells.spellLikes[index].cast = self.sender().value()
    if self.data_frame.spells.spellLikes[index].prepared:
        self.spellLikeList[index].setText(
            '{} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                self.data_frame.spells.spellLikes[index].cast,
                                self.data_frame.spells.spellLikes[index].prepared))
    else:
        self.spellLikeList[index].setText(
            '{}'.format(self.data_frame.spells.spellLikes[index].name))


def spell_like_notes_updated(self, index):
    self.data_frame.spells.spellLikes[index].notes = self.sender().toPlainText()
