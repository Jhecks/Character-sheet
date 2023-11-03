import sys

import tkinter
from tkinter import filedialog
from PyQt5 import QtWidgets
from enum import Enum
import qtTranslateLayer as qtl

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
        # self.setLightTheme()
        self.setDarkTheme()

        self.actionLight_theme_2.triggered.connect(self.setLightTheme)
        self.actionDark_theme_2.triggered.connect(self.setDarkTheme)
        self.menuFile.triggered.connect(self.selectFile)

        self.pushButton_14.clicked.connect(self.cpGroup)

        # Select boxes logic
        self.acrobatics.toggled.connect(self.checked_acrobatics)
        self.appraise.toggled.connect(self.checked_appraise)

        self.setupTabs()

    def setupTabs(self):
        # Add widgets or layouts to the original and target tabs
        originalLayout = QtWidgets.QVBoxLayout(self.tabWidget)
        originalLayout.addWidget(QtWidgets.QLabel("Original Tab Content"))

        targetLayout = QtWidgets.QVBoxLayout(self.tabWidget)
        targetLayout.addWidget(QtWidgets.QLabel("Target Tab Content"))

    def copyTabItems(self):
        # Get the layouts of both tabs
        originalLayout = self.tabWidget.layout()
        targetLayout = self.tabWidget.layout()

        if originalLayout is not None and targetLayout is not None:
            for i in range(originalLayout.count()):
                item = originalLayout.itemAt(i)
                if item:
                    widget = item.widget()
                    if widget:
                        # Create a deep copy of the widget
                        new_widget = widget.clone()  # You need to implement 'clone' method for each specific widget
                        targetLayout.addWidget(new_widget)

    def cpGroup(self):
        self.copyGroupBox(self.acTemplate)

    def checked_acrobatics(self):
        if self.acrobatics.checkState():
            self.acrobatics4.setText('3')
        else:
            self.acrobatics4.setText('0')

    # "groupBox_4"
    # "meleeAttackButton"
    # def addLineEdits(self):
    #     # Create a row of 5 LineEdits in a horizontal layout
    #     line_edits = []
    #     for _ in range(5):
    #         line_edit = QtWidgets.QLineEdit()
    #         line_edits.append(line_edit)
    #
    #     # Get the groupBox layout (assuming the groupBox's name is groupBoxName)
    #     groupBox_layout = getattr(self, "groupBox_4").layout()
    #
    #     # Find the index of the addButton (assuming the name of the button is addButtonName)
    #     index = groupBox_layout.indexOf(getattr(self, "meleeAttackButton"))
    #
    #     if index != -1:
    #         # Create a new row in the grid layout
    #         new_row = groupBox_layout.rowCount()
    #         groupBox_layout.addWidget(line_edits[0], new_row, 0)
    #         groupBox_layout.addWidget(line_edits[1], new_row, 1)
    #         groupBox_layout.addWidget(line_edits[2], new_row, 2)
    #         groupBox_layout.addWidget(line_edits[3], new_row, 3)
    #         groupBox_layout.addWidget(line_edits[4], new_row, 4)
    #
    #         # Set the row stretch to make the GroupBox extend
    #         groupBox_layout.setRowStretch(new_row, 10)
    def copyGroupBox(self, originalGroupBox):
        newGroupBox = QtWidgets.QGroupBox()
        newGroupBox.setTitle(originalGroupBox.title())

        # Get the layout of the original GroupBox
        originalLayout = originalGroupBox.layout()

        if originalLayout is not None:
            # Create a new layout for the copied GroupBox
            newLayout = QtWidgets.QVBoxLayout(newGroupBox)

            for i in range(originalLayout.count()):
                item = originalLayout.itemAt(i)
                if item:
                    widget = item.widget()
                    spacer = item.spacerItem()
                    layout = item.layout()

                    # Copy the widgets or layouts to the new GroupBox
                    if widget:
                        newLayout.addWidget(widget)
                    elif layout:
                        newLayout.addLayout(self.copyLayout(layout))  # Recursive call to copy nested layouts
                    elif spacer:
                        newLayout.addSpacerItem(spacer)

        return newGroupBox

    def copyLayout(self, originalLayout):
        newLayout = QtWidgets.QVBoxLayout()  # Change layout type if needed

        for i in range(originalLayout.count()):
            item = originalLayout.itemAt(i)
            if item:
                widget = item.widget()
                spacer = item.spacerItem()
                layout = item.layout()

                if widget:
                    newLayout.addWidget(widget)
                elif layout:
                    newLayout.addLayout(self.copyLayout(layout))
                elif spacer:
                    newLayout.addSpacerItem(spacer)

        return newLayout

    def insertCopiedGroupBox(self):
        # Assuming originalGroupBox is the existing groupBox that you want to duplicate
        originalGroupBox = self.originalGroupBox  # Replace with your GroupBox instance

        copiedGroupBox = self.copyGroupBox(originalGroupBox)

        # Add the copied GroupBox after a certain button (replace 'addButtonName' with your button's name)
        layout = self.layout()  # Assuming the layout of the main window
        index = layout.indexOf(getattr(self, 'pushButton_14'))

        if index != -1:
            layout.insertWidget(index + 1, copiedGroupBox)
    def checked_appraise(self):
        if self.appraise.checkState():
            self.appraise4.setText('3')
        else:
            self.appraise4.setText('0')

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

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), data_frame.general.name)

        # Write data to general block in gui
        for attribute in qtl.general_attributes:
            widget = getattr(self, attribute)
            value = getattr(data_frame.general, attribute, "")
            widget.setText(value)

        # Write data to attributes block in gui
        for attribute_name in qtl.ability_attributes:
            widget = getattr(self, attribute_name)
            attribute_value = getattr(data_frame.abilities, attribute_name)
            widget.setText(attribute_value)
        self.scoreCalc.setText(data_frame.abilities.scoreCalc)

        # Write data to skills block in gui
        for skill_name, modifier in qtl.skill_attributes.items():
            skill_data = getattr(data_frame.skills, skill_name)
            actual_modifier = getattr(data_frame.abilities, qtl.temp_ability_modifier.get(modifier)) \
                if getattr(data_frame.abilities, qtl.temp_ability_modifier.get(modifier)) != '' \
                else getattr(data_frame.abilities, qtl.ability_modifier.get(modifier))
            self.set_skill_attributes(skill_name, skill_data, actual_modifier)

        self.craft10.setText(data_frame.skills.craft1.name)
        self.craft20.setText(data_frame.skills.craft2.name)
        self.craft30.setText(data_frame.skills.craft3.name)

        self.perform10.setText(data_frame.skills.perform1.name)
        self.perform20.setText(data_frame.skills.perform2.name)

        self.profession10.setText(data_frame.skills.profession1.name)
        self.profession20.setText(data_frame.skills.profession2.name)

        self.conditionalModifiers.setText(data_frame.skills.conditionalModifiers)

        self.languages.setText(data_frame.skills.languages)
        self.levelTotal.setText(data_frame.skills.xp.total)
        self.levelNext.setText(data_frame.skills.xp.toNextLevel)

        self.totalRanks.setText(data_frame.skills.totalRanks)

        # self.tabWidget.addTab(QtWidgets.QLabel("Widget in Tab 1."), "Test")

        # Write data to defense block in gui
        self.ac_total.setText(data_frame.defense.ac.total)
        self.ac_armorBonus.setText(data_frame.defense.ac.armorBonus)
        self.ac_shieldBonus.setText(data_frame.defense.ac.shieldBonus)
        self.ac_dexModifier.setText(data_frame.abilities.tempDexModifier
                                    if data_frame.abilities.tempDexModifier != ""
                                    else data_frame.abilities.dexModifier)
        self.ac_sizeModifier.setText(data_frame.defense.ac.sizeModifier)
        self.ac_naturalArmor.setText(data_frame.defense.ac.naturalArmor)
        self.ac_DeflectionModifier.setText(data_frame.defense.ac.deflectionModifier)
        self.ac_miscModifier.setText(data_frame.defense.ac.miscModifier)
        self.ac_touch.setText(data_frame.defense.ac.touch)
        self.ac_flatFooted.setText(data_frame.defense.ac.flatFooted)
        self.ac_otherModifiers.setText(data_frame.defense.ac.otherModifiers)

        self.hp_total.setText(data_frame.defense.hp.total)
        self.hp_wounds.setText(data_frame.defense.hp.wounds)
        self.hp_nonLethal.setText(data_frame.defense.hp.nonLethal)
        self.damageReduction.setText(data_frame.defense.damageReduction)
        self.spellResistance.setText(data_frame.defense.spellResistance)

        self.fort_total.setText(data_frame.defense.fort.total)
        self.fort_base.setText(data_frame.defense.fort.base)
        self.fort_abilityModifier.setText(data_frame.abilities.tempConModifier
                                  if data_frame.abilities.tempConModifier != ""
                                  else data_frame.abilities.conModifier)
        self.fort_magicModifier.setText(data_frame.defense.fort.magicModifier)
        self.fort_tempModifier.setText(data_frame.defense.fort.tempModifier)
        self.fort_otherModifiers.setText(data_frame.defense.fort.otherModifiers)

        self.reflex_total.setText(data_frame.defense.reflex.total)
        self.reflex_base.setText(data_frame.defense.reflex.base)
        self.reflex_abilityModifier.setText(data_frame.abilities.tempDexModifier
                                            if data_frame.abilities.tempDexModifier != ""
                                            else data_frame.abilities.dexModifier)
        self.reflex_magicModifier.setText(data_frame.defense.reflex.magicModifier)
        self.reflex_tempModifier.setText(data_frame.defense.reflex.tempModifier)
        self.reflex_otherModifiers.setText(data_frame.defense.reflex.otherModifiers)

        self.will_total.setText(data_frame.defense.will.total)
        self.will_base.setText(data_frame.defense.will.base)
        self.will_abilityModifier.setText(data_frame.abilities.tempWisModifier
                                          if data_frame.abilities.tempWisModifier != ""
                                          else data_frame.abilities.wisModifier)
        self.will_magicModifier.setText(data_frame.defense.will.magicModifier)
        self.will_tempModifier.setText(data_frame.defense.will.tempModifier)
        self.will_otherModifiers.setText(data_frame.defense.will.otherModifiers)

        self.cmd_total.setText(data_frame.defense.cmd.total)
        self.cmd_strModifier.setText(data_frame.abilities.tempStrModifier
                                     if data_frame.abilities.tempStrModifier != ""
                                     else data_frame.abilities.strModifier)
        self.cmd_dexModifier.setText(data_frame.abilities.tempDexModifier
                                     if data_frame.abilities.tempDexModifier != ""
                                     else data_frame.abilities.dexModifier)
        self.cmd_sizeModifier.setText(data_frame.defense.cmd.sizeModifier)
        self.cmd_miscModifiers.setText(data_frame.defense.cmd.miscModifier)
        self.cmd_tempModifiers.setText(data_frame.defense.cmd.tempModifier)

        self.resistances.setText(data_frame.defense.resistances)
        self.immunities.setText(data_frame.defense.immunities)

        self.cmd_bab.setText(data_frame.offense.bab)

        # Write data to offense block in gui
        self.initiative_total.setText(data_frame.offense.initiative.total)
        self.initiative_dexModifier.setText(data_frame.abilities.tempDexModifier
                                            if data_frame.abilities.tempDexModifier != ""
                                            else data_frame.abilities.dexModifier)
        self.initiative_miscModifier.setText(data_frame.offense.initiative.miscModifier)
        self.bab.setText(data_frame.offense.bab)
        self.conditionalOffenseModifiers.setText(data_frame.offense.conditionalOffenseModifiers)
        self.speed_base.setText(data_frame.offense.speed.base)
        self.speed_withArmor.setText(data_frame.offense.speed.withArmor)
        self.speed_fly.setText(data_frame.offense.speed.fly)
        self.speed_swim.setText(data_frame.offense.speed.swim)
        self.speed_climb.setText(data_frame.offense.speed.climb)
        self.speed_burrow.setText(data_frame.offense.speed.burrow)
        self.speed_tempModifiers.setText(data_frame.offense.speed.tempModifiers)
        self.cmb_total.setText(data_frame.offense.cmb.total)
        self.cmb_bab.setText(data_frame.offense.bab)
        self.cmb_strModifier.setText(data_frame.abilities.tempStrModifier
                                     if data_frame.abilities.tempStrModifier != ""
                                     else data_frame.abilities.strModifier)
        self.cmb_sizeModifier.setText(data_frame.offense.cmb.sizeModifier)
        self.cmb_miscModifiers.setText(data_frame.offense.cmb.miscModifiers)
        self.cmb_tempModifiers.setText(data_frame.offense.cmb.tempModifiers)

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
