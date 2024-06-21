from PyQt5 import QtWidgets, QtCore


def add_attack(self, attack_data=None, attackType='', button=False):
    gridLayout = self.gridLayout_12
    self.attacksCount += 1
    new_position = self.attacksCount * 2

    checkBox = QtWidgets.QCheckBox(self.groupBox_10)
    checkBox.setObjectName('test')

    attack_weapon_edit = QtWidgets.QLineEdit(self.groupBox_10)
    attack_weapon_edit.setObjectName(f'attack_weapon_edit{self.attacksCount}')
    attack_bonus_edit = QtWidgets.QLineEdit(self.groupBox_10)
    attack_bonus_edit.setObjectName(f'attack_bonus_edit{self.attacksCount}')
    attack_damage_edit = QtWidgets.QLineEdit(self.groupBox_10)
    attack_damage_edit.setObjectName(f'attack_damage_edit{self.attacksCount}')
    attack_critical_edit = QtWidgets.QLineEdit(self.groupBox_10)
    attack_critical_edit.setObjectName(f'attack_critical_edit{self.attacksCount}')
    attack_type_edit = QtWidgets.QLineEdit(self.groupBox_10)
    attack_type_edit.setObjectName(f'attack_type_edit{self.attacksCount}')
    attack_notes_edit = QtWidgets.QLineEdit(self.groupBox_10)
    attack_notes_edit.setObjectName(f'attack_notes_edit{self.attacksCount}')

    if attack_data:
        attack_weapon_edit.setText(attack_data.weapon)
        attack_bonus_edit.setText(attack_data.attackBonus)
        attack_damage_edit.setText(attack_data.damage)
        attack_critical_edit.setText(attack_data.critical)
        attack_type_edit.setText(attack_data.type)
        if attackType == 'melee':
            attack_notes_edit.setText(attack_data.notes)
        else:
            attack_notes_edit.setText(attack_data.ammunition)

    attack_weapon = QtWidgets.QLabel(self.groupBox_10)
    attack_weapon.setObjectName(f'attack_weapon{self.attacksCount}')
    attack_weapon.setAlignment(QtCore.Qt.AlignCenter)
    attack_weapon.setText('Weapon')
    attack_bonus = QtWidgets.QLabel(self.groupBox_10)
    attack_bonus.setObjectName(f'attack_bonus{self.attacksCount}')
    attack_bonus.setAlignment(QtCore.Qt.AlignCenter)
    attack_bonus.setText('Attack Bonus')
    attack_damage = QtWidgets.QLabel(self.groupBox_10)
    attack_damage.setObjectName(f'attack_damage{self.attacksCount}')
    attack_damage.setAlignment(QtCore.Qt.AlignCenter)
    attack_damage.setText('Damage')
    attack_critical = QtWidgets.QLabel(self.groupBox_10)
    attack_critical.setObjectName(f'attack_critical{self.attacksCount}')
    attack_critical.setAlignment(QtCore.Qt.AlignCenter)
    attack_critical.setText('Critical')
    attack_type = QtWidgets.QLabel(self.groupBox_10)
    attack_type.setObjectName(f'attack_type{self.attacksCount}')
    attack_type.setAlignment(QtCore.Qt.AlignCenter)
    attack_type.setText('Type')

    if attackType == 'melee':
        checkBox.setText('Melee attack')

        attack_notes = QtWidgets.QLabel(self.groupBox_10)
        attack_notes.setObjectName(f'attack_notes{self.attacksCount}')
        attack_notes.setAlignment(QtCore.Qt.AlignCenter)
        attack_notes.setText('Notes')

        self.meleeAttacksList.append(
            self.Attack(checkBox, attack_weapon_edit, attack_bonus_edit, attack_damage_edit,
                        attack_critical_edit, attack_type_edit, attack_notes_edit, attack_weapon,
                        attack_bonus, attack_damage, attack_critical, attack_type, attack_notes))

    else:
        checkBox.setText('Ranged attack')

        attack_notes = QtWidgets.QLabel(self.groupBox_10)
        attack_notes.setObjectName(f'attack_notes{self.attacksCount}')
        attack_notes.setAlignment(QtCore.Qt.AlignCenter)
        attack_notes.setText('Ammunition')

        self.rangedAttacksList.append(
            self.Attack(checkBox, attack_weapon_edit, attack_bonus_edit, attack_damage_edit,
                        attack_critical_edit, attack_type_edit, attack_notes_edit,
                        attack_weapon,
                        attack_bonus, attack_damage, attack_critical, attack_type,
                        attack_notes))

    if button:
        if attackType == 'melee':
            self.data_frame.attacks.add_melee_attack()
        else:
            self.data_frame.attacks.add_ranged_attack()

    gridLayout.addWidget(checkBox, new_position, 0)

    gridLayout.addWidget(attack_weapon_edit, new_position, 1)
    gridLayout.addWidget(attack_bonus_edit, new_position, 2)
    gridLayout.addWidget(attack_damage_edit, new_position, 3)
    gridLayout.addWidget(attack_critical_edit, new_position, 4)
    gridLayout.addWidget(attack_type_edit, new_position, 5)
    gridLayout.addWidget(attack_notes_edit, new_position, 6)

    gridLayout.addWidget(attack_weapon, new_position + 1, 1)
    gridLayout.addWidget(attack_bonus, new_position + 1, 2)
    gridLayout.addWidget(attack_damage, new_position + 1, 3)
    gridLayout.addWidget(attack_critical, new_position + 1, 4)
    gridLayout.addWidget(attack_type, new_position + 1, 5)
    gridLayout.addWidget(attack_notes, new_position + 1, 6)

    attack_weapon_edit.textEdited.connect(lambda: self.attack_weapon_update(attackType == 'melee'))
    attack_bonus_edit.textEdited.connect(lambda: self.attack_bonus_update(attackType == 'melee'))
    attack_damage_edit.textEdited.connect(lambda: self.attack_damage_update(attackType == 'melee'))
    attack_critical_edit.textEdited.connect(lambda: self.attack_critical_update(attackType == 'melee'))
    attack_type_edit.textEdited.connect(lambda: self.attack_type_update(attackType == 'melee'))
    attack_notes_edit.textEdited.connect(lambda: self.attack_notes_update(attackType == 'melee'))


