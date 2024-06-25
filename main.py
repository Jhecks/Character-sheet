import copy
import os
import sys
import time
import tkinter
import qdarktheme

import dataFrame
import qtTranslateLayer as qTL
import shutil
from datetime import datetime
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QPushButton, QMainWindow, QVBoxLayout
from enum import Enum
from tkinter import filedialog

from PyUi_Files import CharacterSheet

from auxiliary import data_base_handler as dBH, jsonParser, data_from_db
from buttons import (spell_like_button, spell_button, gear_button,
                     feat_button, ability_button, trait_button, ac_data, attack_data, update_window, add_or_edit_data)


class Themes(Enum):
    dark = 0
    light = 1


def str_to_int(string):
    if string == '' or string == '0':
        return 0
    elif string[0] == '-':
        return 0 - int(string[1:])
    else:
        return int(string[1:])


class ButtonListWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up window
        self.setWindowTitle("Button List")
        self.setGeometry(100, 100, 200, 200)

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        names = dBH.get_character_sheet_names()

        # Create a button for each name
        for name in names:
            button = QPushButton(name)
            button.clicked.connect(lambda checked, n=name: self.open_main_window(n))
            layout.addWidget(button)

        import_button = QPushButton("Import Character")
        import_button.clicked.connect(self.import_character)
        layout.addWidget(import_button)

        # Create a QWidget and set the layout
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def import_character(self):
        # Code to import a character goes here
        pass

    def open_main_window(self, name):
        self.main_window = MainWindow()
        self.main_window.show()
        self.main_window.selectFile(name)
        self.close()


