import sys

import operator
import tkinter
from tkinter import filedialog
from PyQt5 import QtWidgets, QtCore
from enum import Enum
import qtTranslateLayer as qtl

import CharacterSheet
import xmlParser
import dataFrame

import qdarktheme


class Themes(Enum):
    dark = 0
    light = 1


def str_to_int(string):
    # print(string)
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
        self.actualTheme = None
        self.setupUi(self)
        # self.setLightTheme()
        # self.setDarkTheme()

        self.actionLight_theme_2.triggered.connect(self.setLightTheme)
        self.actionDark_theme_2.triggered.connect(self.setDarkTheme)
        self.menuFile.triggered.connect(self.selectFile)

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
        self.levelTotal.textEdited.connect(self.levelTotal_changed)
        self.levelNext.textEdited.connect(self.levelNext_changed)

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
        self.addGear.clicked.connect(lambda: self.add_gear())

        self.featCount = 0
        self.addFeat.clicked.connect(lambda: self.add_feat())

        self.abilityCount = 0
        self.addAbility.clicked.connect(lambda: self.add_ability())

        self.traitCount = 0
        self.addTrait.clicked.connect(lambda: self.add_trait())

        self.acCount = 0
        self.acList = []
        self.acList.append(self.ACItem(self.ac_checkBox, self.ac_item_name, self.ac_item_bonus, self.ac_item_type,
                                       self.ac_item_check_penalty, self.ac_item_spell_failure, self.ac_item_weight,
                                       self.ac_item_properties, self.item_name, self.item_bonus, self.item_type,
                                       self.item_check_penalty, self.item_spell_failure, self.item_weight,
                                       self.item_properties))
        self.addAC.clicked.connect(lambda: self.add_ac())
        self.deleteAC.clicked.connect(lambda: self.delete_ac())

        self.attacksList = []
        self.attacksList.append(self.Attack(self.attack_checkbox, self.attack_weapon, self.attack_bonus,
                                            self.attack_damage, self.attack_critical, self.attack_type,
                                            self.attack_notes, self.attack_weapon_label, self.attack_bonus_label,
                                            self.attack_damage_label, self.attack_critical_label,
                                            self.attack_type_label, self.attack_notes_label))

        self.attacksCount = 1
        self.addAttack.clicked.connect(lambda: self.add_attack())
        self.deleteAttack.clicked.connect(lambda: self.delete_attack())

        self.buttons = []

    def add_gear(self, gear=None):

        gridLayout = self.gridLayout_13
        self.gearCount += 1
        new_position = ((self.gearCount - 1) // 7 + 1, (self.gearCount - 1) % 7 + 2)
        name = f'button №{self.gearCount}'
        button = QtWidgets.QPushButton(self.groupBox_11)
        button.setObjectName(f'button{self.gearCount}')
        if gear:
            button.setText(gear.name)
        else:
            button.setText('Click me')
        gridLayout.addWidget(button, new_position[0], new_position[1])
        button.clicked.connect(lambda: self.clicked_gear_button(name))
        self.buttons.append(button)

    def clicked_gear_button(self, counter):
        print(f'clicked gear {counter}')

    def add_feat(self, feat=None):
        gridLayout = self.gridLayout_3
        self.featCount += 1
        new_position = (((self.featCount - 1) // 7) + 1, ((self.featCount - 1) % 7) + 2)
        name = f'button №{self.featCount}'
        button = QtWidgets.QPushButton(self.widget_25)
        button.setObjectName('test')
        if feat:
            button.setText(feat.name)
        else:
            button.setText('Click me')
        gridLayout.addWidget(button, new_position[0], new_position[1])
        button.clicked.connect(lambda: self.clicked_feat_button(name))
        # print(self.buttons[-1].setText('newText'))

    def clicked_feat_button(self, counter):
        print(f'clicked feat {counter}')

    def add_ability(self, ability=None):
        gridLayout = self.gridLayout_11
        self.abilityCount += 1
        new_position = ((self.abilityCount - 1) // 7 + 1, (self.abilityCount - 1) % 7 + 2)
        name = f'button №{self.abilityCount}'
        button = QtWidgets.QPushButton(self.widget)
        button.setObjectName('test')
        if ability:
            button.setText(ability.name)
        else:
            button.setText('Click me')
        gridLayout.addWidget(button, new_position[0], new_position[1])
        button.clicked.connect(lambda: self.clicked_ability_button(name))

    def clicked_ability_button(self, counter):
        print(f'clicked ability {counter}')

    def add_trait(self, trait=None):
        gridLayout = self.gridLayout_26
        self.traitCount += 1
        new_position = ((self.traitCount - 1) // 7 + 1, (self.traitCount - 1) % 7 + 2)
        name = f'button №{self.traitCount}'
        button = QtWidgets.QPushButton(self.widget_2)
        button.setObjectName('test')
        if trait:
            button.setText(trait.name)
        else:
            button.setText('Click me')
        gridLayout.addWidget(button, new_position[0], new_position[1])
        button.clicked.connect(lambda: self.clicked_trait_button(name))

    def clicked_trait_button(self, counter):
        print(f'clicked trait {counter}')

    def add_ac(self):
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

    def delete_ac(self):
        gridLayout = self.gridLayout_14
        deleted = []
        for ac in self.acList:
            if ac.checkbox.checkState():
                for attribute in ac.attributes:
                    gridLayout.removeWidget(getattr(ac, attribute))
                    getattr(ac, attribute).deleteLater()
                deleted.append(ac)
        for item in deleted:
            self.acList.remove(item)
        print(len(self.acList))

    def add_attack(self):
        gridLayout = self.gridLayout_12
        self.attacksCount += 1
        new_position = self.attacksCount * 2

        checkBox = QtWidgets.QCheckBox(self.groupBox_10)
        checkBox.setObjectName('test')
        checkBox.setText('Attack')

        attack_weapon_edit = QtWidgets.QLineEdit(self.groupBox_10)
        attack_weapon_edit.setObjectName(f'attack_weapon_edit{self.acCount}')
        attack_bonus_edit = QtWidgets.QLineEdit(self.groupBox_10)
        attack_bonus_edit.setObjectName(f'attack_bonus_edit{self.acCount}')
        attack_damage_edit = QtWidgets.QLineEdit(self.groupBox_10)
        attack_damage_edit.setObjectName(f'attack_damage_edit{self.acCount}')
        attack_critical_edit = QtWidgets.QLineEdit(self.groupBox_10)
        attack_critical_edit.setObjectName(f'attack_critical_edit{self.acCount}')
        attack_type_edit = QtWidgets.QLineEdit(self.groupBox_10)
        attack_type_edit.setObjectName(f'attack_type_edit{self.acCount}')
        attack_notes_edit = QtWidgets.QLineEdit(self.groupBox_10)
        attack_notes_edit.setObjectName(f'attack_notes_edit{self.acCount}')

        attack_weapon = QtWidgets.QLabel(self.groupBox_10)
        attack_weapon.setObjectName(f'attack_weapon{self.acCount}')
        attack_weapon.setAlignment(QtCore.Qt.AlignCenter)
        attack_weapon.setText('Weapon')
        attack_bonus = QtWidgets.QLabel(self.groupBox_10)
        attack_bonus.setObjectName(f'attack_bonus{self.acCount}')
        attack_bonus.setAlignment(QtCore.Qt.AlignCenter)
        attack_bonus.setText('Attack Bonus')
        attack_damage = QtWidgets.QLabel(self.groupBox_10)
        attack_damage.setObjectName(f'attack_damage{self.acCount}')
        attack_damage.setAlignment(QtCore.Qt.AlignCenter)
        attack_damage.setText('Damage')
        attack_critical = QtWidgets.QLabel(self.groupBox_10)
        attack_critical.setObjectName(f'attack_critical{self.acCount}')
        attack_critical.setAlignment(QtCore.Qt.AlignCenter)
        attack_critical.setText('Critical')
        attack_type = QtWidgets.QLabel(self.groupBox_10)
        attack_type.setObjectName(f'attack_type{self.acCount}')
        attack_type.setAlignment(QtCore.Qt.AlignCenter)
        attack_type.setText('Type')
        attack_notes = QtWidgets.QLabel(self.groupBox_10)
        attack_notes.setObjectName(f'attack_notes{self.acCount}')
        attack_notes.setAlignment(QtCore.Qt.AlignCenter)
        attack_notes.setText('Notes/Ammunition')

        self.attacksList.append(self.Attack(checkBox, attack_weapon_edit, attack_bonus_edit, attack_damage_edit,
                                            attack_critical_edit, attack_type_edit, attack_notes_edit, attack_weapon,
                                            attack_bonus, attack_damage, attack_critical, attack_type, attack_notes))

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

    def delete_attack(self):
        gridLayout = self.gridLayout_12
        deleted = []
        for attack in self.attacksList:
            if attack.checkbox.checkState():
                for attribute in attack.attributes:
                    gridLayout.removeWidget(getattr(attack, attribute))
                    getattr(attack, attribute).deleteLater()
                deleted.append(attack)
        for item in deleted:
            self.attacksList.remove(item)
        print(len(self.attacksList))

    # General change
    def general_changed(self, general_item):
        setattr(self.data_frame.general, general_item, getattr(self, general_item).text())

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

    def levelTotal_changed(self):
        self.data_frame.skills.xp.total = self.levelTotal.text()

    def levelNext_changed(self):
        self.data_frame.skills.xp.toNextLevel = self.levelNext.text()

    def money_changed(self, item):
        setattr(self.data_frame.money, item, getattr(self, item).text())

    def notes_changed(self):
        self.data_frame.notes = self.notes.toPlainText()
        self.data_frame.update_data()

    def setDarkTheme(self):
        qdarktheme.setup_theme()
        self.actionDark_theme_2.setChecked(True)
        self.actionLight_theme_2.setChecked(False)
        self.actualTheme = Themes.dark

    def setLightTheme(self):
        qdarktheme.setup_theme('light')
        self.actionDark_theme_2.setChecked(False)
        self.actionLight_theme_2.setChecked(True)
        self.actualTheme = Themes.light

    def selectFile(self):
        tkinter.Tk().withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        self.data_frame = xmlParser.xml_parser(file_path)

        self.setWindowTitle(self.data_frame.general.name)

        self.update_window()

        for gear in self.data_frame.gears.gears:
            self.add_gear(gear)

        for feat in self.data_frame.feats.feats:
            self.add_feat(feat)

        for trait in self.data_frame.traits.traits:
            self.add_trait(trait)

        for specialAbility in self.data_frame.specialAbilities.specialAbilities:
            self.add_ability(specialAbility)

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
        self.fort_tempModifier.setText(self.data_frame.defense.fort.tempModifier)
        self.fort_otherModifiers.setText(self.data_frame.defense.fort.otherModifiers)

        self.reflex_total.setText(self.data_frame.defense.reflex.total)
        self.reflex_base.setText(self.data_frame.defense.reflex.base)
        self.reflex_abilityModifier.setText(self.data_frame.abilities.tempDexModifier
                                            if self.data_frame.abilities.tempDexModifier != ""
                                            else self.data_frame.abilities.dexModifier)
        self.reflex_magicModifier.setText(self.data_frame.defense.reflex.magicModifier)
        self.reflex_tempModifier.setText(self.data_frame.defense.reflex.tempModifier)
        self.reflex_otherModifiers.setText(self.data_frame.defense.reflex.otherModifiers)

        self.will_total.setText(self.data_frame.defense.will.total)
        self.will_base.setText(self.data_frame.defense.will.base)
        self.will_abilityModifier.setText(self.data_frame.abilities.tempWisModifier
                                          if self.data_frame.abilities.tempWisModifier != ""
                                          else self.data_frame.abilities.wisModifier)
        self.will_magicModifier.setText(self.data_frame.defense.will.magicModifier)
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
        self.cmd_miscModifiers.setText(self.data_frame.defense.cmd.miscModifier)
        self.cmd_tempModifiers.setText(self.data_frame.defense.cmd.tempModifier)

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
        class_skill_text.setText("3" if skill_data.classSkill else "0")
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