def delete_attack(self):
    gridLayout = self.gridLayout_12
    deleted = []
    data_frame_deleted = []
    index = 0
    for attack in self.meleeAttacksList:
        if attack.checkbox.checkState():
            data_frame_deleted.append(index)
            for attribute in attack.attributes:
                gridLayout.removeWidget(getattr(attack, attribute))
                getattr(attack, attribute).deleteLater()
            deleted.append(attack)
        index += 1
    for item in deleted:
        self.meleeAttacksList.remove(item)
    self.data_frame.attacks.delete_melee_attacks(data_frame_deleted)
    deleted = []
    data_frame_deleted = []
    index = 0
    for attack in self.rangedAttacksList:
        if attack.checkbox.checkState():
            data_frame_deleted.append(index)
            for attribute in attack.attributes:
                gridLayout.removeWidget(getattr(attack, attribute))
                getattr(attack, attribute).deleteLater()
            deleted.append(attack)
        index += 1
    for item in deleted:
        self.rangedAttacksList.remove(item)
    self.data_frame.attacks.delete_ranged_attacks(data_frame_deleted)


def attack_weapon_update(self, melee=False):
    object_name = self.sender().objectName()
    if melee:
        index = 0
        for i in range(len(self.meleeAttacksList)):
            if self.meleeAttacksList[i].weapon.objectName() == object_name:
                index = i
        self.data_frame.attacks.melee[index].weapon = self.meleeAttacksList[index].weapon.text()
    else:
        index = 0
        for i in range(len(self.rangedAttacksList)):
            if self.rangedAttacksList[i].weapon.objectName() == object_name:
                index = i
        self.data_frame.attacks.ranged[index].weapon = self.rangedAttacksList[index].weapon.text()


