from PyUi_Files.GearEdit import Ui_GearEdit
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics


def add_gear(self, gear=None, button_clicked=False):
    gridLayout = self.gridLayout_13
    self.gearCount += 1
    self.gearIndex += 1
    new_position = ((self.gearCount - 1) // 5 + 1, (self.gearCount - 1) % 5 + 2)
    name = f'button №{self.gearIndex}'
    button = QtWidgets.QPushButton(self.groupBox_11)
    button.setObjectName(name)
    if gear:
        button_text = f'{gear.name} ({gear.quantity})'
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
    button.clicked.connect(self.clicked_gear_button)
    self.gearList.append(button)
    if button_clicked:
        self.data_frame.gears.add_gear()
        button.click()


def clicked_gear_button(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.gearList)):
        if self.gearList[i].objectName() == object_name:
            index = i
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_GearEdit()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Edit Gear')

    self.ui.type.setText(self.data_frame.gears.list[index].type)
    self.ui.item.setText(self.data_frame.gears.list[index].name)
    self.ui.location.setText(self.data_frame.gears.list[index].location)
    self.ui.quantity.setText(self.data_frame.gears.list[index].quantity)
    self.ui.weight.setText(self.data_frame.gears.list[index].weight)
    self.ui.notes.setPlainText(self.data_frame.gears.list[index].notes)

    self.ui.type.textEdited.connect(lambda: self.gear_type_updated(index))
    self.ui.item.textEdited.connect(lambda: self.gear_item_updated(index))
    self.ui.location.textEdited.connect(lambda: self.gear_location_updated(index))
    self.ui.quantity.textEdited.connect(lambda: self.gear_quantity_updated(index))
    self.ui.weight.textEdited.connect(lambda: self.gear_weight_updated(index))
    self.ui.notes.textChanged.connect(lambda: self.gear_notes_updated(index))
    self.ui.closeButton.clicked.connect(lambda: self.window.close())
    self.ui.deleteButton.clicked.connect(lambda: self.gear_delete(index))

    self.window.show()
    position = self.pos()
    position.setX(self.pos().x() + 180)
    position.setY(self.pos().y() + 350)
    self.window.move(position)


def gear_type_updated(self, index):
    self.data_frame.gears.list[index].type = self.sender().text()


def gear_item_updated(self, index):
    self.data_frame.gears.list[index].name = self.sender().text()
    self.gearList[index].setText(f'{self.data_frame.gears.list[index].name} '
                                 f'({self.data_frame.gears.list[index].quantity})')


def gear_location_updated(self, index):
    self.data_frame.gears.list[index].location = self.sender().text()


def gear_quantity_updated(self, index):
    self.data_frame.gears.list[index].quantity = self.sender().text()
    self.gearList[index].setText(f'{self.data_frame.gears.list[index].name} '
                                 f'({self.data_frame.gears.list[index].quantity})')


def gear_weight_updated(self, index):
    self.data_frame.gears.list[index].weight = self.sender().text()


def gear_notes_updated(self, index):
    self.data_frame.gears.list[index].notes = self.sender().toPlainText()


def gear_delete(self, index=0, reset=False):
    grid_layout = self.gridLayout_13
    if not reset:
        self.window.close()
    self.data_frame.gears.delete_gear([index])
    grid_layout.removeWidget(self.gearList[index])
    self.gearList[index].deleteLater()
    del self.gearList[index]
    self.reset_gear_position()
    self.gearCount -= 1


def reset_gear_position(self):
    gridLayout = self.gridLayout_13
    index = 0
    for button in self.gearList:
        index += 1
        new_position = (((index - 1) // 5) + 1, ((index - 1) % 5) + 2)
        gridLayout.removeWidget(button)
        gridLayout.addWidget(button, new_position[0], new_position[1])
