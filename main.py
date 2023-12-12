import copy
import operator
import os
import sys
import tkinter
from enum import Enum
from tkinter import filedialog

import qdarktheme
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

import CharacterSheet
import dataFrame
import qtTranslateLayer as qtl
import xmlParser
from FeatEdit import Ui_FeatEdit
from GearEdit import Ui_GearEdit
from SpellEdit import Ui_SpellEdit
from SpellLikeEdit import Ui_SpellLikeEdit
from TraitEdit import Ui_TraitEdit


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

        # General data update
        self.name.textEdited.connect(lambda: self.general_changed('name'))
        self.alignment.textEdited.connect(lambda: self.general_changed('alignment'))
        self.playerName.textEdited.connect(lambda: self.general_changed('playerName'))
        self.level.textEdited.connect(lambda: self.general_changed('level'))
        self.deity.textEdited.connect(lambda: self.general_changed('deity'))
        self.homeland.textEdited.connect(lambda: self.general_changed('homeland'))
        self.race.textEdited.connect(lambda: self.general_changed('race'))
        self.size.textEdited.connect(lambda: self.general_changed('size'))
        self.gender.textEdited.connect(lambda: self.general_changed('gender'))
        self.age.textEdited.connect(lambda: self.general_changed('age'))
        self.height.textEdited.connect(lambda: self.general_changed('height'))
        self.weight.textEdited.connect(lambda: self.general_changed('weight'))
        self.hair.textEdited.connect(lambda: self.general_changed('hair'))
        self.eyes.textEdited.connect(lambda: self.general_changed('eyes'))

        # Ability data update
        self.str.textEdited.connect(lambda: self.abilities_changed('str'))
        self.tempStr.textEdited.connect(lambda: self.abilities_changed('tempStr'))
        self.int.textEdited.connect(lambda: self.abilities_changed('int'))
        self.tempInt.textEdited.connect(lambda: self.abilities_changed('tempInt'))
        self.dex.textEdited.connect(lambda: self.abilities_changed('dex'))
        self.tempDex.textEdited.connect(lambda: self.abilities_changed('tempDex'))
        self.wis.textEdited.connect(lambda: self.abilities_changed('wis'))
        self.tempWis.textEdited.connect(lambda: self.abilities_changed('tempWis'))
        self.con.textEdited.connect(lambda: self.abilities_changed('con'))
        self.tempCon.textEdited.connect(lambda: self.abilities_changed('tempCon'))
        self.cha.textEdited.connect(lambda: self.abilities_changed('cha'))
        self.tempCha.textEdited.connect(lambda: self.abilities_changed('tempCha'))

        # Defence data update
        self.ac_total.textEdited.connect(lambda: self.defense_ac_changed('ac_total'))
        self.ac_armorBonus.textEdited.connect(lambda: self.defense_ac_changed('ac_armorBonus'))
        self.ac_shieldBonus.textEdited.connect(lambda: self.defense_ac_changed('ac_shieldBonus'))
        self.ac_sizeModifier.textEdited.connect(lambda: self.defense_ac_changed('ac_sizeModifier'))
        self.ac_naturalArmor.textEdited.connect(lambda: self.defense_ac_changed('ac_naturalArmor'))
        self.ac_DeflectionModifier.textEdited.connect(lambda: self.defense_ac_changed('ac_DeflectionModifier'))
        self.ac_miscModifier.textEdited.connect(lambda: self.defense_ac_changed('ac_miscModifier'))

        self.ac_touch.textEdited.connect(lambda: self.defense_ac_changed('ac_touch'))
        self.ac_flatFooted.textEdited.connect(lambda: self.defense_ac_changed('ac_flatFooted'))
        self.ac_otherModifiers.textEdited.connect(lambda: self.defense_ac_changed('ac_otherModifiers'))

        self.hp_total.textEdited.connect(lambda: self.defense_hp_changed('hp_total'))
        self.hp_wounds.textEdited.connect(lambda: self.defense_hp_changed('hp_wounds'))
        self.hp_nonLethal.textEdited.connect(lambda: self.defense_hp_changed('hp_nonLethal'))

        self.fort_total.textEdited.connect(lambda: self.defense_fort_changed('fort_total'))
        self.fort_base.textEdited.connect(lambda: self.defense_fort_changed('fort_base'))
        self.fort_magicModifier.textEdited.connect(lambda: self.defense_fort_changed('fort_magicModifier'))
        self.fort_miscModifier.textEdited.connect(lambda: self.defense_fort_changed('fort_miscModifier'))
        self.fort_tempModifier.textEdited.connect(lambda: self.defense_fort_changed('fort_tempModifier'))
        self.fort_otherModifiers.textEdited.connect(lambda: self.defense_fort_changed('fort_otherModifiers'))

        self.reflex_total.textEdited.connect(lambda: self.defense_reflex_changed('reflex_total'))
        self.reflex_base.textEdited.connect(lambda: self.defense_reflex_changed('reflex_base'))
        self.reflex_magicModifier.textEdited.connect(lambda: self.defense_reflex_changed('reflex_magicModifier'))
        self.reflex_miscModifier.textEdited.connect(lambda: self.defense_reflex_changed('reflex_miscModifier'))
        self.reflex_tempModifier.textEdited.connect(lambda: self.defense_reflex_changed('reflex_tempModifier'))
        self.reflex_otherModifiers.textEdited.connect(lambda: self.defense_reflex_changed('reflex_otherModifiers'))

        self.will_total.textEdited.connect(lambda: self.defense_will_changed('will_total'))
        self.will_base.textEdited.connect(lambda: self.defense_will_changed('will_base'))
        self.will_magicModifier.textEdited.connect(lambda: self.defense_will_changed('will_magicModifier'))
        self.will_miscModifier.textEdited.connect(lambda: self.defense_will_changed('will_miscModifier'))
        self.will_tempModifier.textEdited.connect(lambda: self.defense_will_changed('will_tempModifier'))
        self.will_otherModifiers.textEdited.connect(lambda: self.defense_will_changed('will_otherModifiers'))

        self.resistances.textEdited.connect(lambda: self.defense_changed('resistances'))
        self.immunities.textEdited.connect(lambda: self.defense_changed('immunities'))
        self.damageReduction.textEdited.connect(lambda: self.defense_changed('damageReduction'))
        self.spellResistance.textEdited.connect(lambda: self.defense_changed('spellResistance'))

        self.cmd_total.textEdited.connect(lambda: self.defense_cmd_changed('cmd_total'))
        self.cmd_sizeModifier.textEdited.connect(lambda: self.defense_cmd_changed('cmd_sizeModifier'))
        self.cmd_miscModifiers.textEdited.connect(lambda: self.defense_cmd_changed('cmd_miscModifiers'))
        self.cmd_tempModifiers.textEdited.connect(lambda: self.defense_cmd_changed('cmd_tempModifiers'))

        # Offense data update
        self.initiative_total.textEdited.connect(self.initiative_total_changed)
        self.initiative_miscModifier.textEdited.connect(self.initiative_miscModifier_changed)
        self.bab.textEdited.connect(self.bab_changed)
        self.conditionalOffenseModifiers.textEdited.connect(self.conditionalOffenseModifiers_changed)
        self.speed_base.textEdited.connect(self.speed_base_changed)
        self.speed_withArmor.textEdited.connect(self.speed_withArmor_changed)
        self.speed_fly.textEdited.connect(self.speed_fly_changed)
        self.speed_swim.textEdited.connect(self.speed_swim_changed)
        self.speed_climb.textEdited.connect(self.speed_climb_changed)
        self.speed_burrow.textEdited.connect(self.speed_burrow_changed)
        self.speed_tempModifiers.textEdited.connect(self.speed_tempModifiers_changed)
        self.cmd_total.textEdited.connect(self.cmb_total_changed)
        self.cmb_sizeModifier.textEdited.connect(self.cmb_sizeModifier_changed)
        self.cmb_miscModifiers.textEdited.connect(self.cmb_miscModifiers_changed)
        self.cmb_tempModifiers.textEdited.connect(self.cmb_tempModifiers_changed)

        # skills logic
        self.acrobatics.toggled.connect(lambda: self.checked_skill('acrobatics'))
        self.appraise.toggled.connect(lambda: self.checked_skill('appraise'))
        self.bluff.toggled.connect(lambda: self.checked_skill('bluff'))
        self.climb.toggled.connect(lambda: self.checked_skill('climb'))
        self.craft1.toggled.connect(lambda: self.checked_skill('craft1'))
        self.craft2.toggled.connect(lambda: self.checked_skill('craft2'))
        self.craft3.toggled.connect(lambda: self.checked_skill('craft3'))
        self.diplomacy.toggled.connect(lambda: self.checked_skill('diplomacy'))
        self.disableDevice.toggled.connect(lambda: self.checked_skill('disableDevice'))
        self.disguise.toggled.connect(lambda: self.checked_skill('disguise'))
        self.escapeArtist.toggled.connect(lambda: self.checked_skill('escapeArtist'))
        self.fly.toggled.connect(lambda: self.checked_skill('fly'))
        self.handleAnimal.toggled.connect(lambda: self.checked_skill('handleAnimal'))
        self.heal.toggled.connect(lambda: self.checked_skill('heal'))
        self.intimidate.toggled.connect(lambda: self.checked_skill('intimidate'))
        self.knowledgeArcana.toggled.connect(lambda: self.checked_skill('knowledgeArcana'))
        self.knowledgeDungeoneering.toggled.connect(lambda: self.checked_skill('knowledgeDungeoneering'))
        self.knowledgeEngineering.toggled.connect(lambda: self.checked_skill('knowledgeEngineering'))
        self.knowledgeGeography.toggled.connect(lambda: self.checked_skill('knowledgeGeography'))
        self.knowledgeHistory.toggled.connect(lambda: self.checked_skill('knowledgeHistory'))
        self.knowledgeLocal.toggled.connect(lambda: self.checked_skill('knowledgeLocal'))
        self.knowledgeNature.toggled.connect(lambda: self.checked_skill('knowledgeNature'))
        self.knowledgeNobility.toggled.connect(lambda: self.checked_skill('knowledgeNobility'))
        self.knowledgePlanes.toggled.connect(lambda: self.checked_skill('knowledgePlanes'))
        self.knowledgeReligion.toggled.connect(lambda: self.checked_skill('knowledgeReligion'))
        self.linguistics.toggled.connect(lambda: self.checked_skill('linguistics'))
        self.perception.toggled.connect(lambda: self.checked_skill('perception'))
        self.perform1.toggled.connect(lambda: self.checked_skill('perform1'))
        self.perform2.toggled.connect(lambda: self.checked_skill('perform2'))
        self.profession1.toggled.connect(lambda: self.checked_skill('profession1'))
        self.profession2.toggled.connect(lambda: self.checked_skill('profession2'))
        self.senseMotive.toggled.connect(lambda: self.checked_skill('senseMotive'))
        self.sleightOfHand.toggled.connect(lambda: self.checked_skill('sleightOfHand'))
        self.spellcraft.toggled.connect(lambda: self.checked_skill('spellcraft'))
        self.stealth.toggled.connect(lambda: self.checked_skill('stealth'))
        self.useMagicDevice.toggled.connect(lambda: self.checked_skill('useMagicDevice'))
        self.survival.toggled.connect(lambda: self.checked_skill('survival'))
        self.swim.toggled.connect(lambda: self.checked_skill('swim'))
        self.ride.toggled.connect(lambda: self.checked_skill('ride'))

        self.craft10.textEdited.connect(lambda: self.skill_name_changed('craft1'))
        self.craft20.textEdited.connect(lambda: self.skill_name_changed('craft2'))
        self.craft30.textEdited.connect(lambda: self.skill_name_changed('craft3'))
        self.perform10.textEdited.connect(lambda: self.skill_name_changed('perform1'))
        self.perform20.textEdited.connect(lambda: self.skill_name_changed('perform2'))
        self.profession10.textEdited.connect(lambda: self.skill_name_changed('profession1'))
        self.profession20.textEdited.connect(lambda: self.skill_name_changed('profession2'))

        self.acrobatics3.textEdited.connect(lambda: self.ranks_changed('acrobatics'))
        self.appraise3.textEdited.connect(lambda: self.ranks_changed('appraise'))
        self.bluff3.textEdited.connect(lambda: self.ranks_changed('bluff'))
        self.climb3.textEdited.connect(lambda: self.ranks_changed('climb'))
        self.craft13.textEdited.connect(lambda: self.ranks_changed('craft1'))
        self.craft23.textEdited.connect(lambda: self.ranks_changed('craft2'))
        self.craft33.textEdited.connect(lambda: self.ranks_changed('craft3'))
        self.diplomacy3.textEdited.connect(lambda: self.ranks_changed('diplomacy'))
        self.disableDevice3.textEdited.connect(lambda: self.ranks_changed('disableDevice'))
        self.disguise3.textEdited.connect(lambda: self.ranks_changed('disguise'))
        self.escapeArtist3.textEdited.connect(lambda: self.ranks_changed('escapeArtist'))
        self.fly3.textEdited.connect(lambda: self.ranks_changed('fly'))
        self.handleAnimal3.textEdited.connect(lambda: self.ranks_changed('handleAnimal'))
        self.heal3.textEdited.connect(lambda: self.ranks_changed('heal'))
        self.intimidate3.textEdited.connect(lambda: self.ranks_changed('intimidate'))
        self.knowledgeArcana3.textEdited.connect(lambda: self.ranks_changed('knowledgeArcana'))
        self.knowledgeDungeoneering3.textEdited.connect(lambda: self.ranks_changed('knowledgeDungeoneering'))
        self.knowledgeEngineering3.textEdited.connect(lambda: self.ranks_changed('knowledgeEngineering'))
        self.knowledgeGeography3.textEdited.connect(lambda: self.ranks_changed('knowledgeGeography'))
        self.knowledgeHistory3.textEdited.connect(lambda: self.ranks_changed('knowledgeHistory'))
        self.knowledgeLocal3.textEdited.connect(lambda: self.ranks_changed('knowledgeLocal'))
        self.knowledgeNature3.textEdited.connect(lambda: self.ranks_changed('knowledgeNature'))
        self.knowledgeNobility3.textEdited.connect(lambda: self.ranks_changed('knowledgeNobility'))
        self.knowledgePlanes3.textEdited.connect(lambda: self.ranks_changed('knowledgePlanes'))
        self.knowledgeReligion3.textEdited.connect(lambda: self.ranks_changed('knowledgeReligion'))
        self.linguistics3.textEdited.connect(lambda: self.ranks_changed('linguistics'))
        self.perception3.textEdited.connect(lambda: self.ranks_changed('perception'))
        self.perform13.textEdited.connect(lambda: self.ranks_changed('perform1'))
        self.perform23.textEdited.connect(lambda: self.ranks_changed('perform2'))
        self.profession13.textEdited.connect(lambda: self.ranks_changed('profession1'))
        self.profession23.textEdited.connect(lambda: self.ranks_changed('profession2'))
        self.senseMotive3.textEdited.connect(lambda: self.ranks_changed('senseMotive'))
        self.sleightOfHand3.textEdited.connect(lambda: self.ranks_changed('sleightOfHand'))
        self.spellcraft3.textEdited.connect(lambda: self.ranks_changed('spellcraft'))
        self.stealth3.textEdited.connect(lambda: self.ranks_changed('stealth'))
        self.useMagicDevice3.textEdited.connect(lambda: self.ranks_changed('useMagicDevice'))
        self.survival3.textEdited.connect(lambda: self.ranks_changed('survival'))
        self.swim3.textEdited.connect(lambda: self.ranks_changed('swim'))
        self.ride3.textEdited.connect(lambda: self.ranks_changed('ride'))

        self.acrobatics5.textEdited.connect(lambda: self.racial_changed('acrobatics'))
        self.appraise5.textEdited.connect(lambda: self.racial_changed('appraise'))
        self.bluff5.textEdited.connect(lambda: self.racial_changed('bluff'))
        self.climb5.textEdited.connect(lambda: self.racial_changed('climb'))
        self.craft15.textEdited.connect(lambda: self.racial_changed('craft1'))
        self.craft25.textEdited.connect(lambda: self.racial_changed('craft2'))
        self.craft35.textEdited.connect(lambda: self.racial_changed('craft3'))
        self.diplomacy5.textEdited.connect(lambda: self.racial_changed('diplomacy'))
        self.disableDevice5.textEdited.connect(lambda: self.racial_changed('disableDevice'))
        self.disguise5.textEdited.connect(lambda: self.racial_changed('disguise'))
        self.escapeArtist5.textEdited.connect(lambda: self.racial_changed('escapeArtist'))
        self.fly5.textEdited.connect(lambda: self.racial_changed('fly'))
        self.handleAnimal5.textEdited.connect(lambda: self.racial_changed('handleAnimal'))
        self.heal5.textEdited.connect(lambda: self.racial_changed('heal'))
        self.intimidate5.textEdited.connect(lambda: self.racial_changed('intimidate'))
        self.knowledgeArcana5.textEdited.connect(lambda: self.racial_changed('knowledgeArcana'))
        self.knowledgeDungeoneering5.textEdited.connect(lambda: self.racial_changed('knowledgeDungeoneering'))
        self.knowledgeEngineering5.textEdited.connect(lambda: self.racial_changed('knowledgeEngineering'))
        self.knowledgeGeography5.textEdited.connect(lambda: self.racial_changed('knowledgeGeography'))
        self.knowledgeHistory5.textEdited.connect(lambda: self.racial_changed('knowledgeHistory'))
        self.knowledgeLocal5.textEdited.connect(lambda: self.racial_changed('knowledgeLocal'))
        self.knowledgeNature5.textEdited.connect(lambda: self.racial_changed('knowledgeNature'))
        self.knowledgeNobility5.textEdited.connect(lambda: self.racial_changed('knowledgeNobility'))
        self.knowledgePlanes5.textEdited.connect(lambda: self.racial_changed('knowledgePlanes'))
        self.knowledgeReligion5.textEdited.connect(lambda: self.racial_changed('knowledgeReligion'))
        self.linguistics5.textEdited.connect(lambda: self.racial_changed('linguistics'))
        self.perception5.textEdited.connect(lambda: self.racial_changed('perception'))
        self.perform15.textEdited.connect(lambda: self.racial_changed('perform1'))
        self.perform25.textEdited.connect(lambda: self.racial_changed('perform2'))
        self.profession15.textEdited.connect(lambda: self.racial_changed('profession1'))
        self.profession25.textEdited.connect(lambda: self.racial_changed('profession2'))
        self.senseMotive5.textEdited.connect(lambda: self.racial_changed('senseMotive'))
        self.sleightOfHand5.textEdited.connect(lambda: self.racial_changed('sleightOfHand'))
        self.spellcraft5.textEdited.connect(lambda: self.racial_changed('spellcraft'))
        self.stealth5.textEdited.connect(lambda: self.racial_changed('stealth'))
        self.useMagicDevice5.textEdited.connect(lambda: self.racial_changed('useMagicDevice'))
        self.survival5.textEdited.connect(lambda: self.racial_changed('survival'))
        self.swim5.textEdited.connect(lambda: self.racial_changed('swim'))
        self.ride5.textEdited.connect(lambda: self.racial_changed('ride'))

        self.acrobatics6.textEdited.connect(lambda: self.trait_changed('acrobatics'))
        self.appraise6.textEdited.connect(lambda: self.trait_changed('appraise'))
        self.bluff6.textEdited.connect(lambda: self.trait_changed('bluff'))
        self.climb6.textEdited.connect(lambda: self.trait_changed('climb'))
        self.craft16.textEdited.connect(lambda: self.trait_changed('craft1'))
        self.craft26.textEdited.connect(lambda: self.trait_changed('craft2'))
        self.craft36.textEdited.connect(lambda: self.trait_changed('craft3'))
        self.diplomacy6.textEdited.connect(lambda: self.trait_changed('diplomacy'))
        self.disableDevice6.textEdited.connect(lambda: self.trait_changed('disableDevice'))
        self.disguise6.textEdited.connect(lambda: self.trait_changed('disguise'))
        self.escapeArtist6.textEdited.connect(lambda: self.trait_changed('escapeArtist'))
        self.fly6.textEdited.connect(lambda: self.trait_changed('fly'))
        self.handleAnimal6.textEdited.connect(lambda: self.trait_changed('handleAnimal'))
        self.heal6.textEdited.connect(lambda: self.trait_changed('heal'))
        self.intimidate6.textEdited.connect(lambda: self.trait_changed('intimidate'))
        self.knowledgeArcana6.textEdited.connect(lambda: self.trait_changed('knowledgeArcana'))
        self.knowledgeDungeoneering6.textEdited.connect(lambda: self.trait_changed('knowledgeDungeoneering'))
        self.knowledgeEngineering6.textEdited.connect(lambda: self.trait_changed('knowledgeEngineering'))
        self.knowledgeGeography6.textEdited.connect(lambda: self.trait_changed('knowledgeGeography'))
        self.knowledgeHistory6.textEdited.connect(lambda: self.trait_changed('knowledgeHistory'))
        self.knowledgeLocal6.textEdited.connect(lambda: self.trait_changed('knowledgeLocal'))
        self.knowledgeNature6.textEdited.connect(lambda: self.trait_changed('knowledgeNature'))
        self.knowledgeNobility6.textEdited.connect(lambda: self.trait_changed('knowledgeNobility'))
        self.knowledgePlanes6.textEdited.connect(lambda: self.trait_changed('knowledgePlanes'))
        self.knowledgeReligion6.textEdited.connect(lambda: self.trait_changed('knowledgeReligion'))
        self.linguistics6.textEdited.connect(lambda: self.trait_changed('linguistics'))
        self.perception6.textEdited.connect(lambda: self.trait_changed('perception'))
        self.perform16.textEdited.connect(lambda: self.trait_changed('perform1'))
        self.perform26.textEdited.connect(lambda: self.trait_changed('perform2'))
        self.profession16.textEdited.connect(lambda: self.trait_changed('profession1'))
        self.profession26.textEdited.connect(lambda: self.trait_changed('profession2'))
        self.senseMotive6.textEdited.connect(lambda: self.trait_changed('senseMotive'))
        self.sleightOfHand6.textEdited.connect(lambda: self.trait_changed('sleightOfHand'))
        self.spellcraft6.textEdited.connect(lambda: self.trait_changed('spellcraft'))
        self.stealth6.textEdited.connect(lambda: self.trait_changed('stealth'))
        self.useMagicDevice6.textEdited.connect(lambda: self.trait_changed('useMagicDevice'))
        self.survival6.textEdited.connect(lambda: self.trait_changed('survival'))
        self.swim6.textEdited.connect(lambda: self.trait_changed('swim'))
        self.ride6.textEdited.connect(lambda: self.trait_changed('ride'))

        self.acrobatics7.textEdited.connect(lambda: self.misc_changed('acrobatics'))
        self.appraise7.textEdited.connect(lambda: self.misc_changed('appraise'))
        self.bluff7.textEdited.connect(lambda: self.misc_changed('bluff'))
        self.climb7.textEdited.connect(lambda: self.misc_changed('climb'))
        self.craft17.textEdited.connect(lambda: self.misc_changed('craft1'))
        self.craft27.textEdited.connect(lambda: self.misc_changed('craft2'))
        self.craft37.textEdited.connect(lambda: self.misc_changed('craft3'))
        self.diplomacy7.textEdited.connect(lambda: self.misc_changed('diplomacy'))
        self.disableDevice7.textEdited.connect(lambda: self.misc_changed('disableDevice'))
        self.disguise7.textEdited.connect(lambda: self.misc_changed('disguise'))
        self.escapeArtist7.textEdited.connect(lambda: self.misc_changed('escapeArtist'))
        self.fly7.textEdited.connect(lambda: self.misc_changed('fly'))
        self.handleAnimal7.textEdited.connect(lambda: self.misc_changed('handleAnimal'))
        self.heal7.textEdited.connect(lambda: self.misc_changed('heal'))
        self.intimidate7.textEdited.connect(lambda: self.misc_changed('intimidate'))
        self.knowledgeArcana7.textEdited.connect(lambda: self.misc_changed('knowledgeArcana'))
        self.knowledgeDungeoneering7.textEdited.connect(lambda: self.misc_changed('knowledgeDungeoneering'))
        self.knowledgeEngineering7.textEdited.connect(lambda: self.misc_changed('knowledgeEngineering'))
        self.knowledgeGeography7.textEdited.connect(lambda: self.misc_changed('knowledgeGeography'))
        self.knowledgeHistory7.textEdited.connect(lambda: self.misc_changed('knowledgeHistory'))
        self.knowledgeLocal7.textEdited.connect(lambda: self.misc_changed('knowledgeLocal'))
        self.knowledgeNature7.textEdited.connect(lambda: self.misc_changed('knowledgeNature'))
        self.knowledgeNobility7.textEdited.connect(lambda: self.misc_changed('knowledgeNobility'))
        self.knowledgePlanes7.textEdited.connect(lambda: self.misc_changed('knowledgePlanes'))
        self.knowledgeReligion7.textEdited.connect(lambda: self.misc_changed('knowledgeReligion'))
        self.linguistics7.textEdited.connect(lambda: self.misc_changed('linguistics'))
        self.perception7.textEdited.connect(lambda: self.misc_changed('perception'))
        self.perform17.textEdited.connect(lambda: self.misc_changed('perform1'))
        self.perform27.textEdited.connect(lambda: self.misc_changed('perform2'))
        self.profession17.textEdited.connect(lambda: self.misc_changed('profession1'))
        self.profession27.textEdited.connect(lambda: self.misc_changed('profession2'))
        self.senseMotive7.textEdited.connect(lambda: self.misc_changed('senseMotive'))
        self.sleightOfHand7.textEdited.connect(lambda: self.misc_changed('sleightOfHand'))
        self.spellcraft7.textEdited.connect(lambda: self.misc_changed('spellcraft'))
        self.stealth7.textEdited.connect(lambda: self.misc_changed('stealth'))
        self.useMagicDevice7.textEdited.connect(lambda: self.misc_changed('useMagicDevice'))
        self.survival7.textEdited.connect(lambda: self.misc_changed('survival'))
        self.swim7.textEdited.connect(lambda: self.misc_changed('swim'))
        self.ride7.textEdited.connect(lambda: self.misc_changed('ride'))

        self.conditionalModifiers.textEdited.connect(self.conditionalModifiers_changed)
        self.languages.textEdited.connect(self.languages_changed)
        self.levelTotal.textEdited.connect(self.level_total_changed)
        self.levelNext.textEdited.connect(self.level_next_changed)

        # Money change
        self.pp.textEdited.connect(lambda: self.money_changed('pp'))
        self.gp.textEdited.connect(lambda: self.money_changed('gp'))
        self.sp.textEdited.connect(lambda: self.money_changed('sp'))
        self.cp.textEdited.connect(lambda: self.money_changed('cp'))
        self.gems.textEdited.connect(lambda: self.money_changed('gems'))
        self.other.textEdited.connect(lambda: self.money_changed('other'))

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

    def closeEvent(self, event):
        if self.data_frame != self.previous_frame:
            self.saveFile()

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
                button.setText(f"{spell.name} | {spell.school} ({spell.cast}/{spell.prepared})")
            else:
                button.setText(f"{spell.name} | {spell.school}")
            if spell.marked:
                button.setStyleSheet("QPushButton"
                                     "{"
                                     "background-color : grey;"
                                     "}")
        else:
            button.setText('Click me')
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
        self.window.setWindowTitle('Edit Spell')

        self.ui.name.setText(self.data_frame.spells.spellLikes[index].name)
        self.ui.level.setValue(self.data_frame.spells.spellLikes[index].level)
        self.ui.school.setText(self.data_frame.spells.spellLikes[index].school)
        self.ui.subschool.setText(self.data_frame.spells.spellLikes[index].subschool)
        self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].prepared)
        self.ui.used.setValue(self.data_frame.spells.spellLikes[index].cast)
        self.ui.notes.setPlainText(self.data_frame.spells.spellLikes[index].notes)
        self.ui.description.setPlainText(self.data_frame.spells.spellLikes[index].description)

        self.ui.name.textEdited.connect(lambda: self.spell_like_name_updated(index))
        self.ui.level.valueChanged.connect(lambda: self.spell_like_level_updated(index))
        self.ui.school.textEdited.connect(lambda: self.spell_like_school_updated(index))
        self.ui.subschool.textEdited.connect(lambda: self.spell_like_subschool_updated(index))
        self.ui.perDay.valueChanged.connect(lambda: self.spell_like_prepared_updated(index))
        self.ui.used.valueChanged.connect(lambda: self.spell_like_cast_updated(index))
        self.ui.notes.textChanged.connect(lambda: self.spell_like_notes_updated(index))
        self.ui.description.textChanged.connect(lambda: self.spell_like_description_updated(index))

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

    def spell_like_name_updated(self, index):
        self.data_frame.spells.spellLikes[index].name = self.sender().text()
        if self.data_frame.spells.spellLikes[index].prepared:
            self.spellLikeList[index].setText(
                '{} | {} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                         self.data_frame.spells.spellLikes[index].school,
                                         self.data_frame.spells.spellLikes[index].cast,
                                         self.data_frame.spells.spellLikes[index].prepared))
        else:
            self.spellLikeList[index].setText(
                '{} | {}'.format(self.data_frame.spells.spellLikes[index].name,
                                 self.data_frame.spells.spellLikes[index].school))

    def spell_like_level_updated(self, index):
        self.data_frame.spells.spellLikes[index].level = self.sender().value()

    def spell_like_school_updated(self, index):
        self.data_frame.spells.spellLikes[index].school = self.sender().text()
        if self.data_frame.spells.spellLikes[index].prepared:
            self.spellLikeList[index].setText(
                '{} | {} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                         self.data_frame.spells.spellLikes[index].school,
                                         self.data_frame.spells.spellLikes[index].cast,
                                         self.data_frame.spells.spellLikes[index].prepared))
        else:
            self.spellLikeList[index].setText(
                '{} | {}'.format(self.data_frame.spells.spellLikes[index].name,
                                 self.data_frame.spells.spellLikes[index].school))

    def spell_like_subschool_updated(self, index):
        self.data_frame.spells.spellLikes[index].subschool = self.sender().text()

    def spell_like_prepared_updated(self, index):
        self.data_frame.spells.spellLikes[index].prepared = self.sender().value()
        if self.data_frame.spells.spellLikes[index].prepared:
            self.spellLikeList[index].setText(
                '{} | {} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                         self.data_frame.spells.spellLikes[index].school,
                                         self.data_frame.spells.spellLikes[index].cast,
                                         self.data_frame.spells.spellLikes[index].prepared))
        else:
            self.spellLikeList[index].setText(
                '{} | {}'.format(self.data_frame.spells.spellLikes[index].name,
                                 self.data_frame.spells.spellLikes[index].school))

    def spell_like_cast_updated(self, index):
        self.data_frame.spells.spellLikes[index].cast = self.sender().value()
        if self.data_frame.spells.spellLikes[index].prepared:
            self.spellLikeList[index].setText(
                '{} | {} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                         self.data_frame.spells.spellLikes[index].school,
                                         self.data_frame.spells.spellLikes[index].cast,
                                         self.data_frame.spells.spellLikes[index].prepared))
        else:
            self.spellLikeList[index].setText(
                '{} | {}'.format(self.data_frame.spells.spellLikes[index].name,
                                 self.data_frame.spells.spellLikes[index].school))

    def spell_like_notes_updated(self, index):
        self.data_frame.spells.spellLikes[index].notes = self.sender().toPlainText()

    def spell_like_description_updated(self, index):
        self.data_frame.spells.spellLikes[index].description = self.sender().toPlainText()

    def add_spell(self, spell=None, button_clicked=False, spell_level='', grid_layout=None):
        gridLayout = grid_layout
        setattr(self, spell_level + 'Count', getattr(self, spell_level + 'Count') + 1)
        setattr(self, spell_level + 'Index', getattr(self, spell_level + 'Index') + 1)
        new_position = (
            ((getattr(self, spell_level + 'Count') - 1) // 7) + 1, ((getattr(self, spell_level + 'Count') - 1) % 7) + 1)
        name = 'button № {}'.format(getattr(self, spell_level + 'Index'))
        button = QtWidgets.QPushButton(self.groupBox_14)
        button.setObjectName(name)
        if spell:
            if spell.prepared:
                button.setText(f'{spell.name} | {spell.school} ({spell.cast}/{spell.prepared})')
            else:
                if spell.name or spell.school:
                    button.setText(f'{spell.name} | {spell.school}')
            if spell.marked:
                button.setStyleSheet("QPushButton"
                                     "{"
                                     "background-color : grey;"
                                     "}")
        else:
            button.setText('Click me')
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

        self.ui.name.setText(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name)
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].level = qtl.spell_levels[spell_level]
        self.ui.level.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].level)
        self.ui.school.setText(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school)
        self.ui.subschool.setText(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].subschool)
        self.ui.prepared.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared)
        self.ui.cast.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast)
        self.ui.notes.setPlainText(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].notes)
        self.ui.description.setPlainText(
            getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].description)

        self.ui.name.textEdited.connect(lambda: self.spell_name_updated(index, spell_level))
        self.ui.level.valueChanged.connect(lambda: self.spell_level_updated(index, spell_level))
        self.ui.school.textEdited.connect(lambda: self.spell_school_updated(index, spell_level))
        self.ui.subschool.textEdited.connect(lambda: self.spell_subschool_updated(index, spell_level))
        self.ui.prepared.valueChanged.connect(lambda: self.spell_prepared_updated(index, spell_level))
        self.ui.cast.valueChanged.connect(lambda: self.spell_cast_updated(index, spell_level))
        self.ui.notes.textChanged.connect(lambda: self.spell_notes_updated(index, spell_level))
        self.ui.description.textChanged.connect(lambda: self.spell_description_updated(index, spell_level))

        self.ui.closeButton.clicked.connect(lambda: self.window.close())
        self.ui.preparedButton.clicked.connect(lambda: self.spell_increase_prepared(index, spell_level))
        self.ui.castButton.clicked.connect(lambda: self.spell_increase_cast(index, spell_level))
        self.ui.clearButton.clicked.connect(lambda: self.spell_clear_data(index, spell_level))
        self.ui.markButton.clicked.connect(lambda: self.spell_mark(index, spell_level))
        self.ui.deleteButton.clicked.connect(lambda: self.spell_delete(index, spell_level, grid_layout))

        self.window.show()
        position = self.pos()
        position.setX(self.pos().x() + 120)
        position.setY(self.pos().y() + 250)
        self.window.move(position)

    def increase_prepared(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared += 1
        self.ui.perDay.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared)
        if self.data_frame.spells.spellLikes[index].prepared:
            self.spellLikeList[index].setText(
                '{} | {} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                         self.data_frame.spells.spellLikes[index].school,
                                         self.data_frame.spells.spellLikes[index].cast,
                                         self.data_frame.spells.spellLikes[index].prepared))
        else:
            self.spellLikeList[index].setText(
                '{} | {}'.format(self.data_frame.spells.spellLikes[index].name,
                                 self.data_frame.spells.spellLikes[index].school))

    def increase_cast(self, index):
        self.data_frame.spells.spellLikes[index].used += 1
        self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].used)
        if self.data_frame.spells.spellLikes[index].prepared:
            self.spellLikeList[index].setText(
                '{} | {} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                         self.data_frame.spells.spellLikes[index].school,
                                         self.data_frame.spells.spellLikes[index].cast,
                                         self.data_frame.spells.spellLikes[index].prepared))
        else:
            self.spellLikeList[index].setText(
                '{} | {}'.format(self.data_frame.spells.spellLikes[index].name,
                                 self.data_frame.spells.spellLikes[index].school))

    def clear_spell_counter_data(self, index):
        self.data_frame.spells.spellLikes[index].prepared = 0
        self.data_frame.spells.spellLikes[index].used = 0
        self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].prepared)
        self.ui.perDay.setValue(self.data_frame.spells.spellLikes[index].used)
        if self.data_frame.spells.spellLikes[index].prepared:
            self.spellLikeList[index].setText(
                '{} | {} ({}/{})'.format(self.data_frame.spells.spellLikes[index].name,
                                         self.data_frame.spells.spellLikes[index].school,
                                         self.data_frame.spells.spellLikes[index].cast,
                                         self.data_frame.spells.spellLikes[index].prepared))
        else:
            self.spellLikeList[index].setText(
                '{} | {}'.format(self.data_frame.spells.spellLikes[index].name,
                                 self.data_frame.spells.spellLikes[index].school))

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

    def spell_name_updated(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name = self.sender().text()
        if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                             index].prepared))
        else:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                 getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school))

    def spell_level_updated(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].level = self.sender().value()

    def spell_school_updated(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school = self.sender().text()
        if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                             index].prepared))
        else:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                 getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school))

    def spell_subschool_updated(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].subschool = self.sender().text()

    def spell_prepared_updated(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared = self.sender().value()
        if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school,
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
                '{} | {} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                             index].prepared))
        else:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                 getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school))

    def spell_notes_updated(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].notes = self.sender().toPlainText()

    def spell_description_updated(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].description = self.sender().toPlainText()

    def spell_increase_prepared(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared += 1
        self.ui.prepared.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared)
        if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                             index].prepared))
        else:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                 getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school))

    def spell_increase_cast(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast += 1
        self.ui.cast.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast)
        if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                             index].prepared))
        else:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                 getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school))

    def spell_clear_data(self, index, spell_level):
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared = 0
        getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast = 0
        self.ui.prepared.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared)
        self.ui.cast.setValue(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast)
        if getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].prepared:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {} ({}/{})'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].cast,
                                         getattr(self.data_frame.spells, spell_level + 'Level').slotted[
                                             index].prepared))
        else:
            getattr(self, spell_level + 'List')[index].setText(
                '{} | {}'.format(getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].name,
                                 getattr(self.data_frame.spells, spell_level + 'Level').slotted[index].school))

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

    def add_gear(self, gear=None, button_clicked=False):
        gridLayout = self.gridLayout_13
        self.gearCount += 1
        self.gearIndex += 1
        new_position = ((self.gearCount - 1) // 5 + 1, (self.gearCount - 1) % 5 + 2)
        name = f'button №{self.gearIndex}'
        button = QtWidgets.QPushButton(self.groupBox_11)
        button.setObjectName(name)
        if gear:
            button.setText(f'{gear.type} | {gear.item} ({gear.quantity}) {gear.location}')
        else:
            button.setText('Click me')
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
        self.ui.item.setText(self.data_frame.gears.list[index].item)
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
        self.gearList[index].setText(f'{self.data_frame.gears.list[index].type} | '
                                     f'{self.data_frame.gears.list[index].item} '
                                     f'({self.data_frame.gears.list[index].quantity}) '
                                     f'{self.data_frame.gears.list[index].location}')

    def gear_item_updated(self, index):
        self.data_frame.gears.list[index].item = self.sender().text()
        self.gearList[index].setText(f'{self.data_frame.gears.list[index].type} | '
                                     f'{self.data_frame.gears.list[index].item} '
                                     f'({self.data_frame.gears.list[index].quantity}) '
                                     f'{self.data_frame.gears.list[index].location}')

    def gear_location_updated(self, index):
        self.data_frame.gears.list[index].location = self.sender().text()
        self.gearList[index].setText(f'{self.data_frame.gears.list[index].type} | '
                                     f'{self.data_frame.gears.list[index].item} '
                                     f'({self.data_frame.gears.list[index].quantity}) '
                                     f'{self.data_frame.gears.list[index].location}')

    def gear_quantity_updated(self, index):
        self.data_frame.gears.list[index].quantity = self.sender().text()
        self.gearList[index].setText(f'{self.data_frame.gears.list[index].type} | '
                                     f'{self.data_frame.gears.list[index].item} '
                                     f'({self.data_frame.gears.list[index].quantity}) '
                                     f'{self.data_frame.gears.list[index].location}')

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

    def add_feat(self, feat=None, button_clicked=False):
        gridLayout = self.gridLayout_3
        self.featCount += 1
        self.featIndex += 1
        new_position = (((self.featCount - 1) // 5) + 1, ((self.featCount - 1) % 5) + 2)
        name = f'button №{self.featIndex}'
        button = QtWidgets.QPushButton(self.widget_25)
        button.setObjectName(name)
        if feat:
            if feat.name or feat.type:
                button.setText(f"{feat.type} | {feat.name}")
        else:
            button.setText('Click me')
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

        self.ui.name.setText(self.data_frame.feats.list[index].name)
        self.ui.type.setText(self.data_frame.feats.list[index].type)
        self.ui.notes.setPlainText(self.data_frame.feats.list[index].notes)

        self.ui.name.textEdited.connect(lambda: self.feat_name_updated(index))
        self.ui.type.textEdited.connect(lambda: self.feat_type_updated(index))
        self.ui.notes.textChanged.connect(lambda: self.feat_notes_updated(index))
        self.ui.closeButton.clicked.connect(lambda: self.window.close())
        self.ui.deleteButton.clicked.connect(lambda: self.feat_delete(index))

        self.window.show()
        position = self.pos()
        position.setX(self.pos().x() + 280)
        position.setY(self.pos().y() + 370)
        self.window.move(position)

    def feat_name_updated(self, index):
        self.data_frame.feats.list[index].name = self.sender().text()
        self.featList[index].setText(f'{self.data_frame.feats.list[index].type} | '
                                     f'{self.data_frame.feats.list[index].name}')

    def feat_type_updated(self, index):
        self.data_frame.feats.list[index].type = self.sender().text()
        self.featList[index].setText(f'{self.data_frame.feats.list[index].type} | '
                                     f'{self.data_frame.feats.list[index].name}')

    def feat_notes_updated(self, index):
        self.data_frame.feats.list[index].notes = self.sender().toPlainText()

    def feat_delete(self, index, reset=False):
        grid_layot = self.gridLayout_3
        self.data_frame.feats.delete_feat([index])
        if not reset:
            self.window.close()
        grid_layot.removeWidget(self.featList[index])
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

    def add_ability(self, ability=None, button_clicked=False):
        gridLayout = self.gridLayout_11
        self.abilityCount += 1
        self.abilityIndex += 1
        new_position = ((self.abilityCount - 1) // 5 + 1, (self.abilityCount - 1) % 5 + 2)
        name = f'button №{self.abilityIndex}'
        button = QtWidgets.QPushButton(self.widget)
        button.setObjectName(name)
        if ability:
            if ability.name or ability.type:
                button.setText(f"{ability.name} ({ability.type})")
        else:
            button.setText('Click me')
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
        self.ui = Ui_FeatEdit()
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
        self.abilityList[index].setText(f'{self.data_frame.specialAbilities.list[index].name} '
                                        f'({self.data_frame.specialAbilities.list[index].type})')

    def ability_type_updated(self, index):
        self.data_frame.specialAbilities.list[index].type = self.sender().text()
        self.abilityList[index].setText(f'{self.data_frame.specialAbilities.list[index].name} '
                                        f'({self.data_frame.specialAbilities.list[index].type})')

    def ability_notes_updated(self, index):
        self.data_frame.specialAbilities.list[index].notes = self.sender().toPlainText()

    def ability_delete(self, index, reset=False):
        grid_layot = self.gridLayout_11
        self.data_frame.specialAbilities.delete_special_ability([index])
        if not reset:
            self.window.close()
        grid_layot.removeWidget(self.abilityList[index])
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

    def add_trait(self, trait=None, button_clicked=False):
        gridLayout = self.gridLayout_26
        self.traitCount += 1
        self.traitIndex += 1
        new_position = ((self.traitCount - 1) // 5 + 1, (self.traitCount - 1) % 5 + 2)
        name = f'button №{self.traitIndex}'
        button = QtWidgets.QPushButton(self.widget_2)
        button.setObjectName(name)
        if trait:
            button.setText(f"{trait.type} | {trait.name}")
        else:
            button.setText('Click me')
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

        self.ui.type.setText(self.data_frame.traits.list[index].type)
        self.ui.name.setText(self.data_frame.traits.list[index].name)
        self.ui.notes.setPlainText(self.data_frame.traits.list[index].notes)

        self.ui.type.textEdited.connect(lambda: self.trait_type_updated(index))
        self.ui.name.textEdited.connect(lambda: self.trait_name_updated(index))
        self.ui.notes.textChanged.connect(lambda: self.trait_notes_updated(index))
        self.ui.closeButton.clicked.connect(lambda: self.window.close())
        self.ui.deleteButton.clicked.connect(lambda: self.trait_delete(index))

        self.window.show()
        position = self.pos()
        position.setX(self.pos().x() + 280)
        position.setY(self.pos().y() + 370)
        self.window.move(position)

    def trait_name_updated(self, index):
        self.data_frame.traits.list[index].name = self.sender().text()
        self.traitList[index].setText(f'{self.data_frame.traits.list[index].type} | '
                                      f'{self.data_frame.traits.list[index].name}')

    def trait_type_updated(self, index):
        self.data_frame.traits.list[index].type = self.sender().text()
        self.traitList[index].setText(f'{self.data_frame.traits.list[index].type} | '
                                      f'{self.data_frame.traits.list[index].name}')

    def trait_notes_updated(self, index):
        self.data_frame.traits.list[index].notes = self.sender().toPlainText()

    def trait_delete(self, index, reset=False):
        grid_layot = self.gridLayout_26
        self.data_frame.traits.delete_traits([index])
        if not reset:
            self.window.close()
        grid_layot.removeWidget(self.traitList[index])
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

    # General change
    def general_changed(self, general_item):
        setattr(self.data_frame.general, general_item, getattr(self, general_item).text())
        if general_item == 'name':
            self.setWindowTitle(self.data_frame.general.name)

    # Abilities change function
    def abilities_changed(self, ability):
        setattr(self.data_frame.abilities, ability, getattr(self, ability).text())
        self.data_frame.update_data()
        self.update_window()

    # Defence data update
    def defense_ac_changed(self, item):
        setattr(self.data_frame.defense.ac, qtl.inverse_ac_defense_data.get(item), getattr(self, item).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_hp_changed(self, item):
        setattr(self.data_frame.defense.hp, qtl.inverse_hp_defense_data.get(item), getattr(self, item).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_fort_changed(self, item):
        setattr(self.data_frame.defense.fort, qtl.inverse_fort_defense_data.get(item), getattr(self, item).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_reflex_changed(self, item):
        setattr(self.data_frame.defense.reflex, qtl.inverse_reflex_defense_data.get(item), getattr(self, item).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_will_changed(self, item):
        setattr(self.data_frame.defense.will, qtl.inverse_will_defense_data.get(item), getattr(self, item).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_cmd_changed(self, item):
        setattr(self.data_frame.defense.cmd, qtl.inverse_cmd_defense_data.get(item), getattr(self, item).text())
        self.data_frame.update_data()
        self.update_window()

    def defense_changed(self, item):
        setattr(self.data_frame.defense, qtl.inverse_defense_data.get(item), getattr(self, item).text())
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
    def checked_skill(self, skill_name):
        if getattr(self, skill_name).checkState():
            getattr(self.data_frame.skills, skill_name).classSkill = True
        else:
            getattr(self.data_frame.skills, skill_name).classSkill = False
        self.data_frame.update_data()
        self.update_window()

    def skill_name_changed(self, skill):
        getattr(self.data_frame.skills, skill).name = getattr(self, skill + '0').text()
        self.data_frame.update_data()
        self.update_window()

    def conditionalModifiers_changed(self):
        self.data_frame.skills.conditionalModifiers = self.conditionalModifiers.text()
        self.data_frame.update_data()
        self.update_window()

    # skills logic
    def ranks_changed(self, skill_name):
        getattr(self.data_frame.skills, skill_name).ranks = getattr(self, qtl.skill_ranks.get(skill_name)).text()
        self.data_frame.update_data()
        self.update_window()

    def racial_changed(self, skill_name):
        getattr(self.data_frame.skills, skill_name).racial = getattr(self, qtl.skill_racial.get(skill_name)).text()
        self.data_frame.update_data()
        self.update_window()

    def trait_changed(self, skill_name):
        getattr(self.data_frame.skills, skill_name).trait = getattr(self, qtl.skill_trait.get(skill_name)).text()
        self.data_frame.update_data()
        self.update_window()

    def misc_changed(self, skill_name):
        getattr(self.data_frame.skills, skill_name).misc = getattr(self, qtl.skill_misc.get(skill_name)).text()
        self.data_frame.update_data()
        self.update_window()

    def languages_changed(self):
        self.data_frame.skills.languages = self.languages.text()

    def level_total_changed(self):
        self.data_frame.skills.xp.total = self.levelTotal.text()

    def level_next_changed(self):
        self.data_frame.skills.xp.toNextLevel = self.levelNext.text()

    def money_changed(self, item):
        setattr(self.data_frame.money, item, getattr(self, item).text())

    def notes_changed(self):
        self.data_frame.notes = self.notes.toPlainText()
        self.data_frame.update_data()

    def set_dark_theme(self):
        qdarktheme.setup_theme()
        self.actionDark_theme_2.setChecked(True)
        self.actionLight_theme_2.setChecked(False)
        self.actualTheme = Themes.dark

    def set_light_theme(self):
        qdarktheme.setup_theme('light')
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

    def selectFile(self):
        if self.data_frame != self.previous_frame:
            self.saveFile()
        tkinter.Tk().withdraw()
        self.file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if self.file_path == '':
            return
        self.reset_buttons()
        self.data_frame = xmlParser.xml_to_character_sheet(self.file_path)
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
        xmlParser.character_sheet_to_xml(self.file_path, self.data_frame.create_json())

    def saveFileAs(self):
        tkinter.Tk().withdraw()
        self.file_path = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")], defaultextension='.json')
        if self.file_path == '':
            return
        xmlParser.character_sheet_to_xml(self.file_path, self.data_frame.create_json())

    def update_window(self):
        # Write data to general block in gui
        for attribute in qtl.general_attributes:
            widget = getattr(self, attribute)
            value = getattr(self.data_frame.general, attribute, "")
            widget.setText(value)

        # Write data to attributes block in gui
        for attribute_name in qtl.ability_attributes:
            widget = getattr(self, attribute_name)
            attribute_value = getattr(self.data_frame.abilities, attribute_name)
            widget.setText(attribute_value)
        self.scoreCalc.setText(self.data_frame.abilities.scoreCalc)
        self.int.setText(self.data_frame.abilities.int)

        # Write data to skills block in gui
        for skill_name, modifier in qtl.skill_attributes.items():
            skill_data = getattr(self.data_frame.skills, skill_name)
            actual_modifier = getattr(self.data_frame.abilities, qtl.temp_ability_modifier.get(modifier)) \
                if getattr(self.data_frame.abilities, qtl.temp_ability_modifier.get(modifier)) != '' \
                else getattr(self.data_frame.abilities, qtl.ability_modifier.get(modifier))
            self.set_skill_attributes(skill_name, skill_data, actual_modifier)

        self.craft10.setText(self.data_frame.skills.craft1.name)
        self.craft20.setText(self.data_frame.skills.craft2.name)
        self.craft30.setText(self.data_frame.skills.craft3.name)

        self.perform10.setText(self.data_frame.skills.perform1.name)
        self.perform20.setText(self.data_frame.skills.perform2.name)

        self.profession10.setText(self.data_frame.skills.profession1.name)
        self.profession20.setText(self.data_frame.skills.profession2.name)

        self.conditionalModifiers.setText(self.data_frame.skills.conditionalModifiers)

        self.languages.setText(self.data_frame.skills.languages)
        self.levelTotal.setText(self.data_frame.skills.xp.total)
        self.levelNext.setText(self.data_frame.skills.xp.toNextLevel)

        self.totalRanks.setText(self.data_frame.skills.totalRanks)

        # Write data to defense block in gui
        self.ac_total.setText(self.data_frame.defense.ac.total)
        self.ac_armorBonus.setText(self.data_frame.defense.ac.armorBonus)
        self.ac_shieldBonus.setText(self.data_frame.defense.ac.shieldBonus)
        self.ac_dexModifier.setText(self.data_frame.abilities.tempDexModifier
                                    if self.data_frame.abilities.tempDexModifier != ""
                                    else self.data_frame.abilities.dexModifier)
        self.ac_sizeModifier.setText(self.data_frame.defense.ac.sizeModifier)
        self.ac_naturalArmor.setText(self.data_frame.defense.ac.naturalArmor)
        self.ac_DeflectionModifier.setText(self.data_frame.defense.ac.deflectionModifier)
        self.ac_miscModifier.setText(self.data_frame.defense.ac.miscModifier)
        self.ac_touch.setText(self.data_frame.defense.ac.touch)
        self.ac_flatFooted.setText(self.data_frame.defense.ac.flatFooted)
        self.ac_otherModifiers.setText(self.data_frame.defense.ac.otherModifiers)

        self.hp_total.setText(self.data_frame.defense.hp.total)
        self.hp_wounds.setText(self.data_frame.defense.hp.wounds)
        self.hp_nonLethal.setText(self.data_frame.defense.hp.nonLethal)
        self.damageReduction.setText(self.data_frame.defense.damageReduction)
        self.spellResistance.setText(self.data_frame.defense.spellResistance)

        self.fort_total.setText(self.data_frame.defense.fort.total)
        self.fort_base.setText(self.data_frame.defense.fort.base)
        self.fort_abilityModifier.setText(self.data_frame.abilities.tempConModifier
                                          if self.data_frame.abilities.tempConModifier != ""
                                          else self.data_frame.abilities.conModifier)
        self.fort_magicModifier.setText(self.data_frame.defense.fort.magicModifier)
        self.fort_miscModifier.setText(self.data_frame.defense.fort.miscModifier)
        self.fort_tempModifier.setText(self.data_frame.defense.fort.tempModifier)
        self.fort_otherModifiers.setText(self.data_frame.defense.fort.otherModifiers)

        self.reflex_total.setText(self.data_frame.defense.reflex.total)
        self.reflex_base.setText(self.data_frame.defense.reflex.base)
        self.reflex_abilityModifier.setText(self.data_frame.abilities.tempDexModifier
                                            if self.data_frame.abilities.tempDexModifier != ""
                                            else self.data_frame.abilities.dexModifier)
        self.reflex_magicModifier.setText(self.data_frame.defense.reflex.magicModifier)
        self.reflex_miscModifier.setText(self.data_frame.defense.reflex.miscModifier)
        self.reflex_tempModifier.setText(self.data_frame.defense.reflex.tempModifier)
        self.reflex_otherModifiers.setText(self.data_frame.defense.reflex.otherModifiers)

        self.will_total.setText(self.data_frame.defense.will.total)
        self.will_base.setText(self.data_frame.defense.will.base)
        self.will_abilityModifier.setText(self.data_frame.abilities.tempWisModifier
                                          if self.data_frame.abilities.tempWisModifier != ""
                                          else self.data_frame.abilities.wisModifier)
        self.will_magicModifier.setText(self.data_frame.defense.will.magicModifier)
        self.will_miscModifier.setText(self.data_frame.defense.will.miscModifier)
        self.will_tempModifier.setText(self.data_frame.defense.will.tempModifier)
        self.will_otherModifiers.setText(self.data_frame.defense.will.otherModifiers)

        self.cmd_total.setText(self.data_frame.defense.cmd.total)
        self.cmd_strModifier.setText(self.data_frame.abilities.tempStrModifier
                                     if self.data_frame.abilities.tempStrModifier != ""
                                     else self.data_frame.abilities.strModifier)
        self.cmd_dexModifier.setText(self.data_frame.abilities.tempDexModifier
                                     if self.data_frame.abilities.tempDexModifier != ""
                                     else self.data_frame.abilities.dexModifier)
        self.cmd_sizeModifier.setText(self.data_frame.defense.cmd.sizeModifier)
        self.cmd_miscModifiers.setText(self.data_frame.defense.cmd.miscModifiers)
        self.cmd_tempModifiers.setText(self.data_frame.defense.cmd.tempModifiers)

        self.resistances.setText(self.data_frame.defense.resistances)
        self.immunities.setText(self.data_frame.defense.immunities)

        self.cmd_bab.setText(self.data_frame.offense.bab)

        # Write data to offense block in gui
        self.initiative_total.setText(self.data_frame.offense.initiative.total)
        self.initiative_dexModifier.setText(self.data_frame.abilities.tempDexModifier
                                            if self.data_frame.abilities.tempDexModifier != ""
                                            else self.data_frame.abilities.dexModifier)
        self.initiative_miscModifier.setText(self.data_frame.offense.initiative.miscModifier)
        self.bab.setText(self.data_frame.offense.bab)
        self.conditionalOffenseModifiers.setText(self.data_frame.offense.conditionalOffenseModifiers)
        self.speed_base.setText(self.data_frame.offense.speed.base)
        self.speed_withArmor.setText(self.data_frame.offense.speed.withArmor)
        self.speed_fly.setText(self.data_frame.offense.speed.fly)
        self.speed_swim.setText(self.data_frame.offense.speed.swim)
        self.speed_climb.setText(self.data_frame.offense.speed.climb)
        self.speed_burrow.setText(self.data_frame.offense.speed.burrow)
        self.speed_tempModifiers.setText(self.data_frame.offense.speed.tempModifiers)
        self.cmb_total.setText(self.data_frame.offense.cmb.total)
        self.cmb_bab.setText(self.data_frame.offense.bab)
        self.cmb_strModifier.setText(self.data_frame.abilities.tempStrModifier
                                     if self.data_frame.abilities.tempStrModifier != ""
                                     else self.data_frame.abilities.strModifier)
        self.cmb_sizeModifier.setText(self.data_frame.offense.cmb.sizeModifier)
        self.cmb_miscModifiers.setText(self.data_frame.offense.cmb.miscModifiers)
        self.cmb_tempModifiers.setText(self.data_frame.offense.cmb.tempModifiers)

        # money data
        self.pp.setText(self.data_frame.money.pp)
        self.gp.setText(self.data_frame.money.gp)
        self.sp.setText(self.data_frame.money.sp)
        self.cp.setText(self.data_frame.money.cp)
        self.gems.setText(self.data_frame.money.gems)
        self.other.setText(self.data_frame.money.other)

        self.ac_item_total.setText(self.data_frame.defense.ac.itemsTotals.bonus)
        self.ac_item_check_penalty.setText(self.data_frame.defense.ac.itemsTotals.armorCheckPenalty)
        self.ac_item_spell_penalty.setText(self.data_frame.defense.ac.itemsTotals.spellFailure)
        self.ac_item_weight.setText(self.data_frame.defense.ac.itemsTotals.weight)

        # spells data
        for data_frame_path, gui_path in qtl.spells_data.items():
            getattr(self, gui_path).setText(operator.attrgetter(data_frame_path)(self.data_frame.spells))
        self.spellsConditionalModifiers.setText(self.data_frame.spells.spellsConditionalModifiers)
        self.spellsSpeciality.setText(self.data_frame.spells.spellsSpeciality)

        # adding notes data
        self.notes.setPlainText(self.data_frame.notes)

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


def main():
    try:
        qdarktheme.enable_hi_dpi()
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()

    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)


if __name__ == '__main__':
    main()