def attack_bonus_update(self, melee=False):
    object_name = self.sender().objectName()
    if melee:
        index = 0
        for i in range(len(self.meleeAttacksList)):
            if self.meleeAttacksList[i].bonus.objectName() == object_name:
                index = i
        self.data_frame.attacks.melee[index].attackBonus = self.meleeAttacksList[index].bonus.text()
    else:
        index = 0
        for i in range(len(self.rangedAttacksList)):
            if self.rangedAttacksList[i].bonus.objectName() == object_name:
                index = i
        self.data_frame.attacks.ranged[index].attackBonus = self.rangedAttacksList[index].bonus.text()


def attack_damage_update(self, melee=False):
    object_name = self.sender().objectName()
    if melee:
        index = 0
        for i in range(len(self.meleeAttacksList)):
            if self.meleeAttacksList[i].damage.objectName() == object_name:
                index = i
        self.data_frame.attacks.melee[index].damage = self.meleeAttacksList[index].damage.text()
    else:
        index = 0
        for i in range(len(self.rangedAttacksList)):
            if self.rangedAttacksList[i].damage.objectName() == object_name:
                index = i
        self.data_frame.attacks.ranged[index].damage = self.rangedAttacksList[index].damage.text()


def attack_critical_update(self, melee=False):
    object_name = self.sender().objectName()
    if melee:
        index = 0
        for i in range(len(self.meleeAttacksList)):
            if self.meleeAttacksList[i].critical.objectName() == object_name:
                index = i
        self.data_frame.attacks.melee[index].critical = self.meleeAttacksList[index].critical.text()
    else:
        index = 0
        for i in range(len(self.rangedAttacksList)):
            if self.rangedAttacksList[i].critical.objectName() == object_name:
                index = i
        self.data_frame.attacks.ranged[index].critical = self.rangedAttacksList[index].critical.text()


def attack_type_update(self, melee=False):
    object_name = self.sender().objectName()
    if melee:
        index = 0
        for i in range(len(self.meleeAttacksList)):
            if self.meleeAttacksList[i].type.objectName() == object_name:
                index = i
        self.data_frame.attacks.melee[index].type = self.meleeAttacksList[index].type.text()
    else:
        index = 0
        for i in range(len(self.rangedAttacksList)):
            if self.rangedAttacksList[i].type.objectName() == object_name:
                index = i
        self.data_frame.attacks.ranged[index].type = self.rangedAttacksList[index].type.text()


def attack_notes_update(self, melee=False):
    object_name = self.sender().objectName()
    if melee:
        index = 0
        for i in range(len(self.meleeAttacksList)):
            if self.meleeAttacksList[i].notes.objectName() == object_name:
                index = i
        self.data_frame.attacks.melee[index].notes = self.meleeAttacksList[index].notes.text()
    else:
        index = 0
        for i in range(len(self.rangedAttacksList)):
            if self.rangedAttacksList[i].notes.objectName() == object_name:
                index = i
        self.data_frame.attacks.ranged[index].ammunition = self.rangedAttacksList[index].notes.text()


class Attack:
    def __init__(self, checkbox, weapon, bonus, damage, critical, type, notes, weapon_label, bonus_label,
                 damage_label, critical_label, type_label, notes_label):
        self.checkbox = checkbox
        self.weapon = weapon
        self.bonus = bonus
        self.damage = damage
        self.critical = critical
        self.type = type
        self.notes = notes

        self.weapon_label = weapon_label
        self.bonus_label = bonus_label
        self.damage_label = damage_label
        self.critical_label = critical_label
        self.type_label = type_label
        self.notes_label = notes_label

        self.attributes = [
            "checkbox",
            "weapon",
            "bonus",
            "damage",
            "critical",
            "type",
            "notes",
            "weapon_label",
            "bonus_label",
            "damage_label",
            "critical_label",
            "type_label",
            "notes_label"
        ]