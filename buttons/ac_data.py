from PyQt5 import QtWidgets, QtCore


def add_ac(self, item=None, button=False):
    gridLayout = self.gridLayout_14
    self.acCount += 1
    new_position = self.acCount * 2
    checkBox = QtWidgets.QCheckBox(self.groupBox_12)
    checkBox.setObjectName('test')
    checkBox.setText('AC Item')

    item_name_edit = QtWidgets.QLineEdit(self.groupBox_12)
    item_name_edit.setObjectName(f'item_name_edit{self.acCount}')
    item_bonus_edit = QtWidgets.QLineEdit(self.groupBox_12)
    item_bonus_edit.setObjectName(f'item_bonus_edit{self.acCount}')
    item_type_edit = QtWidgets.QLineEdit(self.groupBox_12)
    item_type_edit.setObjectName(f'item_type_edit{self.acCount}')
    item_check_penalty_edit = QtWidgets.QLineEdit(self.groupBox_12)
    item_check_penalty_edit.setObjectName(f'item_check_penalty_edit{self.acCount}')
    item_spell_failure_edit = QtWidgets.QLineEdit(self.groupBox_12)
    item_spell_failure_edit.setObjectName(f'item_spell_failure_edit{self.acCount}')
    item_weight_edit = QtWidgets.QLineEdit(self.groupBox_12)
    item_weight_edit.setObjectName(f'item_weight_edit{self.acCount}')
    item_properties_edit = QtWidgets.QLineEdit(self.groupBox_12)
    item_properties_edit.setObjectName(f'item_properties_edit{self.acCount}')

    if item:
        item_name_edit.setText(item.name)
        item_bonus_edit.setText(item.bonus)
        item_type_edit.setText(item.type)
        item_check_penalty_edit.setText(item.armorCheckPenalty)
        item_spell_failure_edit.setText(item.spellFailure)
        item_weight_edit.setText(item.weight)
        item_properties_edit.setText(item.properties)

    item_name = QtWidgets.QLabel(self.groupBox_12)
    item_name.setObjectName(f'item_name{self.acCount}')
    item_name.setAlignment(QtCore.Qt.AlignCenter)
    item_name.setText('Item Name')
    item_bonus = QtWidgets.QLabel(self.groupBox_12)
    item_bonus.setObjectName(f'item_bonus{self.acCount}')
    item_bonus.setAlignment(QtCore.Qt.AlignCenter)
    item_bonus.setText('Bonus')
    item_type = QtWidgets.QLabel(self.groupBox_12)
    item_type.setObjectName(f'item_type{self.acCount}')
    item_type.setAlignment(QtCore.Qt.AlignCenter)
    item_type.setText('Type')
    item_check_penalty = QtWidgets.QLabel(self.groupBox_12)
    item_check_penalty.setObjectName(f'item_check_penalty{self.acCount}')
    item_check_penalty.setAlignment(QtCore.Qt.AlignCenter)
    item_check_penalty.setText('Check Penalty')
    item_spell_failure = QtWidgets.QLabel(self.groupBox_12)
    item_spell_failure.setObjectName(f'item_spell_failure{self.acCount}')
    item_spell_failure.setAlignment(QtCore.Qt.AlignCenter)
    item_spell_failure.setText('Spell Failure')
    item_weight = QtWidgets.QLabel(self.groupBox_12)
    item_weight.setObjectName(f'item_weight{self.acCount}')
    item_weight.setAlignment(QtCore.Qt.AlignCenter)
    item_weight.setText('Weight')
    item_properties = QtWidgets.QLabel(self.groupBox_12)
    item_properties.setObjectName(f'item_properties{self.acCount}')
    item_properties.setAlignment(QtCore.Qt.AlignCenter)
    item_properties.setText('Properties')

    self.acList.append(self.ACItem(checkBox, item_name_edit, item_bonus_edit, item_type_edit,
                                   item_check_penalty_edit, item_spell_failure_edit, item_weight_edit,
                                   item_properties_edit, item_name, item_bonus, item_type, item_check_penalty,
                                   item_spell_failure, item_weight, item_properties))

    if button:
        self.data_frame.defense.ac.items.add_item()

    gridLayout.addWidget(checkBox, new_position, 0)

    gridLayout.addWidget(item_name_edit, new_position, 1)
    gridLayout.addWidget(item_bonus_edit, new_position, 2)
    gridLayout.addWidget(item_type_edit, new_position, 3)
    gridLayout.addWidget(item_check_penalty_edit, new_position, 4)
    gridLayout.addWidget(item_spell_failure_edit, new_position, 5)
    gridLayout.addWidget(item_weight_edit, new_position, 6)
    gridLayout.addWidget(item_properties_edit, new_position, 7)

    gridLayout.addWidget(item_name, new_position + 1, 1)
    gridLayout.addWidget(item_bonus, new_position + 1, 2)
    gridLayout.addWidget(item_type, new_position + 1, 3)
    gridLayout.addWidget(item_check_penalty, new_position + 1, 4)
    gridLayout.addWidget(item_spell_failure, new_position + 1, 5)
    gridLayout.addWidget(item_weight, new_position + 1, 6)
    gridLayout.addWidget(item_properties, new_position + 1, 7)

    item_name_edit.textEdited.connect(self.ac_name_update)
    item_bonus_edit.textEdited.connect(self.ac_bonus_update)
    item_type_edit.textEdited.connect(self.ac_type_update)
    item_check_penalty_edit.textEdited.connect(self.ac_check_penalty_update)
    item_spell_failure_edit.textEdited.connect(self.ac_spell_penalty_update)
    item_weight_edit.textEdited.connect(self.ac_weight_update)
    item_properties_edit.textEdited.connect(self.ac_properties_update)


