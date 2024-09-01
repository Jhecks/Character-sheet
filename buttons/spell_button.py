from auxiliary import qt_translate_layer as qtl
from PyUi_Files.SpellEdit import Ui_SpellEdit
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics

from auxiliary.from_main import Themes


def add_spell(self, spell=None, button_clicked=False, spell_level='', grid_layout=None):
    gridLayout = grid_layout
    setattr(self, spell_level + 'Count', getattr(self, spell_level + 'Count') + 1)
    setattr(self, spell_level + 'Index', getattr(self, spell_level + 'Index') + 1)
    new_position = (
        ((getattr(self, spell_level + 'Count') - 1) // 7) + 1, ((getattr(self, spell_level + 'Count') - 1) % 7) + 1)
    name = 'button № {}'.format(getattr(self, spell_level + 'Index'))
    button = QtWidgets.QPushButton(self.groupBox_14)
    button.setObjectName(name)
    button_text = ''
    if spell:
        if spell.prepared:
            button_text = f'{spell.name} ({spell.cast}/{spell.prepared})'
        else:
            if spell.name or spell.school:
                button_text = f'{spell.name}'
        if spell.marked:
            button.setStyleSheet("QPushButton"
                                 "{"
                                 "background-color : grey;"
                                 "}")
    else:
        button_text = 'Click me'
    # font_metrics = QFontMetrics(button.font())
    # text_width = font_metrics.width(button_text)
    # button_width = button.width()

    button.setStyleSheet(button.styleSheet() + " " + "QToolTip { color: #000000; background-color: #dadada;"
                                                     "border: 1px solid grey; }")
    button.setToolTip(button_text)
    button.setText(button_text)
    gridLayout.addWidget(button, new_position[0], new_position[1])
    button.clicked.connect(lambda: self.clicked_spell_button(spell_level, grid_layout))
    getattr(self, spell_level + 'List').append(button)
    if button_clicked:
        getattr(self.data_frame.spells, spell_level + 'Level').add_spell()
        button.click()


def clicked_spell_button(self, spell_level, grid_layout):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(getattr(self, spell_level + 'List'))):
        if getattr(self, spell_level + 'List')[i].objectName() == object_name:
            index = i
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_SpellEdit()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Edit Spell')
    self.ui.description.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
    self.ui.description.setOpenLinks(False)

    self.ui.name.setEditable(True)
    self.ui.name.addItems(self.spell_data.spell_names)
    self.ui.name.setCurrentText(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name)
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].level = qtl.spell_levels[spell_level]
    self.ui.level.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].level)
    self.ui.school.setReadOnly(True)
    self.ui.school.setText(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school)
    self.ui.subschool.setReadOnly(True)
    self.ui.subschool.setText(
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].subschool)
    self.ui.prepared.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared)
    self.ui.cast.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast)
    self.ui.notes.setPlainText(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].notes)
    self.ui.description.setHtml(
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].description)

    self.ui.name.currentIndexChanged.connect(
        lambda: self.spell_name_updated(index, spell_level, self.ui.name.currentText()))
    self.ui.level.valueChanged.connect(lambda: self.spell_level_updated(index, spell_level))
    self.ui.prepared.valueChanged.connect(lambda: self.spell_prepared_updated(index, spell_level))
    self.ui.cast.valueChanged.connect(lambda: self.spell_cast_updated(index, spell_level))
    self.ui.notes.textChanged.connect(lambda: self.spell_notes_updated(index, spell_level))

    self.spell_name_updated(index, spell_level, self.ui.name.currentText())

    self.ui.closeButton.clicked.connect(lambda: self.window.close())
    self.ui.preparedButton.clicked.connect(lambda: self.spell_increase_prepared(index, spell_level))
    self.ui.castButton.clicked.connect(lambda: self.spell_increase_cast(index, spell_level))
    self.ui.clearButton.clicked.connect(lambda: self.spell_clear_data(index, spell_level))
    self.ui.markButton.clicked.connect(lambda: self.spell_mark(index, spell_level))
    self.ui.deleteButton.clicked.connect(lambda: self.spell_delete(index, spell_level, grid_layout))

    position = self.pos()
    position.setX(self.pos().x() + 120)
    position.setY(self.pos().y() + 250)
    self.window.move(position)
    self.window.show()


def increase_prepared(self, index, spell_level):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared += 1
    self.ui.perDay.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared)
    if self.data_frame.spells.spellLikes[index].prepared:
        self.spellLikeList[index].setText(
            '{} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                self.data_frame.spells.spellLikes[index].cast,
                                self.data_frame.spells.spellLikes[index].prepared))
    else:
        self.spellLikeList[index].setText(
            '{} '.format(self.data_frame.spells.spellLikes[index].name))


def increase_cast(self, index):
    self.data_frame.spells.spellLikes[index].used += 1
    self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].used)
    if self.data_frame.spells.spellLikes[index].prepared:
        self.spellLikeList[index].setText(
            '{} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                self.data_frame.spells.spellLikes[index].cast,
                                self.data_frame.spells.spellLikes[index].prepared))
    else:
        self.spellLikeList[index].setText(
            '{}'.format(self.data_frame.spells.spellLikes[index].name))


