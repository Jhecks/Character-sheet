import sys
import unittest

from PyQt5 import QtCore

import main
from auxiliary import qt_translate_layer as qtl

from PyQt5.QtWidgets import QApplication

# Assuming the code above is in a file named main.py
from main import MainWindow, Themes
from PyQt5.QtTest import QTest
# from main import *


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        # self.main_window.show()
        # self.app.exec()

    def test_str_to_int_with_negative_number(self):
        result = main.str_to_int("-321")
        self.assertEqual(result, -321)

    def test_str_to_int_with_zero(self):
        result = main.str_to_int("0")
        self.assertEqual(result, 0)

    def test_str_to_int_with_empty_string(self):
        result = main.str_to_int("")
        self.assertEqual(result, 0)

    def test_str_to_int_with_positive_number(self):
        result = main.str_to_int("+321")
        self.assertEqual(result, 321)

    def test_general_main_window(self):
        for attr in qtl.general_attributes:
            QTest.keyClicks(getattr(self.main_window, attr), "Test_" + attr)
        for attr in qtl.general_attributes:
            self.assertEqual(getattr(self.main_window.data_frame.general, attr), "Test_" + attr)

        # self.main_window.show()
        # self.app.exec()

    def test_ability_main_window(self):
        random_data = [0, -1, +2, 'test', 4, 5, 6, '7dsfgsdf', 8, 9, 10, 11]
        for attr, data in zip(qtl.ability_editable_attributes, random_data):
            QTest.keyClicks(getattr(self.main_window, attr), str(data))
        for attr, data in zip(qtl.ability_editable_attributes, random_data):
            self.assertEqual(getattr(self.main_window.data_frame.abilities, attr), str(data))
        # self.main_window.show()
        # self.app.exec()

    def test_spells_main_window(self):
        QTest.mouseClick(self.main_window.addSpellLike, QtCore.Qt.LeftButton)
        for i in range(self.main_window.ui.name.count()):
            self.main_window.ui.name.setCurrentIndex(i)
            self.assertEqual(self.main_window.ui.name.currentText(), self.main_window.spell_data.spell_names[i])
            self.assertEqual(self.main_window.ui.school.currentText(), self.main_window.spell_data.get_spell_data_from_index(i)['school'])
            self.assertEqual(self.main_window.ui.subschool.currentText(), self.main_window.spell_data.get_spell_data_from_index(i)['subschool'])

    def test_feats_main_window(self):
        QTest.mouseClick(self.main_window.addFeat, QtCore.Qt.LeftButton)
        for i in range(self.main_window.ui.name.count()):
            self.main_window.ui.name.setCurrentIndex(i)
            self.assertEqual(self.main_window.ui.name.currentText(), self.main_window.spell_data.feat_names[i])
            self.assertEqual(self.main_window.ui.type.currentText(), self.main_window.spell_data.get_feat_data_from_index(i)['type'])

    def test_traits_main_window(self):
        QTest.mouseClick(self.main_window.addTrait, QtCore.Qt.LeftButton)
        for i in range(self.main_window.ui.name.count()):
            self.main_window.ui.name.setCurrentIndex(i)
            self.assertEqual(self.main_window.ui.name.currentText(), self.main_window.spell_data.trait_names[i])
            self.assertEqual(self.main_window.ui.type.currentText(), self.main_window.spell_data.get_trait_data_from_index(i)['type'])

    # def check_sort(self):


    # @patch('main.jsonParser.xml_to_character_sheet')
    # def test_selectFile_with_valid_file(self, mock_json_parser):
    #     mock_json_parser.return_value = MagicMock()
    #     self.main_window.filedialog.askopenfilename = MagicMock(return_value="valid_file.json")
    #     self.main_window.selectFile()
    #     mock_json_parser.assert_called_once_with("valid_file.json")
    #
    # @patch('main.jsonParser.xml_to_character_sheet')
    # def test_selectFile_with_no_file_selected(self, mock_json_parser):
    #     self.main_window.filedialog.askopenfilename = MagicMock(return_value="")
    #     self.main_window.selectFile()
    #     mock_json_parser.assert_not_called()
    #
    # @patch('main.jsonParser.character_sheet_to_xml')
    # def test_saveFile_with_existing_file_path(self, mock_json_parser):
    #     self.main_window.file_path = "existing_file.json"
    #     self.main_window.data_frame.create_json = MagicMock(return_value={})
    #     self.main_window.saveFile()
    #     mock_json_parser.assert_called_once_with("existing_file.json", {})
    #
    # @patch('main.jsonParser.character_sheet_to_xml')
    # def test_saveFile_with_no_file_path(self, mock_json_parser):
    #     self.main_window.file_path = None
    #     self.main_window.saveFile()
    #     mock_json_parser.assert_not_called()

    def test_set_dark_theme(self):
        self.main_window.set_dark_theme()
        self.assertEqual(self.main_window.actualTheme, Themes.dark)
        self.assertTrue(self.main_window.actionDark_theme_2.isChecked())
        self.assertFalse(self.main_window.actionLight_theme_2.isChecked())

    def test_set_light_theme(self):
        self.main_window.set_light_theme()
        self.assertEqual(self.main_window.actualTheme, Themes.light)
        self.assertFalse(self.main_window.actionDark_theme_2.isChecked())
        self.assertTrue(self.main_window.actionLight_theme_2.isChecked())


if __name__ == '__main__':
    unittest.main()
