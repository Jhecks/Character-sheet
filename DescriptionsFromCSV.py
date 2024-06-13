import os
import pandas as pd


# This class is used to get data from the CSV files that contain the spell and feat data
class DataFromCSV:
    def __init__(self):
        spell_data_path = os.getcwd() + '\\_data_files\\spell_full.csv'
        feat_data_path = os.getcwd() + '\\_data_files\\feat_ogl.csv'
        trait_data_path = os.getcwd() + '\\_data_files\\trait.csv'

        self.spell_df = pd.read_csv(spell_data_path)
        self.feat_df = pd.read_csv(feat_data_path)
        self.trait_df = pd.read_csv(trait_data_path)

        self.spell_names = self.spell_df.get('name').tolist()
        self.spell_names_lower = [x.lower() for x in self.spell_names]
        self.spell_schools = self.spell_df.get('school').tolist()
        self.spell_schools = [x.title() for x in set(self.spell_schools)]
        self.spell_subschools = self.spell_df.get('subschool').tolist()
        self.spell_subschools = [x.capitalize() for x in set(self.spell_subschools) if not isinstance(x, float)]

        self.feat_names = self.feat_df.get('name').tolist()
        self.feat_names_lower = [x.lower() for x in self.feat_names]
        self.feat_types = self.feat_df.get('type').tolist()
        self.feat_types = [x.title() for x in set(self.feat_types)]

        self.trait_names = self.trait_df.get('Name').tolist()
        self.trait_names_lower = [x.lower() for x in self.trait_names]
        self.trait_types = self.trait_df.get('Trait List').tolist()
        self.trait_types = [x.title() for x in set(self.trait_types)]

    def check_spell_availability(self, text):
        if text.lower() in self.spell_names_lower:
            return self.get_data_from_name(self.spell_names_lower.index(text.lower()))
        else:
            return None

    def get_data_from_name(self, index_of_spell_name=None):
        if index_of_spell_name is None:
            return None

        html_data = self.spell_df.iloc[self.spell_names.index(self.spell_names[index_of_spell_name])]['full_text']
        html_data = html_data.replace('<link rel="stylesheet"href="PF.css">', '')

        school = self.spell_df.iloc[self.spell_names.index(self.spell_names[index_of_spell_name])]['school']
        if isinstance(school, float):
            school = ''
        else:
            school = school.title()
        subschool = self.spell_df.iloc[self.spell_names.index(self.spell_names[index_of_spell_name])]['subschool']
        if isinstance(subschool, float):
            subschool = ''
        else:
            subschool = subschool.title()

        # print(self.spell_df.iloc[self.spell_names.index(self.spell_names[index_of_spell_name])]['linktext'])

        return ({
            'name': self.spell_names[index_of_spell_name],
            'school': school,
            'subschool': subschool,
            'description': html_data
        })

    def check_feat_availability(self, text):
        if text.lower() in self.feat_names_lower:
            return self.get_feat_data_from_name(self.feat_names_lower.index(text.lower()))
        else:
            return None

    def get_feat_data_from_name(self, index_of_feat_name=None):
        if index_of_feat_name is None:
            return None

        html_data = self.feat_df.iloc[self.feat_names.index(self.feat_names[index_of_feat_name])]['fulltext']
        html_data = html_data.replace('<link rel="stylesheet"href="PF.css">', '')

        return ({
            'name': self.feat_names[index_of_feat_name],
            'type': self.feat_df.iloc[self.feat_names.index(self.feat_names[index_of_feat_name])]['type'],
            'description': html_data
        })

    def check_trait_availability(self, text):
        if text.lower() in self.trait_names_lower:
            return self.get_trait_data_from_name(self.trait_names_lower.index(text.lower()))
        else:
            return None

    def get_trait_data_from_name(self, index_of_trait_name=None):
        if index_of_trait_name is None:
            return None

        html_data = self.trait_df.iloc[self.trait_names.index(self.trait_names[index_of_trait_name])]['Benefit']
        return ({
            'name': self.trait_names[index_of_trait_name],
            'type': self.trait_df.iloc[self.trait_names.index(self.trait_names[index_of_trait_name])]['Trait List'],
            'description': html_data
        })