def clear_spell_counter_data(self, index):
    self.data_frame.spells.spellLikes[index].prepared = 0
    self.data_frame.spells.spellLikes[index].used = 0
    self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].prepared)
    self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].used)
    if self.data_frame.spells.spellLikes[index].prepared:
        self.spellLikeList[index].setText(
            '{} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                self.data_frame.spells.spellLikes[index].cast,
                                self.data_frame.spells.spellLikes[index].prepared))
    else:
        self.spellLikeList[index].setText(
            '{}'.format(self.data_frame.spells.spellLikes[index].name))


def marked_spell(self, index):
    if self.data_frame.spells.spellLikes[index].marked:
        self.spellLikeList[index].setStyleSheet("")
        self.data_frame.spells.spellLikes[index].marked = False
    else:
        self.spellLikeList[index].setStyleSheet("QPushButton"
                                                "{"
                                                "background-color : grey;"
                                                "}")
        self.data_frame.spells.spellLikes[index].marked = True


def spell_name_updated(self, index, spell_level, text):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].update_data_by_name(text)
    self.ui.school.setText(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school)
    self.ui.subschool.setText(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].subschool)
    self.ui.description.setHtml(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].description)
    if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
        button_text = '{} ({}/{})'.format(
            getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
            getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
            getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                index].prepared)
    else:
        button_text = '{}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name)
    getattr(self, spell_level + 'List')[index].setStyleSheet(
        getattr(self, spell_level + 'List')[
            index].styleSheet() + " " + "QToolTip { color: #000000; background-color: #dadada;"
                                        "border: 1px solid grey; }")
    if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].notes:
        getattr(self, spell_level + 'List')[index].setToolTip(
            button_text + '\n' + getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].notes)
    else:
        getattr(self, spell_level + 'List')[index].setToolTip(button_text)
    getattr(self, spell_level + 'List')[index].setToolTipDuration(50000)
    getattr(self, spell_level + 'List')[index].setText(button_text)


def spell_level_updated(self, index, spell_level):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].level = self.sender().value()


def spell_school_updated(self, index, spell_level, text):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school = text


# def spell_notes_updated(self, index, spell_level):


def spell_subschool_updated(self, index, spell_level, text):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].subschool = text


def spell_prepared_updated(self, index, spell_level):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared = self.sender().value()
    if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
        getattr(self, spell_level + 'List')[index].setText(
            '{} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                    index].prepared))
    else:
        getattr(self, spell_level + 'List')[index].setText(
            getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name)


def spell_cast_updated(self, index, spell_level):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast = self.sender().value()
    if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
        getattr(self, spell_level + 'List')[index].setText(
            '{} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                    index].prepared))
    else:
        getattr(self, spell_level + 'List')[index].setText(
            '{}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name))


def spell_notes_updated(self, index, spell_level):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].notes = self.sender().toPlainText()
    getattr(self, spell_level + 'List')[index].setToolTip(
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name + '\n' +
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].notes)


def spell_increase_prepared(self, index, spell_level):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared += 1
    self.ui.prepared.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared)
    if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
        getattr(self, spell_level + 'List')[index].setText(
            '{} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                    index].prepared))
    else:
        getattr(self, spell_level + 'List')[index].setText(
            '{}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name))


def spell_increase_cast(self, index, spell_level):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast += 1
    self.ui.cast.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast)
    if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
        getattr(self, spell_level + 'List')[index].setText(
            '{} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                    index].prepared))
    else:
        getattr(self, spell_level + 'List')[index].setText(
            '{}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name))


def spell_clear_data(self, index, spell_level):
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared = 0
    getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast = 0
    self.ui.prepared.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared)
    self.ui.cast.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast)
    if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
        getattr(self, spell_level + 'List')[index].setText(
            '{} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                    index].prepared))
    else:
        getattr(self, spell_level + 'List')[index].setText(
            '{}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name))


def spell_mark(self, index, spell_level):
    if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].marked:
        getattr(self, spell_level + 'List')[index].setStyleSheet("")
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].marked = False
    else:
        getattr(self, spell_level + 'List')[index].setStyleSheet("QPushButton"
                                                                 "{"
                                                                 "background-color : grey;"
                                                                 "}")
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].marked = True


def spell_delete(self, index, spell_level, grid_layout, reset=False):
    getattr(self.data_frame.spells, spell_level + 'Level').delete_spells([index])
    if not reset:
        self.window.close()
    grid_layout.removeWidget(getattr(self, spell_level + 'List')[index])
    getattr(self, spell_level + 'List')[index].deleteLater()
    del getattr(self, spell_level + 'List')[index]
    self.reset_spell_position(spell_level, grid_layout)
    setattr(self, spell_level + 'Count', getattr(self, spell_level + 'Count') - 1)


def reset_spell_position(self, spell_level, grid_layout):
    index = 0
    for button in getattr(self, spell_level + 'List'):
        index += 1
        new_position = (((index - 1) // 7) + 1, ((index - 1) % 7) + 1)
        grid_layout.removeWidget(button)
        grid_layout.addWidget(button, new_position[0], new_position[1])
