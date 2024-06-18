import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication
from main import *
import sys
import qtTranslateLayer as qtl

# Assuming the code above is in a file named main.py
from main import MainWindow, Themes


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

    def test_str_to_int_with_negative_number(self):
        result = self.main_window.str_to_int("-123")
        self.assertEqual(result, -123)

    def test_str_to_int_with_zero(self):
        result = self.main_window.str_to_int("0")
        self.assertEqual(result, 0)

    def test_str_to_int_with_empty_string(self):
        result = self.main_window.str_to_int("")
        self.assertEqual(result, 0)

    @patch('main.jsonParser.xml_to_character_sheet')
    def test_selectFile_with_valid_file(self, mock_json_parser):
        mock_json_parser.return_value = MagicMock()
        self.main_window.filedialog.askopenfilename = MagicMock(return_value="valid_file.json")
        self.main_window.selectFile()
        mock_json_parser.assert_called_once_with("valid_file.json")

    @patch('main.jsonParser.xml_to_character_sheet')
    def test_selectFile_with_no_file_selected(self, mock_json_parser):
        self.main_window.filedialog.askopenfilename = MagicMock(return_value="")
        self.main_window.selectFile()
        mock_json_parser.assert_not_called()

    @patch('main.jsonParser.character_sheet_to_xml')
    def test_saveFile_with_existing_file_path(self, mock_json_parser):
        self.main_window.file_path = "existing_file.json"
        self.main_window.data_frame.create_json = MagicMock(return_value={})
        self.main_window.saveFile()
        mock_json_parser.assert_called_once_with("existing_file.json", {})

    @patch('main.jsonParser.character_sheet_to_xml')
    def test_saveFile_with_no_file_path(self, mock_json_parser):
        self.main_window.file_path = None
        self.main_window.saveFile()
        mock_json_parser.assert_not_called()

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
