import os
import pandas as pd


# This class is used to get data from the CSV files that contain the spell and feat data
class DataFromCSV:
    def __init__(self):
        self.spell_data_path = os.getcwd() + '\\_data_files\\spells.csv'
        self.feat_data_path = os.getcwd() + '\\_data_files\\feats.csv'
        self.trait_data_path = os.getcwd() + '\\_data_files\\traits.csv'

        self.spell_df = pd.read_csv(self.spell_data_path)
        self.feat_df = pd.read_csv(self.feat_data_path)
        self.trait_df = pd.read_csv(self.trait_data_path)

        self.spell_names = self.spell_df.get('name').tolist()
        self.spell_names_lower = [x.lower() for x in self.spell_names]
        self.spell_schools = self.spell_df.get('school').tolist()
        self.spell_schools = [x.title() for x in set(self.spell_schools)]
        self.spell_subschools = self.spell_df.get('subschool').tolist()
        self.spell_subschools = [x.capitalize() for x in set(self.spell_subschools) if not isinstance(x, float)]
        self.spell_schools.sort()
        self.spell_subschools.sort()
        self.spell_schools.insert(0, '')
        self.spell_subschools.insert(0, '')

        self.feat_names = self.feat_df.get('name').tolist()
        self.feat_names_lower = [x.lower() for x in self.feat_names]
        self.feat_types = self.feat_df.get('type').tolist()
        self.feat_types = [x.title() for x in set(self.feat_types)]

        self.trait_names = self.trait_df.get('name').tolist()
        self.trait_names_lower = [x.lower() for x in self.trait_names]
        self.trait_types = self.trait_df.get('type').tolist()
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

        html_data = self.feat_df.iloc[self.feat_names.index(self.feat_names[index_of_feat_name])]['full_text']
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

        html_data = self.trait_df.iloc[self.trait_names.index(self.trait_names[index_of_trait_name])]['full_text']
        return ({
            'name': self.trait_names[index_of_trait_name],
            'type': self.trait_df.iloc[self.trait_names.index(self.trait_names[index_of_trait_name])]['type'],
            'description': html_data
        })

    def update_spell_data(self, dict_of_data):
        dict_of_data['name'] = dict_of_data['name'].title()
        input_data = pd.DataFrame(dict_of_data, index=[0])
        self.spell_df = self.spell_df._append(input_data, ignore_index=True)
        self.spell_names.append(dict_of_data['name'])
        self.spell_names_lower.append(dict_of_data['name'].lower())
        self.rename_file(self.spell_data_path, self.spell_data_path + '.bak')
        self.spell_df.to_csv(self.spell_data_path, index=False)

    def rename_file(self, old_name, new_name):
        try:
            if os.path.exists(new_name):
                os.remove(new_name)
                print(f"File {new_name} removed.")

            os.rename(old_name, new_name)
            print(f"File renamed successfully from {old_name} to {new_name}")
        except FileNotFoundError:
            print(f"The file {old_name} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