def delete_ac(self):
    gridLayout = self.gridLayout_14
    deleted = []
    data_frame_deleted = []
    index = 0
    for ac in self.acList:
        if ac.checkbox.checkState():
            data_frame_deleted.append(index)
            for attribute in ac.attributes:
                gridLayout.removeWidget(getattr(ac, attribute))
                getattr(ac, attribute).deleteLater()
            deleted.append(ac)
        index += 1
    for item in deleted:
        self.acList.remove(item)
    self.data_frame.defense.ac.items.delete_items(data_frame_deleted)
    self.data_frame.update_data()
    self.update_window()


def ac_name_update(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.acList)):
        if self.acList[i].name.objectName() == object_name:
            index = i
    self.data_frame.defense.ac.items.list[index].name = self.acList[index].name.text()


def ac_bonus_update(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.acList)):
        if self.acList[i].bonus.objectName() == object_name:
            index = i
    self.data_frame.defense.ac.items.list[index].bonus = self.acList[index].bonus.text()
    self.data_frame.update_data()
    self.update_window()


def ac_type_update(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.acList)):
        if self.acList[i].type.objectName() == object_name:
            index = i
    self.data_frame.defense.ac.items.list[index].type = self.acList[index].type.text()


def ac_check_penalty_update(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.acList)):
        if self.acList[i].check_penalty.objectName() == object_name:
            index = i
    self.data_frame.defense.ac.items.list[index].armorCheckPenalty = self.acList[index].check_penalty.text()
    self.data_frame.update_data()
    self.update_window()


def ac_spell_penalty_update(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.acList)):
        if self.acList[i].spell_failure.objectName() == object_name:
            index = i
    self.data_frame.defense.ac.items.list[index].spellFailure = self.acList[index].spell_failure.text()
    self.data_frame.update_data()
    self.update_window()


def ac_weight_update(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.acList)):
        if self.acList[i].weight.objectName() == object_name:
            index = i
    self.data_frame.defense.ac.items.list[index].weight = self.acList[index].weight.text()
    self.data_frame.update_data()
    self.update_window()


def ac_properties_update(self):
    object_name = self.sender().objectName()
    index = 0
    for i in range(len(self.acList)):
        if self.acList[i].properties.objectName() == object_name:
            index = i
    self.data_frame.defense.ac.items.list[index].properties = self.acList[index].properties.text()


class ACItem:
    def __init__(self, checkbox, name, bonus, type, check_penalty, spell_failure, weight, properties,
                 name_label, bonus_label, type_label, check_penalty_label,
                 spell_failure_label, weight_label, properties_label):
        self.checkbox = checkbox
        self.name = name
        self.bonus = bonus
        self.type = type
        self.check_penalty = check_penalty
        self.spell_failure = spell_failure
        self.weight = weight
        self.properties = properties

        self.name_label = name_label
        self.bonus_label = bonus_label
        self.type_label = type_label
        self.check_penalty_label = check_penalty_label
        self.spell_failure_label = spell_failure_label
        self.weight_label = weight_label
        self.properties_label = properties_label

        self.attributes = [
            "checkbox",
            "name",
            "bonus",
            "type",
            "check_penalty",
            "spell_failure",
            "weight",
            "properties",
            "name_label",
            "bonus_label",
            "type_label",
            "check_penalty_label",
            "spell_failure_label",
            "weight_label",
            "properties_label"
        ]
