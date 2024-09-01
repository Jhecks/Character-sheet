from PyQt5.QtWidgets import QGridLayout
from PyUi_Files.FeatEdit import Ui_FeatEdit
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics


def add_feat(self, feat=None, button_clicked=False):
    gridLayout = self.gridLayout_3
    self.featCount += 1
    self.featIndex += 1
    new_position = (((self.featCount - 1) // 5) + 1, ((self.featCount - 1) % 5) + 2)
    name = f'button №{self.featIndex}'
    button = QtWidgets.QPushButton(self.widget_25)
    button.setObjectName(name)
    button_text = ''
    if feat:
        if feat.name:
            button_text = f"{feat.name}"
    else:
        button_text = 'Click me'
    font_metrics = QFontMetrics(button.font())
    text_width = font_metrics.width(button_text)
    button_width = button.width()

    if text_width > button_width:
        button.setStyleSheet("QPushButton { text-align: left; } "
                             "QToolTip { color: #ffffff; background-color: #000000; "
                             "border: 1px solid black; padding: 2px; border-radius: 30px; opacity: 200; }")
        button.setToolTip(button_text + '\n' + 'test')
    button.setText(button_text)
    gridLayout.addWidget(button, new_position[0], new_position[1])
    button.clicked.connect(self.clicked_feat_button)
    self.featList.append(button)
    if button_clicked:
        self.data_frame.feats.add_feat()
        button.click()


def clicked_feat_button(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.featList)):
        if self.featList[i].objectName() == object_name:
            index = i
    self.window = QtWidgets.QMainWindow()
    self.ui = Ui_FeatEdit()
    self.ui.setupUi(self.window)
    self.window.setWindowModality(Qt.ApplicationModal)
    self.window.setWindowIcon(QtGui.QIcon(self.icon_path))
    self.window.setWindowTitle('Edit Feat')

    self.ui.notes.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
    self.ui.notes.setOpenLinks(False)

    self.ui.name.setEditable(True)
    self.ui.name.addItems(self.spell_data.feat_names)
    self.ui.name.setCurrentText(self.data_frame.feats.list[index].name)
    self.ui.additionalNotes.setText(self.data_frame.feats.list[index].additionalNotes)
    self.ui.type.setReadOnly(True)
    self.ui.type.setText(self.data_frame.feats.list[index].type)
    self.ui.source.setReadOnly(True)
    self.ui.source.setText(self.data_frame.feats.list[index].source)
    self.ui.notes.setHtml(self.data_frame.feats.list[index].notes)

    self.ui.name.currentIndexChanged.connect(lambda: self.feat_name_updated(self.ui.name.currentIndex(), index, self.ui.name.currentText()))
    self.ui.additionalNotes.textChanged.connect(lambda: self.feat_additional_notes_updated(index, self.ui.additionalNotes.text()))
    self.ui.source.textChanged.connect(lambda: self.feat_source_updated(self.ui.name.currentIndex(), index, self.ui.source.text()))
    self.ui.closeButton.clicked.connect(lambda: self.window.close())
    self.ui.deleteButton.clicked.connect(lambda: self.feat_delete(index))

    position = self.pos()
    position.setX(self.pos().x() + 280)
    position.setY(self.pos().y() + 370)
    self.window.move(position)
    self.window.show()


def feat_name_updated(self, feat_name_index, index, text):
    data = self.spell_data.get_feat_data_from_index(feat_name_index)
    self.data_frame.feats.list[index].name = text
    # TODO: fix opened file option to select other source
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
            self.data_frame.feats.list[index].type = data['type'][i]
            self.data_frame.feats.list[index].source = data['source'][i]
            self.data_frame.feats.list[index].notes = data['description'][i]

            for source_data in data['source']:
                action = QtWidgets.QAction(source_data, self)
                self.ui.menuChange_source.addAction(action)
                action.triggered.connect(lambda checked, text=source_data: self.ui.source.setText(text))

        else:
            self.ui.type.setText(data['type'])
            self.ui.source.setText(data['source'])
            self.ui.notes.setHtml(data['description'])
            self.data_frame.feats.list[index].type = data['type']
            self.data_frame.feats.list[index].source = data['source']
            self.data_frame.feats.list[index].notes = data['description']

    font_metrics = QFontMetrics(self.featList[index].font())
    text_width = font_metrics.width(self.data_frame.feats.list[index].name)
    button_width = self.featList[index].width()

    if text_width > button_width:
        self.featList[index].setStyleSheet(
            self.featList[index].styleSheet() + " " + "QPushButton { text-align: left; } "
                                                      "QToolTip { color: #ffffff; background-color: #000000; border: "
                                                      "1px solid black; padding: 2px; border-radius: 10px; opacity: "
                                                      "200; }")
        self.featList[index].setToolTip(self.data_frame.feats.list[index].name)
    self.featList[index].setText(f'{self.data_frame.feats.list[index].name}')
    print(self.ui.notes.toHtml())


def feat_additional_notes_updated(self, index, text):
    self.data_frame.feats.list[index].additional_notes = text


def feat_source_updated(self, feat_name_index, index, text):
    data = self.spell_data.get_feat_data_from_index(feat_name_index)
    for i in range(len(data['source'])):
        if data['source'][i] == text:
            self.ui.type.setText(data['type'][i])
            self.ui.notes.setHtml(data['description'][i])
    self.data_frame.feats.list[index].source = text
    self.data_frame.feats.list[index].description = self.ui.notes.toHtml()


def feat_delete(self, index, reset=False):
    grid_layout: QGridLayout = self.gridLayout_3
    self.data_frame.feats.delete_feat([index])
    if not reset:
        self.window.close()
    grid_layout.removeWidget(self.featList[index])
    self.featList[index].deleteLater()
    del self.featList[index]
    self.reset_feats_positions()
    self.featCount -= 1


def reset_feats_positions(self):
    gridLayout = self.gridLayout_3
    index = 0
    for button in self.featList:
        index += 1
        new_position = (((index - 1) // 5) + 1, ((index - 1) % 5) + 2)
        gridLayout.removeWidget(button)
        gridLayout.addWidget(button, new_position[0], new_position[1])
