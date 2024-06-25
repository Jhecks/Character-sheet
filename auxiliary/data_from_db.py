import time
from auxiliary import data_base_handler as dBH


class DataFromDB:
    def __init__(self):
        start_time = time.time()
        self.init_spells()
        self.init_feats()
        self.init_traits()
        print('Data in DataFromDB loaded in', time.time() - start_time, 'seconds.')

    def init_spells(self):
        self.spell_names = dBH.get_all_names_of_spells()
        self.spell_names_lower = [x.lower() for x in self.spell_names]
        self.spell_schools = dBH.get_all_schools_of_spells()
        self.spell_schools = [x.title() for x in self.spell_schools]
        self.spell_subschools = dBH.get_all_subschools_of_spells()
        self.spell_subschools = list(filter(lambda item: item is not None, self.spell_subschools))
        self.spell_subschools = [x.capitalize() for x in self.spell_subschools if not None]
        self.spell_names.insert(0, '')
        self.spell_names_lower.insert(0, '')
        self.spell_schools.insert(0, '')
        self.spell_subschools.insert(0, '')

    def init_feats(self):
        self.feat_names = dBH.get_all_names_of_feats()
        self.feat_names_lower = [x.lower() for x in self.feat_names]
        self.feat_types = dBH.get_all_types_of_feats()
        self.feat_types = [x.title() for x in self.feat_types]
        self.feat_sources = dBH.get_all_sources_of_feats()
        self.feat_sources.insert(0, '')
        self.feat_names.insert(0, '')
        self.feat_names_lower.insert(0, '')
        self.feat_types.insert(0, '')

    def init_traits(self):
        self.trait_names = dBH.get_all_names_of_traits()
        self.trait_names_lower = [x.lower() for x in self.trait_names]
        self.trait_types = dBH.get_all_types_of_traits()
        self.trait_types = [x.title() for x in set(self.trait_types)]
        self.trait_sources = dBH.get_all_sources_of_traits()
        self.trait_sources.insert(0, '')
        self.trait_names.insert(0, '')
        self.trait_names_lower.insert(0, '')
        self.trait_types.insert(0, '')

    def get_spell_data_from_name(self, name):
        if name.lower() in self.spell_names_lower:
            return self.get_spell_data_from_index(self.spell_names_lower.index(name.lower()))
        else:
            return None

    def get_spell_data_from_index(self, index_of_spell_name=0):
        if index_of_spell_name == 0 or index_of_spell_name >= len(self.spell_names):
            return ({
                'name': '',
                'school': '',
                'subschool': '',
                'description': ''
            })

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

    def get_feat_data_from_name(self, name):
        if name.lower() in self.feat_names_lower:
            return self.get_feat_data_from_index(self.feat_names_lower.index(name.lower()))
        else:
            return None

    def get_feat_data_from_index(self, index_of_feat_name=0):
        if index_of_feat_name == 0 or index_of_feat_name >= len(self.feat_names):
            return ({
                'name': '',
                'type': '',
                'source': '',
                'description': ''
            })

        data_from_db = dBH.get_data_from_db_by_feat_name(self.feat_names[index_of_feat_name])
        # TODO: Fix multiple entries for traits
        data_from_db = data_from_db[0]
        html_data = data_from_db[1]
        html_data = html_data.replace('<link rel="stylesheet"href="PF.css">', '')

        return ({
            'name': self.feat_names[index_of_feat_name],
            'type': data_from_db[0],
            'source': data_from_db[2],
            'description': html_data
        })

    def get_trait_data_from_name(self, name):
        if name.lower() in self.trait_names_lower:
            return self.get_trait_data_from_index(self.trait_names_lower.index(name.lower()))
        else:
            return None

    def get_trait_data_from_index(self, index_of_trait_name=0):
        if index_of_trait_name == 0 or index_of_trait_name >= len(self.trait_names):
            return ({
                'name': '',
                'type': '',
                'source': '',
                'description': ''
            })

        data_from_db = dBH.get_data_from_db_by_trait_name(self.trait_names[index_of_trait_name])
        # TODO: Fix multiple entries for traits
        data_from_db = data_from_db[0]
        return ({
            'name': self.trait_names[index_of_trait_name],
            'type': data_from_db[0],
            'source': data_from_db[2],
            'description': data_from_db[1]
        })

    def update_spell_data(self, dict_of_data, update=False):
        if dict_of_data['name'].lower() in self.spell_names_lower and not update:
            return
        dict_of_data['name'] = dict_of_data['name'].title()
        dBH.insert_spell_data(dict_of_data)
        self.init_spells()

    def update_feat_data(self, dict_of_data):
        if dict_of_data['name'].lower() in self.feat_names_lower:
            return
        dict_of_data['name'] = dict_of_data['name'].title()
        dBH.insert_feat_data(dict_of_data)
        self.init_feats()

    def update_trait_data(self, dict_of_data):
        if dict_of_data['name'].lower() in self.trait_names_lower:
            return
        dict_of_data['name'] = dict_of_data['name'].title()
        dBH.insert_trait_data(dict_of_data)
        self.init_traits()


spell_data = DataFromDB()
