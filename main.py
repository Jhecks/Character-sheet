import sys
import os
import ftfy

import tkinter
from tkinter import filedialog
from PyQt5 import QtWidgets
from enum import Enum

import CharacterSheet
import xmlParser

import qdarktheme


class Themes(Enum):
    dark = 0
    light = 1


class MainWindow(QtWidgets.QMainWindow, CharacterSheet.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.actualTheme = None
        self.setupUi(self)
        self.setLightTheme()
        # self.setDarkTheme()

        self.actionLight_theme_2.triggered.connect(self.setLightTheme)
        self.actionDark_theme_2.triggered.connect(self.setDarkTheme)
        self.menuFile.triggered.connect(self.selectFile)

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
        data_frame = xmlParser.xml_parser(file_path)
        self.CharacterName.setText(data_frame.general.name)
        self.Alignment.setText(data_frame.general.alignment)
        self.PlayerName.setText(data_frame.general.playerName)
        self.CharacterClassAndLevel.setText(data_frame.general.level)
        self.Deity.setText(data_frame.general.deity)
        self.Homeland.setText(data_frame.general.homeland)
        self.Race.setText(data_frame.general.race)
        self.Size.setText(data_frame.general.size)
        self.Gender.setText(data_frame.general.gender)
        self.Age.setText(data_frame.general.age)
        self.Height.setText(data_frame.general.height)
        self.Weight.setText(data_frame.general.weight)
        self.Hair.setText(data_frame.general.hair)
        self.Eyes.setText(data_frame.general.eyes)

        self.Str1.setText(data_frame.abilities.str)
        self.Str2.setText(data_frame.abilities.strModifier)
        self.Str3.setText(data_frame.abilities.tempStr)
        self.Str4.setText(data_frame.abilities.tempStrModifier)
        self.Int1.setText(data_frame.abilities.int)
        self.Int2.setText(data_frame.abilities.intModifier)
        self.Int3.setText(data_frame.abilities.tempInt)
        self.Int4.setText(data_frame.abilities.tempIntModifier)
        self.Dex1.setText(data_frame.abilities.dex)
        self.Dex2.setText(data_frame.abilities.dexModifier)
        self.Dex3.setText(data_frame.abilities.tempDex)
        self.Dex4.setText(data_frame.abilities.tempDexModifier)
        self.Wis1.setText(data_frame.abilities.wis)
        self.Wis2.setText(data_frame.abilities.wisModifier)
        self.Wis3.setText(data_frame.abilities.tempWis)
        self.Wis4.setText(data_frame.abilities.tempWisModifier)
        self.Con1.setText(data_frame.abilities.con)
        self.Con2.setText(data_frame.abilities.conModifier)
        self.Con3.setText(data_frame.abilities.tempCon)
        self.Con4.setText(data_frame.abilities.tempConModifier)
        self.Cha1.setText(data_frame.abilities.cha)
        self.Cha2.setText(data_frame.abilities.chaModifier)
        self.Cha3.setText(data_frame.abilities.tempCha)
        self.Cha4.setText(data_frame.abilities.tempChaModifier)

        self.set_skill_attributes('Acrobatics', data_frame.skills.acrobatics, data_frame.abilities.dexModifier)
        self.set_skill_attributes('Appraise', data_frame.skills.appraise, data_frame.abilities.intModifier)
        self.set_skill_attributes('Bluff', data_frame.skills.bluff, data_frame.abilities.chaModifier)
        self.set_skill_attributes('Climb', data_frame.skills.climb, data_frame.abilities.strModifier)
        self.set_skill_attributes('Craft_1', data_frame.skills.craft1, data_frame.abilities.intModifier)
        self.Craft_10.setText(data_frame.skills.craft1.name)
        self.set_skill_attributes('Craft_2', data_frame.skills.craft2, data_frame.abilities.intModifier)
        self.Craft_20.setText(data_frame.skills.craft2.name)
        self.set_skill_attributes('Craft_3', data_frame.skills.craft3, data_frame.abilities.intModifier)
        self.Craft_30.setText(data_frame.skills.craft3.name)
        self.set_skill_attributes('Diplomacy', data_frame.skills.diplomacy, data_frame.abilities.chaModifier)
        self.set_skill_attributes('DisableDevice', data_frame.skills.disableDevice, data_frame.abilities.dexModifier)
        self.set_skill_attributes('Disguise', data_frame.skills.disguise, data_frame.abilities.chaModifier)

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

def main():
    try:
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