class MainWindow(QtWidgets.QMainWindow, CharacterSheet.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.data_frame = dataFrame.CharacterSheetData()
        self.previous_frame = dataFrame.CharacterSheetData()
        self.actualTheme = None
        self.setupUi(self)
        self.set_dark_theme()
        self.icon_path = os.getcwd() + '\\_internal\\icon.ico'
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle('Pathfinder Character Sheet')


        self.file_path = ''

        self.actionLight_theme_2.triggered.connect(self.set_light_theme)
        self.actionDark_theme_2.triggered.connect(self.set_dark_theme)

        self.actionSelect_file.triggered.connect(self.selectFile)
        self.openShortCut = QShortcut(QKeySequence('Ctrl+O'), self)
        self.openShortCut.activated.connect(self.selectFile)

        self.actionSave.triggered.connect(self.saveFile)
        self.save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.save.activated.connect(self.saveFile)

        self.actionSave_As.triggered.connect(self.saveFileAs)
        self.saveAs = QShortcut(QKeySequence('Ctrl+Shift+S'), self)
        self.saveAs.activated.connect(self.saveFileAs)

        self.menuAddSpell.triggered.connect(self.addOrEditSpell)
        self.menuAddFeat.triggered.connect(self.addOrEditFeat)
        self.menuAddTrait.triggered.connect(self.addOrEditTrait)

        self.menuEditSpell.triggered.connect(self.editSpellData)
        # self.menuEditFeat.triggered.connect(self.editFeatData)
        # self.menuEditTrait.triggered.connect(self.editTraitData)

        # General data update
        for attr in qTL.general_attributes:
            getattr(self, attr).textEdited.connect(self.general_changed)

        # Ability data update
        for attr in qTL.ability_editable_attributes:
            getattr(self, attr).textEdited.connect(self.abilities_changed)

        # Defence data update
        for attr in qTL.defence_ac_editable_attributes:
            getattr(self, attr).textEdited.connect(self.defense_ac_changed)

        for attr in qTL.defence_hp_editable_attributes:
            getattr(self, attr).textEdited.connect(self.defense_hp_changed)

        for attr in qTL.defence_fort_editable_attributes:
            getattr(self, attr).textEdited.connect(self.defense_fort_changed)

        for attr in qTL.defence_reflex_editable_attributes:
            getattr(self, attr).textEdited.connect(self.defense_reflex_changed)

        for attr in qTL.defence_will_editable_attributes:
            getattr(self, attr).textEdited.connect(self.defense_will_changed)

        for attr in qTL.defence_editable_attributes:
            getattr(self, attr).textEdited.connect(self.defense_changed)

        for attr in qTL.defence_cmd_editable_attributes:
            getattr(self, attr).textEdited.connect(self.defense_cmd_changed)

        # Offense data update
        for attr in qTL.offence_attributes:
            getattr(self, attr).textEdited.connect(getattr(self, attr + '_changed'))

        # skills logic
        for attr in qTL.skills_editable_attributes:
            getattr(self, attr).toggled.connect(self.checked_skill)
            getattr(self, attr + '3').textEdited.connect(self.ranks_changed)
            getattr(self, attr + '5').textEdited.connect(self.racial_changed)
            getattr(self, attr + '6').textEdited.connect(self.trait_changed)
            getattr(self, attr + '7').textEdited.connect(self.misc_changed)

        for attr in qTL.skill_craft_perform_prof_attributes:
            getattr(self, attr).textEdited.connect(self.skill_name_changed)

        self.conditionalModifiers.textEdited.connect(self.conditionalModifiers_changed)
        self.languages.textEdited.connect(self.languages_changed)
        self.levelTotal.textEdited.connect(self.level_total_changed)
        self.levelNext.textEdited.connect(self.level_next_changed)

        # Money change
        for attr in qTL.money_attributes:
            getattr(self, attr).textEdited.connect(self.money_changed)

        for data_frame_path, gui_path in qTL.spells_data.items():
            getattr(self, gui_path).textEdited.connect(lambda: self.general_spell_data_changed())

        self.spellsConditionalModifiers.textEdited.connect(lambda: self.spells_conditional_modifiers_changed())
        self.spellsSpeciality.textEdited.connect(lambda: self.spells_speciality_changed())

        # Notes change
        self.notes.textChanged.connect(self.notes_changed)

        self.gearCount = 0
        self.gearIndex = 0
        self.gearList = []
        self.addGear.clicked.connect(lambda: self.add_gear(button_clicked=True))

        self.featCount = 0
        self.featIndex = 0
        self.featList = []
        self.addFeat.clicked.connect(lambda: self.add_feat(button_clicked=True))

        self.abilityCount = 0
        self.abilityIndex = 0
        self.abilityList = []
        self.addAbility.clicked.connect(lambda: self.add_ability(button_clicked=True))

        self.traitCount = 0
        self.traitIndex = 0
        self.traitList = []
        self.addTrait.clicked.connect(lambda: self.add_trait(button_clicked=True))

        self.acCount = 0
        self.acList = []
        self.addAC.clicked.connect(lambda: self.add_ac(button=True))
        self.deleteAC.clicked.connect(lambda: self.delete_ac())

        self.meleeAttacksList = []
        self.rangedAttacksList = []
        self.attacksCount = 0
        self.addMeleeAttack.clicked.connect(lambda: self.add_attack(attackType='melee', button=True))
        self.addRangedAttack.clicked.connect(lambda: self.add_attack(attackType='ranged', button=True))
        self.deleteAttack.clicked.connect(lambda: self.delete_attack())

        self.spellLikeCount = 0
        self.spellLikeIndex = 0
        self.spellLikeList = []
        self.addSpellLike.clicked.connect(
            lambda: self.add_spell_like(button_clicked=True))

        self.zeroCount = 0
        self.zeroIndex = 0
        self.zeroList = []
        self.addZero.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='zero', grid_layout=self.gridLayout_15))

        self.firstCount = 0
        self.firstIndex = 0
        self.firstList = []
        self.addFirst.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='first', grid_layout=self.gridLayout_16))

        self.secondCount = 0
        self.secondIndex = 0
        self.secondList = []
        self.addSecond.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='second', grid_layout=self.gridLayout_17))

        self.thirdCount = 0
        self.thirdIndex = 0
        self.thirdList = []
        self.addThird.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='third', grid_layout=self.gridLayout_18))

        self.fourthCount = 0
        self.fourthIndex = 0
        self.fourthList = []
        self.addFourth.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='fourth', grid_layout=self.gridLayout_19))

        self.fifthCount = 0
        self.fifthIndex = 0
        self.fifthList = []
        self.addFifth.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='fifth', grid_layout=self.gridLayout_20))

        self.sixthCount = 0
        self.sixthIndex = 0
        self.sixthList = []
        self.addSixth.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='sixth', grid_layout=self.gridLayout_21))

        self.seventhCount = 0
        self.seventhIndex = 0
        self.seventhList = []
        self.addSeventh.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='seventh', grid_layout=self.gridLayout_22))

        self.eighthCount = 0
        self.eighthIndex = 0
        self.eighthList = []
        self.addEighth.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='eighth', grid_layout=self.gridLayout_23))

        self.ninthCount = 0
        self.ninthIndex = 0
        self.ninthList = []
        self.addNinth.clicked.connect(
            lambda: self.add_spell(button_clicked=True, spell_level='ninth', grid_layout=self.gridLayout_24))

        self.spell_data = data_from_db.spell_data

    def closeEvent(self, event):
        if self.data_frame != self.previous_frame:
            self.saveFile()

    # spell-likes
    add_spell_like = spell_like_button.add_spell_like
    clicked_spell_like_button = spell_like_button.clicked_spell_like_button
    increase_per_day = spell_like_button.increase_per_day
    increase_used = spell_like_button.increase_used
    clear_data = spell_like_button.clear_data
    marked_spell_like = spell_like_button.marked_spell_like
    at_will = spell_like_button.at_will
    spell_like_delete = spell_like_button.spell_like_delete
    reset_spell_like_position = spell_like_button.reset_spell_like_position
    spell_like_name_updated = spell_like_button.spell_like_name_updated
    spell_like_level_updated = spell_like_button.spell_like_level_updated
    spell_like_school_updated = spell_like_button.spell_like_school_updated
    spell_like_subschool_updated = spell_like_button.spell_like_subschool_updated
    spell_like_prepared_updated = spell_like_button.spell_like_prepared_updated
    spell_like_cast_updated = spell_like_button.spell_like_cast_updated
    spell_like_notes_updated = spell_like_button.spell_like_notes_updated

    # spells
    add_spell = spell_button.add_spell
    clicked_spell_button = spell_button.clicked_spell_button
    increase_prepared = spell_button.increase_prepared
    increase_cast = spell_button.increase_cast
    clear_spell_counter_data = spell_button.clear_spell_counter_data
    marked_spell = spell_button.marked_spell
    spell_name_updated = spell_button.spell_name_updated
    spell_level_updated = spell_button.spell_level_updated
    spell_school_updated = spell_button.spell_school_updated
    spell_subschool_updated = spell_button.spell_subschool_updated
    spell_prepared_updated = spell_button.spell_prepared_updated
    spell_cast_updated = spell_button.spell_cast_updated
    spell_notes_updated = spell_button.spell_notes_updated
    spell_increase_prepared = spell_button.spell_increase_prepared
    spell_increase_cast = spell_button.spell_increase_cast
    spell_clear_data = spell_button.spell_clear_data
    spell_mark = spell_button.spell_mark
    spell_delete = spell_button.spell_delete
    reset_spell_position = spell_button.reset_spell_position

    # gear
    add_gear = gear_button.add_gear
    clicked_gear_button = gear_button.clicked_gear_button
    gear_type_updated = gear_button.gear_type_updated
    gear_item_updated = gear_button.gear_item_updated
    gear_location_updated = gear_button.gear_location_updated
    gear_quantity_updated = gear_button.gear_quantity_updated
    gear_weight_updated = gear_button.gear_weight_updated
    gear_notes_updated = gear_button.gear_notes_updated
    gear_delete = gear_button.gear_delete
    reset_gear_position = gear_button.reset_gear_position

    # feats
    add_feat = feat_button.add_feat
    clicked_feat_button = feat_button.clicked_feat_button
    feat_name_updated = feat_button.feat_name_updated
    feat_type_updated = feat_button.feat_type_updated
    feat_delete = feat_button.feat_delete
    reset_feats_positions = feat_button.reset_feats_positions

    # abilities
    add_ability = ability_button.add_ability
    clicked_ability_button = ability_button.clicked_ability_button
    ability_name_updated = ability_button.ability_name_updated
    ability_type_updated = ability_button.ability_type_updated
    ability_notes_updated = ability_button.ability_notes_updated
    ability_delete = ability_button.ability_delete
    reset_abilities_positions = ability_button.reset_abilities_positions

    # traits
    add_trait = trait_button.add_trait
    clicked_trait_button = trait_button.clicked_trait_button
    trait_name_updated = trait_button.trait_name_updated
    trait_type_updated = trait_button.trait_type_updated
    trait_delete = trait_button.trait_delete
    reset_traits_positions = trait_button.reset_traits_positions

    # ac
    add_ac = ac_data.add_ac
    delete_ac = ac_data.delete_ac
    ac_name_update = ac_data.ac_name_update
    ac_bonus_update = ac_data.ac_bonus_update
    ac_type_update = ac_data.ac_type_update
    ac_check_penalty_update = ac_data.ac_check_penalty_update
    ac_spell_penalty_update = ac_data.ac_spell_penalty_update
    ac_weight_update = ac_data.ac_weight_update
    ac_properties_update = ac_data.ac_properties_update

    # attacks
    add_attack = attack_data.add_attack
    delete_attack = attack_data.delete_attack
    attack_weapon_update = attack_data.attack_weapon_update
    attack_bonus_update = attack_data.attack_bonus_update
    attack_damage_update = attack_data.attack_damage_update
    attack_critical_update = attack_data.attack_critical_update
    attack_type_update = attack_data.attack_type_update
    attack_notes_update = attack_data.attack_notes_update

    # General change
    def general_changed(self):
        setattr(self.data_frame.general, self.sender().objectName(), getattr(self, self.sender().objectName()).text())
        if self.sender().objectName() == 'name':
            self.setWindowTitle(self.data_frame.general.name)

    # Abilities change function
    def abilities_changed(self):
        setattr(self.data_frame.abilities, self.sender().objectName(), getattr(self, self.sender().objectName()).text())
        self.data_frame.update_data()
        self.update_window()

    # Defence data update
    def defense_ac_changed(self):
        setattr(self.data_frame.defense.ac, qTL.inverse_ac_defense_data.get(self.sender().objectName()),
                getattr(self, self.sender().objectName()).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_hp_changed(self):
        setattr(self.data_frame.defense.hp, qTL.inverse_hp_defense_data.get(self.sender().objectName()),
                getattr(self, self.sender().objectName()).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_fort_changed(self):
        setattr(self.data_frame.defense.fort, qTL.inverse_fort_defense_data.get(self.sender().objectName()),
                getattr(self, self.sender().objectName()).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_reflex_changed(self):
        setattr(self.data_frame.defense.reflex, qTL.inverse_reflex_defense_data.get(self.sender().objectName()),
                getattr(self, self.sender().objectName()).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_will_changed(self):
        setattr(self.data_frame.defense.will, qTL.inverse_will_defense_data.get(self.sender().objectName()),
                getattr(self, self.sender().objectName()).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_cmd_changed(self):
        setattr(self.data_frame.defense.cmd, qTL.inverse_cmd_defense_data.get(self.sender().objectName()),
                getattr(self, self.sender().objectName()).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_changed(self):
        setattr(self.data_frame.defense, qTL.inverse_defense_data.get(self.sender().objectName()),
                getattr(self, self.sender().objectName()).text())
        self.data_frame.update_data()
        self.update_window()

    def initiative_total_changed(self):
        self.data_frame.offense.initiative.total = self.initiative_total.text()
        self.data_frame.update_data()
        self.update_window()

    def initiative_miscModifier_changed(self):
        self.data_frame.offense.initiative.miscModifier = self.initiative_miscModifier.text()
        self.data_frame.update_data()
        self.update_window()

    def bab_changed(self):
        self.data_frame.offense.bab = self.bab.text()
        self.data_frame.update_data()
        self.update_window()

    def conditionalOffenseModifiers_changed(self):
        self.data_frame.offense.conditionalOffenseModifiers = self.conditionalOffenseModifiers.text()
        self.data_frame.update_data()
        self.update_window()

    def speed_base_changed(self):
        self.data_frame.offense.speed.base = self.speed_base.text()
        self.data_frame.update_data()
        self.update_window()

    def speed_withArmor_changed(self):
        self.data_frame.offense.speed.withArmor = self.speed_withArmor.text()
        self.data_frame.update_data()
        self.update_window()

    def speed_fly_changed(self):
        self.data_frame.offense.speed.fly = self.speed_fly.text()
        self.data_frame.update_data()
        self.update_window()

    def speed_swim_changed(self):
        self.data_frame.offense.speed.swim = self.speed_swim.text()
        self.data_frame.update_data()
        self.update_window()

    def speed_climb_changed(self):
        self.data_frame.offense.speed.climb = self.speed_climb.text()
        self.data_frame.update_data()
        self.update_window()

    def speed_burrow_changed(self):
        self.data_frame.offense.speed.burrow = self.speed_burrow.text()
        self.data_frame.update_data()
        self.update_window()

    def speed_tempModifiers_changed(self):
        self.data_frame.offense.speed.tempModifiers = self.speed_tempModifiers.text()
        self.data_frame.update_data()
        self.update_window()

    def cmb_total_changed(self):
        self.data_frame.offense.cmb.total = self.cmb_total.text()
        self.data_frame.update_data()
        self.update_window()

    def cmb_sizeModifier_changed(self):
        self.data_frame.offense.cmb.sizeModifier = self.cmb_sizeModifier.text()
        self.data_frame.update_data()
        self.update_window()

    def cmb_miscModifiers_changed(self):
        self.data_frame.offense.cmb.miscModifiers = self.cmb_miscModifiers.text()
        self.data_frame.update_data()
        self.update_window()

    def cmb_tempModifiers_changed(self):
        self.data_frame.offense.cmb.tempModifiers = self.cmb_tempModifiers.text()
        self.data_frame.update_data()
        self.update_window()

    # Skill class check
    def checked_skill(self):
        if getattr(self, self.sender().objectName()).checkState():
            getattr(self.data_frame.skills, self.sender().objectName()).classSkill = True
        else:
            getattr(self.data_frame.skills, self.sender().objectName()).classSkill = False
        self.data_frame.update_data()
        self.update_window()

    def skill_name_changed(self):
        getattr(self.data_frame.skills,
                self.sender().objectName()[:-1]).name = self.sender().text()  # getattr(self, skill + '0').text()
        self.data_frame.update_data()
        self.update_window()

    def conditionalModifiers_changed(self):
        self.data_frame.skills.conditionalModifiers = self.conditionalModifiers.text()
        self.data_frame.update_data()
        self.update_window()

    # skills logic
    def ranks_changed(self):
        getattr(self.data_frame.skills, self.sender().objectName()[:-1]).ranks = self.sender().text()
        self.data_frame.update_data()
        self.update_window()

    def racial_changed(self):
        getattr(self.data_frame.skills, self.sender().objectName()[:-1]).racial = self.sender().text()
        self.data_frame.update_data()
        self.update_window()

    def trait_changed(self):
        getattr(self.data_frame.skills, self.sender().objectName()[:-1]).trait = self.sender().text()
        self.data_frame.update_data()
        self.update_window()

    def misc_changed(self):
        getattr(self.data_frame.skills, self.sender().objectName()[:-1]).misc = self.sender().text()
        self.data_frame.update_data()
        self.update_window()

    def languages_changed(self):
        self.data_frame.skills.languages = self.languages.text()

    def level_total_changed(self):
        self.data_frame.skills.xp.total = self.levelTotal.text()

    def level_next_changed(self):
        self.data_frame.skills.xp.toNextLevel = self.levelNext.text()

    def money_changed(self):
        setattr(self.data_frame.money, self.sender().objectName(), getattr(self, self.sender().objectName()).text())

    def general_spell_data_changed(self):
        self.data_frame.spells.set_attr(qTL.inverse_spell_data[self.sender().objectName()], self.sender().text())

    def spells_conditional_modifiers_changed(self):
        self.data_frame.spells.spellsConditionalModifiers = self.sender().text()

    def spells_speciality_changed(self):
        self.data_frame.spells.spellsSpeciality = self.sender().text()

    def notes_changed(self):
        self.data_frame.notes = self.notes.toPlainText()
        self.data_frame.update_data()

    def set_dark_theme(self):
        qdarktheme.setup_theme()
        self.actionDark_theme_2.setChecked(True)
        self.actionLight_theme_2.setChecked(False)
        self.actualTheme = Themes.dark

    def set_light_theme(self):
        custom_colors = {
            "[light]": {
                "primary": "#4D5157",
                "background": "EEEEEE",
            }
        }
        qdarktheme.setup_theme("light", custom_colors=custom_colors)
        self.actionDark_theme_2.setChecked(False)
        self.actionLight_theme_2.setChecked(True)
        self.actualTheme = Themes.light

    def reset_buttons(self):
        for i in range(len(self.gearList) - 1, -1, -1):
            self.gear_delete(i, reset=True)
        self.gearCount = 0
        self.gearIndex = 0

        for i in range(len(self.featList) - 1, -1, -1):
            self.feat_delete(i, reset=True)
        self.featCount = 0
        self.featIndex = 0

        for i in range(len(self.abilityList) - 1, -1, -1):
            self.ability_delete(i, reset=True)
        self.abilityCount = 0
        self.abilityIndex = 0

        for i in range(len(self.traitList) - 1, -1, -1):
            self.trait_delete(i, reset=True)
        self.traitCount = 0
        self.traitIndex = 0

        for checkBox in self.acList:
            checkBox.checkbox.setChecked(True)
        for i in range(len(self.acList) - 1, -1, -1):
            self.delete_ac()
        self.acCount = 0

        for attack in self.meleeAttacksList:
            attack.checkbox.setChecked(True)
        for attack in self.rangedAttacksList:
            attack.checkbox.setChecked(True)
        self.delete_attack()
        self.attacksCount = 0

        for i in range(len(self.spellLikeList) - 1, -1, -1):
            self.spell_like_delete(i, reset=True)
        self.spellLikeCount = 0
        self.spellLikeIndex = 0

        for i in range(len(self.zeroList) - 1, -1, -1):
            self.spell_delete(i, 'zero', reset=True, grid_layout=self.gridLayout_15)
        self.zeroCount = 0
        self.zeroIndex = 0

        for i in range(len(self.firstList) - 1, -1, -1):
            self.spell_delete(i, 'first', reset=True, grid_layout=self.gridLayout_16)
        self.firstCount = 0
        self.firstIndex = 0

        for i in range(len(self.secondList) - 1, -1, -1):
            self.spell_delete(i, 'second', reset=True, grid_layout=self.gridLayout_17)
        self.secondCount = 0
        self.secondIndex = 0

        for i in range(len(self.thirdList) - 1, -1, -1):
            self.spell_delete(i, 'third', reset=True, grid_layout=self.gridLayout_18)
        self.thirdCount = 0
        self.thirdIndex = 0

        for i in range(len(self.fourthList) - 1, -1, -1):
            self.spell_delete(i, 'fourth', reset=True, grid_layout=self.gridLayout_19)
        self.fourthCount = 0
        self.fourthIndex = 0

        for i in range(len(self.fifthList) - 1, -1, -1):
            self.spell_delete(i, 'fifth', reset=True, grid_layout=self.gridLayout_20)
        self.fifthCount = 0
        self.fifthIndex = 0

        for i in range(len(self.sixthList) - 1, -1, -1):
            self.spell_delete(i, 'sixth', reset=True, grid_layout=self.gridLayout_21)
        self.sixthCount = 0
        self.sixthIndex = 0

        for i in range(len(self.seventhList) - 1, -1, -1):
            self.spell_delete(i, 'seventh', reset=True, grid_layout=self.gridLayout_22)
        self.seventhCount = 0
        self.seventhIndex = 0

        for i in range(len(self.eighthList) - 1, -1, -1):
            self.spell_delete(i, 'eighth', reset=True, grid_layout=self.gridLayout_23)
        self.eighthCount = 0
        self.eighthIndex = 0

        for i in range(len(self.ninthList) - 1, -1, -1):
            self.spell_delete(i, 'ninth', reset=True, grid_layout=self.gridLayout_24)
        self.ninthCount = 0
        self.ninthIndex = 0

    def selectFile(self, name=None):
        if name:
            self.data_frame = jsonParser.json_from_db_to_character_sheet(dBH.get_character_sheet(name))
        else:
            if self.data_frame != self.previous_frame:
                self.saveFile()
            tkinter.Tk().withdraw()
            self.file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if self.file_path == '':
                return

            self.data_frame = jsonParser.json_to_character_sheet(self.file_path)
        self.reset_buttons()
        self.setWindowTitle(self.data_frame.general.name)

        self.update_window()

        for gear in self.data_frame.gears.list:
            self.add_gear(gear)

        for feat in self.data_frame.feats.list:
            self.add_feat(feat)

        for trait in self.data_frame.traits.list:
            self.add_trait(trait)

        for specialAbility in self.data_frame.specialAbilities.list:
            self.add_ability(specialAbility)

        for attack in self.data_frame.attacks.melee:
            self.add_attack(attack, 'melee')

        for attack in self.data_frame.attacks.ranged:
            self.add_attack(attack, 'ranged')

        for item in self.data_frame.defense.ac.items.list:
            self.add_ac(item)

        for spellLike in self.data_frame.spells.spellLikes:
            self.add_spell_like(spellLike)

        spellLevels = {'zero': 'gridLayout_15', 'first': 'gridLayout_16', 'second': 'gridLayout_17',
                       'third': 'gridLayout_18', 'fourth': 'gridLayout_19', 'fifth': 'gridLayout_20',
                       'sixth': 'gridLayout_21', 'seventh': 'gridLayout_22', 'eighth': 'gridLayout_23',
                       'ninth': 'gridLayout_24'}

        for spellLevel, gridLayout in spellLevels.items():
            for spell in getattr(self.data_frame.spells, spellLevel + 'Level').slotted:
                self.add_spell(spell, False, spellLevel, getattr(self, gridLayout))

        self.previous_frame = copy.deepcopy(self.data_frame)

    def saveFile(self):
        if not self.file_path:
            self.saveFileAs()
            return
        self.backup_character_json()
        jsonParser.character_sheet_to_json(self.file_path, self.data_frame.create_json())
        dBH.save_character_sheet(self.data_frame.general.name, self.data_frame.create_json())

    def backup_character_json(self):
        folder_path = os.getcwd() + '\\_internal\\_backup'
        file_to_copy = self.file_path
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        # If there are more than 5 files, delete the oldest
        if len(files) > 50:
            full_paths = [os.path.join(folder_path, f) for f in files]
            oldest_file = min(full_paths, key=os.path.getctime)
            os.remove(oldest_file)

        # Copy the file to the folder and rename it
        current_time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        base_name = os.path.basename(file_to_copy)
        file_name, file_extension = os.path.splitext(base_name)
        new_file_name = f"{file_name}_{current_time}{file_extension}"
        new_file_path = os.path.join(folder_path, new_file_name)
        try:
            shutil.copyfile(file_to_copy, new_file_path)
        except Exception as e:
            print(f"Error while copying file: {e}")

    def saveFileAs(self):
        tkinter.Tk().withdraw()
        self.file_path = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")], defaultextension='.json')
        if self.file_path == '':
            return
        jsonParser.character_sheet_to_json(self.file_path, self.data_frame.create_json())
        dBH.save_character_sheet(self.data_frame.general.name, self.data_frame.create_json())

    # adding or editing data in database
    addOrEditSpell = add_or_edit_data.addOrEditSpell
    check_web_site = add_or_edit_data.check_web_site
    addOrEdit_search = add_or_edit_data.addOrEdit_search
    addOrEdit_changeHtml = add_or_edit_data.addOrEdit_changeHtml
    addOrEditSpell_save = add_or_edit_data.addOrEditSpell_save
    addOrEditSpell_show_warning = add_or_edit_data.addOrEditSpell_show_warning
    addOrEditSpell_show_warning_subschool = add_or_edit_data.addOrEditSpell_show_warning_subschool
    addOrEdit_show_error = add_or_edit_data.addOrEdit_show_error
    addOrEditFeat = add_or_edit_data.addOrEditFeat
    addOrEditFeat_save = add_or_edit_data.addOrEditFeat_save
    addOrEditFeat_show_warning = add_or_edit_data.addOrEditFeat_show_warning
    addOrEditTrait = add_or_edit_data.addOrEditTrait
    addOrEditTrait_save = add_or_edit_data.addOrEditTrait_save
    addOrEditTrait_show_warning = add_or_edit_data.addOrEditTrait_show_warning

    editSpellData = add_or_edit_data.editSpellData
    editSpellData_name_updated = add_or_edit_data.editSpellData_name_updated
    editSpellData_save = add_or_edit_data.editSpellData_save

    # TODO: find correct place
    feat_additional_notes_updated = feat_button.feat_additional_notes_updated

    update_window = update_window.update_window

    def set_skill_attributes(self, skill_name, skill_data, ability_modifier):
        checkbox = getattr(self, skill_name)
        total_text = getattr(self, skill_name + '1')
        ability_text = getattr(self, skill_name + '2')
        ranks_text = getattr(self, skill_name + '3')
        class_skill_text = getattr(self, skill_name + '4')
        racial_text = getattr(self, skill_name + '5')
        trait_text = getattr(self, skill_name + '6')
        misc_text = getattr(self, skill_name + '7')

        checkbox.setChecked(skill_data.classSkill)
        total_text.setText(skill_data.total)
        ability_text.setText(ability_modifier)
        ranks_text.setText(skill_data.ranks)
        class_skill_text.setText(
            "3" if skill_data.classSkill and str.isnumeric(skill_data.ranks) and int(skill_data.ranks) > 0 else "0")
        racial_text.setText(skill_data.racial)
        trait_text.setText(skill_data.trait)
        misc_text.setText(skill_data.misc)

    Attack = attack_data.Attack

    ACItem = ac_data.ACItem


def main():
    try:
        qdarktheme.enable_hi_dpi()
        app = QtWidgets.QApplication(sys.argv)
        start_time = time.time()
        window = MainWindow()
        # window = ButtonListWindow()
        print("--- main window init ---", time.time() - start_time)
        window.show()
        app.exec()

    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)


if __name__ == '__main__':
    main()
