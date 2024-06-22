import time

import dataBaseHandler as dBH


class DataFromDB:
    def __init__(self):
        start_time = time.time()

        self.spell_names = dBH.get_all_names_of_spells()
        self.spell_names_lower = [x.lower() for x in self.spell_names]
        self.spell_schools = dBH.get_all_schools_of_spells()
        self.spell_schools = [x.title() for x in self.spell_schools]
        self.spell_subschools = dBH.get_all_subschools_of_spells()
        self.spell_subschools = [x.capitalize() for x in self.spell_subschools if not None]
        self.spell_schools.sort()
        self.spell_subschools.sort()
        self.spell_schools.insert(0, '')
        self.spell_subschools.insert(0, '')

        self.feat_names = dBH.get_all_names_of_feats()
        self.feat_names_lower = [x.lower() for x in self.feat_names]
        self.feat_types = dBH.get_all_types_of_feats()
        self.feat_types = [x.title() for x in self.feat_types]
        self.feat_names.sort()
        self.feat_names.insert(0, '')
        self.feat_types.sort()
        self.feat_types.insert(0, '')

        self.trait_names = dBH.get_all_names_of_traits()
        self.trait_names_lower = [x.lower() for x in self.trait_names]
        self.trait_types = dBH.get_all_types_of_traits()
        self.trait_types = [x.title() for x in set(self.trait_types)]
        self.trait_names.sort()
        self.trait_names.insert(0, '')
        self.trait_types.sort()
        self.trait_types.insert(0, '')
        print('Data loaded in', time.time() - start_time, 'seconds.')

    def get_data_from_name_index(self, index_of_spell_name=0):
        if index_of_spell_name is 0:
            return None

        data_from_db = dBH.get_data_from_db_by_spell_name(self.spell_names[index_of_spell_name])
        html_data = data_from_db[2]
        html_data = html_data.replace('<link rel="stylesheet"href="PF.css">', '')

        school = data_from_db[0]
        if school is None:
            school = ''
        else:
            school = school.title()
        subschool = data_from_db[1]
        if subschool is None:
            subschool = ''
        else:
            subschool = subschool.title()

        return ({
            'name': self.spell_names[index_of_spell_name],
            'school': school,
            'subschool': subschool,
            'description': html_data
        })

    def get_feat_data_from_name(self, index_of_feat_name=0):
        if index_of_feat_name is 0:
            return None

        data_from_db = dBH.get_data_from_db_by_feat_name(self.feat_names[index_of_feat_name])
        html_data = data_from_db[2]
        html_data = html_data.replace('<link rel="stylesheet"href="PF.css">', '')

        return ({
            'name': self.feat_names[index_of_feat_name],
            'type': data_from_db[0],
            'description': html_data
        })

    def get_trait_data_from_name(self, index_of_trait_name=0):
        if index_of_trait_name is 0:
            return None

        data_from_db = dBH.get_data_from_db_by_trait_name(self.trait_names[index_of_trait_name])
        html_data = data_from_db[1]
        return ({
            'name': self.trait_names[index_of_trait_name],
            'type': data_from_db[0],
            'description': html_data
        })
