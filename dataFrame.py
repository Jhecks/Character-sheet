import json

from main import *


class CharacterSheetData:
    point_table = {
        7: -4,
        8: -2,
        9: -1,
        10: 0,
        11: 1,
        12: 2,
        13: 3,
        14: 5,
        15: 7,
        16: 10,
        17: 13,
        18: 17
    }

    def __init__(self):
        self.general = self.General()
        self.abilities = self.Abilities()
        self.spells = self.Spells()
        self.offense = self.Offense(self.abilities)
        self.defense = self.Defense(self.abilities, self.offense)
        self.skills = self.Skills(self.abilities)
        self.money = self.Money()
        self.gears = self.Gears()
        self.traits = self.Traits()
        self.feats = self.Feats()
        self.specialAbilities = self.SpecialAbilities()
        self.attacks = self.Attacks()
        self.notes = ""
        self.attributes = ['general', 'abilities', 'spells', 'offense', 'defense', 'skills', 'money',
                           'gears', 'traits', 'feats', 'specialAbilities', 'attacks', 'notes']

    def create_from_json(self, json_data):
        self.general.create_from_json(json_data)
        self.abilities.create_from_json(json_data)
        self.defense.create_from_json(json_data)
        self.offense.create_from_json(json_data)
        self.skills.create_from_json(json_data)
        self.money.create_from_json(json_data)
        self.spells.create_from_json(json_data)
        self.gears.create_from_json(json_data)
        self.traits.create_from_json(json_data)
        self.feats.create_from_json(json_data)
        self.specialAbilities.create_from_json(json_data)
        self.attacks.create_from_json(json_data)
        self.notes = json_data.get("notes")

    def update_data(self):
        self.abilities.count_score()
        self.abilities.update_modifiers()
        self.skills.update_skills(self.abilities)
        self.defense.update_defence(self.abilities, self.offense)
        self.offense.update_offense_data(self.abilities)

    def create_json(self):
        output_json = {}
        for general_data in self.general.attributes:
            output_json[general_data] = getattr(self.general, general_data)

        output_json['skills'] = {}
        for skill_data in self.skills.attributes:
            output_json['skills'][skill_data] = {}
            for data in getattr(self.skills, skill_data).attributes:
                output_json['skills'][skill_data][data] = getattr(getattr(self.skills, skill_data), data)

        output_json['spells'] = []
        for n_level_spell in self.spells.attributes:
            spell_data = {}
            for n_level_data in getattr(self.spells, n_level_spell).attributes:
                spell_data[n_level_data] = getattr(getattr(self.spells, n_level_spell), n_level_data)
            spell_data['slotted'] = []
            for slotted_data in getattr(self.spells, n_level_spell).slotted:
                slotted_data_data = {}
                for slotted_data_spell in slotted_data.attributes:
                    slotted_data_data[slotted_data_spell] = getattr(slotted_data, slotted_data_spell)
                spell_data['slotted'].append(slotted_data_data)
            output_json['spells'].append(spell_data)
        output_json['spellsSpeciality'] = self.spells.spellsSpeciality
        output_json['spellsConditionalModifiers'] = self.spells.spellsConditionalModifiers

        output_json['abilities'] = {}
        for ability in self.abilities.attributes:
            output_json['abilities'][ability] = getattr(self.abilities, ability)

        output_json['ac'] = {}
        for ac in self.defense.ac.attributes:
            output_json['ac'][ac] = getattr(self.defense.ac, ac)
        output_json['ac']['items'] = []
        for ac_item in self.defense.ac.items.list:
            item_data = {}
            for ac_item_data in ac_item.attributes:
                item_data[ac_item_data] = getattr(ac_item, ac_item_data)
            output_json['ac']['items'].append(item_data)
        output_json['ac']['itemTotals'] = {}
        for item_total in self.defense.ac.itemsTotals.attributes:
            output_json['ac']['itemTotals'][item_total] = getattr(self.defense.ac.itemsTotals, item_total)

        output_json['damageReduction'] = self.defense.damageReduction
        output_json['hp'] = {}
        for hp_data in self.defense.hp.attributes:
            output_json['hp'][hp_data] = getattr(self.defense.hp, hp_data)
        output_json['spellResistance'] = self.defense.spellResistance

        output_json['cmd'] = {}
        for cmd_data in self.defense.cmd.attributes:
            output_json['cmd'][cmd_data] = getattr(self.defense.cmd, cmd_data)
        output_json['immunities'] = self.defense.immunities
        output_json['resistances'] = self.defense.resistances

        output_json['saves'] = {}
        for save in self.defense.save_attributes:
            output_json['saves'][save] = {}
            for save_data in getattr(self.defense, save).attributes:
                output_json['saves'][save][save_data] = getattr(getattr(self.defense, save), save_data)

        output_json['bab'] = self.offense.bab
        output_json['cmb'] = {}
        for cmb_data in self.offense.cmb.attributes:
            output_json['cmb'][cmb_data] = getattr(self.offense.cmb, cmb_data)
        output_json['conditionalOffenseModifiers'] = self.offense.conditionalOffenseModifiers
        output_json['initiative'] = {}
        output_json['initiative']['total'] = self.offense.initiative.total
        output_json['initiative']['miscModifier'] = self.offense.initiative.miscModifier

        output_json['melee'] = []
        for melee in self.attacks.melee:
            melee_attack = {}
            for melee_data in melee.attributes:
                melee_attack[melee_data] = getattr(melee, melee_data)
            output_json['melee'].append(melee_attack)

        output_json['ranged'] = []
        for ranged in self.attacks.ranged:
            ranged_attack = {}
            for ranged_data in ranged.attributes:
                ranged_attack[ranged_data] = getattr(ranged, ranged_data)
            output_json['ranged'].append(ranged_attack)

        output_json['speed'] = {}
        for speed_data in self.offense.speed.attributes:
            output_json['speed'][speed_data] = getattr(self.offense.speed, speed_data)

        output_json['feats'] = []
        for feat in self.feats.list:
            feat_data = {}
            for feat_data_data in feat.attributes:
                feat_data[feat_data_data] = getattr(feat, feat_data_data)
            output_json['feats'].append(feat_data)
        output_json['languages'] = self.skills.languages
        output_json['xp'] = {}
        output_json['xp']['total'] = self.skills.xp.total
        output_json['xp']['toNextLevel'] = self.skills.xp.toNextLevel

        output_json['specialAbilities'] = []
        for specialAbility in self.specialAbilities.list:
            specialAbility_data = {}
            for specialAbilities_data_data in specialAbility.attributes:
                specialAbility_data[specialAbilities_data_data] = getattr(specialAbility, specialAbilities_data_data)
            output_json['specialAbilities'].append(specialAbility_data)

        output_json['traits'] = []
        for trait in self.traits.list:
            trait_data = {}
            for trait_data_data in trait.attributes:
                trait_data[trait_data_data] = getattr(trait, trait_data_data)
            output_json['traits'].append(trait_data)

        output_json['money'] = {}
        for money in self.money.attributes:
            output_json['money'][money] = getattr(self.money, money)

        output_json['gear'] = []
        for gear in self.gears.list:
            gear_data = {}
            for gear_data_data in gear.attributes:
                gear_data[gear_data_data] = getattr(gear, gear_data_data)
            output_json['gear'].append(gear_data)

        output_json['spellLikes'] = []
        for spellLike in self.spells.spellLikes:
            spellLike_data = {}
            for spellLike_data_data in spellLike.attributes:
                spellLike_data[spellLike_data_data] = getattr(spellLike, spellLike_data_data)
            output_json['spellLikes'].append(spellLike_data)

        output_json['notes'] = self.notes
        return output_json

    def __str__(self):
        string = str.format("{}\n{}\n{}", self.general, self.abilities, self.skills)
        return string

    def __eq__(self, other):
        for attribute in self.attributes:
            if getattr(self, attribute) != getattr(other, attribute):
                return False
        return True

    class General:
        def __init__(self):
            self.name = ""  # Character Name
            self.alignment = ""
            self.level = ""  # Character class and level
            self.deity = ""
            self.homeland = ""
            self.race = ""
            self.size = ""
            self.gender = ""
            self.age = ""
            self.height = ""
            self.weight = ""
            self.hair = ""
            self.eyes = ""
            self.playerName = ""

            self.attributes = [
                "name", "alignment", "level",
                "deity", "homeland", "race", "size", "gender", "age", "height", "weight",
                "hair", "eyes"
            ]

        def create_from_json(self, json_data):
            for attribute in self.attributes:
                if json_data.get(attribute):
                    setattr(self, attribute, json_data.get(attribute, ''))

        def __str__(self):
            string = str.format("\tGeneral\n\nCharacter Name: {}\tAlignment: {}\tPlayer Name:\n"
                                "Character Class & Level: {}\tDeity: {}\tHomeland: {}\n"
                                "Race: {}\tSize: {}\tGender: {}\tAge: {}\tHeight: {}\tWeight: {}\tHair: {}\tEyes: {}",
                                self.name, self.alignment,
                                self.level, self.deity, self.homeland,
                                self.race, self.size, self.gender, self.age, self.height, self.weight, self.hair,
                                self.eyes)
            return string

        def __eq__(self, other):
            for attribute in self.attributes:
                if getattr(self, attribute) != getattr(other, attribute):
                    return False
            return True

    class Abilities:
        def __init__(self):
            self.scoreCalc = ""

            self.str = ""
            self.int = ""
            self.wis = ""
            self.dex = ""
            self.con = ""
            self.cha = ""

            self.strModifier = ""
            self.intModifier = ""
            self.wisModifier = ""
            self.dexModifier = ""
            self.conModifier = ""
            self.chaModifier = ""

            self.tempStr = ""
            self.tempInt = ""
            self.tempWis = ""
            self.tempDex = ""
            self.tempCon = ""
            self.tempCha = ""

            self.tempStrModifier = ""
            self.tempIntModifier = ""
            self.tempWisModifier = ""
            self.tempDexModifier = ""
            self.tempConModifier = ""
            self.tempChaModifier = ""

            self.attributes = ["str", "int", "wis", "dex", "con", "cha",
                               "tempStr", "tempInt", "tempWis", "tempDex", "tempCon", "tempCha"]

        def create_from_json(self, json_data):
            json_ability_data = json_data.get("abilities")
            if json_ability_data:
                for attribute in self.attributes:
                    if json_ability_data.get(attribute):
                        setattr(self, attribute, json_ability_data.get(attribute))
                        modifier = str(attribute) + "Modifier"
                        setattr(self, modifier, self.get_ability_modifier(json_ability_data.get(attribute)))
                self.count_score()

        def count_score(self):
            attributes = ["str", "int", "wis", "dex", "con", "cha"]
            self.scoreCalc = 0
            for attribute in attributes:
                attribute_data = getattr(self, attribute)
                if attribute_data.isdigit():
                    if 6 < int(attribute_data) < 19:
                        self.scoreCalc += CharacterSheetData.point_table.get(int(attribute_data))
                    else:
                        self.scoreCalc = "-"
                        return
            self.scoreCalc = str(self.scoreCalc)

        def update_modifiers(self):
            for attribute in self.attributes:
                modifier = str(attribute) + "Modifier"
                setattr(self, modifier, self.get_ability_modifier(getattr(self, attribute)))

        def get_ability_modifier(self, ability_score):
            if not str.isnumeric(ability_score):
                return ""
            ability_score = int(ability_score)
            modifier = (ability_score - 10) // 2
            return ("+" + str(modifier)) if (modifier > 0) else str(modifier)

        def __str__(self):
            string = str.format("\tAbilities\n\nstr: {} {}\tdex: {} {}\tcon: {} {}\nint: {} {}\twis: {} {}\tcha: {} {}",
                                self.str, self.tempStr, self.dex, self.tempDex, self.con, self.tempCon,
                                self.int, self.tempInt, self.wis, self.tempWis, self.cha, self.tempCha)
            return string

        def __eq__(self, other):
            for attribute in self.attributes:
                if getattr(self, attribute) != getattr(other, attribute):
                    return False
            return True

    class Defense:
        def __init__(self, abilities, offense):
            self.ac = self.AC()
            self.hp = self.HP()
            self.damageReduction = ""
            self.spellResistance = ""
            self.fort = self.Save('con', abilities)
            self.reflex = self.Save('dex', abilities)
            self.will = self.Save('wis', abilities)
            self.resistances = ""
            self.immunities = ""
            self.cmd = self.CMD(offense)
            self.save_attributes = ['fort', 'reflex', 'will']
            self.attributes = ['ac', 'hp', 'damageReduction', 'spellResistance', 'fort',
                               'reflex', 'will', 'resistances', 'immunities', 'cmd']

        def create_from_json(self, json_data):
            self.ac.create_from_json(json_data.get("ac", ""))
            self.hp.create_from_json(json_data.get("hp", ""))
            self.damageReduction = json_data.get("damageReduction", "")
            self.spellResistance = json_data.get("spellResistance", "")
            self.fort.create_from_json(json_data.get("saves", '').get("fort", '') if json_data.get("saves", '') else '')
            self.reflex.create_from_json(json_data.get("saves").get("reflex") if json_data.get("saves", '') else '')
            self.will.create_from_json(json_data.get("saves").get("will") if json_data.get("saves", '') else '')
            self.resistances = json_data.get("resistances", "")
            self.immunities = json_data.get("immunities", "")
            self.cmd.create_from_json(json_data.get("cmd"))

        def update_defence(self, abilities, offense):
            self.ac.update_ac_data(abilities)
            self.fort.update_save_data(abilities)
            self.reflex.update_save_data(abilities)
            self.will.update_save_data(abilities)
            self.cmd.update_cmd_data(abilities, offense)

        def __eq__(self, other):
            for attribute in self.attributes:
                if getattr(self, attribute) != getattr(other, attribute):
                    return False
            return True

        class AC:
            def __init__(self):
                self.total = ""
                self.armorBonus = ""
                self.shieldBonus = ""
                self.sizeModifier = ""
                self.naturalArmor = ""
                self.deflectionModifier = ""
                self.miscModifier = ""
                self.touch = ""
                self.flatFooted = ""
                self.otherModifiers = ""
                self.items = self.Items()
                self.itemsTotals = self.ItemTotals()
                self.attributes = [
                    "total", "armorBonus", "shieldBonus", "sizeModifier",
                    "naturalArmor", "deflectionModifier", "miscModifier",
                    "touch", "flatFooted", "otherModifiers"
                ]

            def create_from_json(self, json_ac_data):
                if json_ac_data:
                    if json_ac_data:
                        for attribute in self.attributes:
                            if json_ac_data.get(attribute):
                                setattr(self, attribute, json_ac_data.get(attribute))
                        if json_ac_data.get("items"):
                            self.items.create_from_json(json_ac_data.get("items"))
                        self.itemsTotals.create_from_json(json_ac_data.get('itemTotals'))

            def update_ac_data(self, abilities):
                attributes = ["armorBonus", "shieldBonus", "sizeModifier",
                              "naturalArmor", "deflectionModifier", "miscModifier"]
                total_score = 10
                for attribute in attributes:
                    if str.isnumeric(getattr(self, attribute)):
                        total_score += int(getattr(self, attribute))
                abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get('dex')) \
                    if getattr(abilities, qtl.temp_ability_modifier.get('dex')) != '' \
                    else getattr(abilities, qtl.ability_modifier.get('dex'))
                total_score += str_to_int(abilityModifierData)
                self.total = str(total_score)

                total_bonus = 0
                total_check_penalty = 0
                total_spell_failure = 0
                total_weight = 0
                for item in self.items.list:
                    if item.bonus.isnumeric():
                        total_bonus += int(item.bonus)
                    if item.armorCheckPenalty.isnumeric():
                        total_check_penalty += int(item.armorCheckPenalty)
                    if item.spellFailure.isnumeric():
                        total_spell_failure += int(item.spellFailure)
                    if item.weight.isnumeric():
                        total_weight += int(item.weight)
                self.itemsTotals.bonus = str(total_bonus)
                self.itemsTotals.armorCheckPenalty = str(total_check_penalty)
                self.itemsTotals.spellFailure = str(total_spell_failure)
                self.itemsTotals.weight = str(total_weight)

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

            class ItemTotals:
                def __init__(self):
                    self.bonus = ''
                    self.armorCheckPenalty = ''
                    self.spellFailure = ''
                    self.weight = ''
                    self.attributes = ['bonus', 'armorCheckPenalty', 'spellFailure', 'weight']

                def create_from_json(self, json_data):
                    if json_data:
                        attributes = ['bonus', 'armorCheckPenalty', 'spellFailure', 'weight']
                        for attribute in attributes:
                            setattr(self, attribute, json_data.get(attribute, ""))

                def __eq__(self, other):
                    for attribute in self.attributes:
                        if getattr(self, attribute) != getattr(other, attribute):
                            return False
                    return True

            class Items:
                def __init__(self):
                    self.list = []

                def create_from_json(self, json_data):
                    if json_data:
                        for item_data in json_data:
                            item = self.Item()
                            item.create_from_json(item_data)
                            self.list.append(item)

                def add_item(self):
                    self.list.append(self.Item())

                def delete_items(self, delete_list):
                    for index in sorted(delete_list, reverse=True):
                        del self.list[index]

                def __eq__(self, other):
                    if self.list == other.list:
                        return True
                    return False

                class Item:
                    def __init__(self):
                        self.name = ""
                        self.bonus = ""
                        self.type = ""
                        self.armorCheckPenalty = ""
                        self.spellFailure = ""
                        self.weight = ""
                        self.properties = ""
                        self.attributes = ["name", "bonus", "type", "armorCheckPenalty",
                                           "spellFailure", "weight", "properties"]

                    def create_from_json(self, json_items_data):
                        if json_items_data:
                            for attribute in self.attributes:
                                if json_items_data.get(attribute):
                                    setattr(self, attribute, json_items_data.get(attribute))

                    def __eq__(self, other):
                        for attribute in self.attributes:
                            if getattr(self, attribute) != getattr(other, attribute):
                                return False
                        return True

        class Save:
            def __init__(self, modifier, abilities):
                self.total = ""
                self.base = ""
                self.magicModifier = ""
                self.miscModifier = ""
                self.tempModifier = ""
                self.otherModifiers = ""
                self.abilityModifier = modifier
                self.abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) \
                    if getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) != '' \
                    else getattr(abilities, qtl.ability_modifier.get(self.abilityModifier))
                self.attributes = [
                    "total", "base", "magicModifier", "miscModifier",
                    "tempModifier", "otherModifiers"
                ]

            def create_from_json(self, json_items_data):
                if json_items_data:
                    for attribute in self.attributes:
                        if json_items_data.get(attribute):
                            setattr(self, attribute, json_items_data.get(attribute))

            def update_save_data(self, abilities):
                attributes = ["base", "magicModifier", "miscModifier",
                              "tempModifier", "otherModifiers"]
                total_score = 0
                for attribute in attributes:
                    if str.isnumeric(getattr(self, attribute)):
                        total_score += int(getattr(self, attribute))
                self.abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) \
                    if getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) != '' \
                    else getattr(abilities, qtl.ability_modifier.get(self.abilityModifier))
                total_score += str_to_int(self.abilityModifierData)
                self.total = str(total_score)

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

        class CMD:
            def __init__(self, offense):
                self.total = ""
                self.sizeModifier = ""
                self.miscModifiers = ""
                self.tempModifiers = ""
                self.attributes = [
                    "total", "sizeModifier", "miscModifiers", "tempModifiers"
                ]

            def create_from_json(self, json_items_data):
                if json_items_data:
                    for attribute in self.attributes:
                        if json_items_data.get(attribute):
                            setattr(self, attribute, json_items_data.get(attribute))

            def update_cmd_data(self, abilities, offence):
                attributes = ["sizeModifier", "miscModifiers", "tempModifiers"]
                total_score = 0
                for attribute in attributes:
                    if str.isnumeric(getattr(self, attribute)):
                        total_score += int(getattr(self, attribute))
                abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get('str')) \
                    if getattr(abilities, qtl.temp_ability_modifier.get('str')) != '' \
                    else getattr(abilities, qtl.ability_modifier.get('str'))
                total_score += str_to_int(abilityModifierData)
                abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get('dex')) \
                    if getattr(abilities, qtl.temp_ability_modifier.get('dex')) != '' \
                    else getattr(abilities, qtl.ability_modifier.get('dex'))
                total_score += str_to_int(abilityModifierData)

                if str.isnumeric(offence.bab):
                    total_score += int(offence.bab)
                self.total = str(total_score + 10)

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

        class HP:
            def __init__(self):
                self.total = ""
                self.wounds = ""
                self.nonLethal = ""
                self.attributes = [
                    "total", "wounds", "nonLethal"
                ]

            def create_from_json(self, json_items_data):
                if json_items_data:
                    for attribute in self.attributes:
                        if json_items_data.get(attribute):
                            setattr(self, attribute, json_items_data.get(attribute))

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

    class Spells:
        def __init__(self):
            self.zeroLevel = self.NLevelSpells()
            self.firstLevel = self.NLevelSpells()
            self.secondLevel = self.NLevelSpells()
            self.thirdLevel = self.NLevelSpells()
            self.fourthLevel = self.NLevelSpells()
            self.fifthLevel = self.NLevelSpells()
            self.sixthLevel = self.NLevelSpells()
            self.seventhLevel = self.NLevelSpells()
            self.eighthLevel = self.NLevelSpells()
            self.ninthLevel = self.NLevelSpells()
            self.spellLikes = []
            self.spellsConditionalModifiers = ""
            self.spellsSpeciality = ""
            self.attributes = ['zeroLevel', 'firstLevel', 'secondLevel', 'thirdLevel', 'fourthLevel',
                               'fifthLevel', 'sixthLevel', 'seventhLevel', 'eighthLevel', 'ninthLevel']

        def create_from_json(self, json_data):
            spells_data = json_data.get('spells')
            if spells_data:
                attributes = ['zeroLevel', 'firstLevel', 'secondLevel', 'thirdLevel', 'fourthLevel',
                              'fifthLevel', 'sixthLevel', 'seventhLevel', 'eighthLevel', 'ninthLevel']
                for nLevel, attribute in zip(spells_data, attributes):
                    getattr(self, attribute).create_from_json(nLevel)
                spellLike_data = json_data.get('spellLikes')
                if spellLike_data:
                    for n_spellLike_data in spellLike_data:
                        spellLike = self.SpellLikes()
                        spellLike.create_from_json(n_spellLike_data)
                        self.spellLikes.append(spellLike)
                    self.spellsConditionalModifiers = json_data.get('spellsConditionalModifiers', '')
                    self.spellsSpeciality = json_data.get('spellsSpeciality', '')

        def add_spell_like(self):
            self.spellLikes.append(self.SpellLikes())

        def delete_spell_like(self, delete_list):
            for index in sorted(delete_list, reverse=True):
                del self.spellLikes[index]

        def __eq__(self, other):
            for attribute in self.attributes:
                if getattr(self, attribute) != getattr(other, attribute):
                    return False
            return True

        class SpellLikes:
            def __init__(self):
                self.prepared = 0
                self.cast = 0
                self.name = ""
                self.level = 0
                self.school = ""
                self.subschool = ""
                self.notes = ""
                self.atWill = False
                self.marked = False
                self.description = ''
                self.attributes = ['name', 'school', 'subschool', 'notes', 'marked',
                                   'prepared', 'cast', 'level', 'atWill', 'marked']

            def create_from_json(self, json_spellLike_data):
                if json_spellLike_data:
                    attributes_str = ['name', 'school', 'subschool', 'notes', 'marked']
                    attributes_int = ['prepared', 'cast', 'level']
                    attributes_bool = ['atWill', 'marked']
                    for attribute in attributes_str:
                        data = json_spellLike_data.get(attribute, '')
                        setattr(self, attribute, data)
                    for attribute in attributes_int:
                        data = json_spellLike_data.get(attribute, 0)
                        setattr(self, attribute, data)
                    for attribute in attributes_bool:
                        data = json_spellLike_data.get(attribute, False)
                        setattr(self, attribute, data)

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

        class NLevelSpells:
            def __init__(self):
                self.totalKnown = ""
                self.dc = ""
                self.totalPerDay = ""
                self.bonusSpells = ""
                self.slotted = []
                self.attributes = ['totalKnown', 'dc', 'totalPerDay', 'bonusSpells']

            def create_from_json(self, json_nLevel_data):
                if json_nLevel_data:
                    attributes = ['totalKnown', 'dc', 'totalPerDay', 'bonusSpells']
                    for attribute in attributes:
                        setattr(self, attribute, json_nLevel_data.get(attribute, ''))
                    json_slotted = json_nLevel_data.get('slotted')
                    if json_slotted:
                        for json_slotted_data in json_slotted:
                            spell = self.Spell()
                            spell.create_from_json(json_slotted_data)
                            self.slotted.append(spell)

            def add_spell(self):
                self.slotted.append(self.Spell())

            def delete_spells(self, delete_list):
                for index in sorted(delete_list, reverse=True):
                    del self.slotted[index]

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

            class Spell:
                def __init__(self):
                    self.level = 0
                    self.prepared = 0
                    self.cast = 0
                    self.name = ""
                    self.school = ""
                    self.subschool = ""
                    self.notes = ""
                    self.description = ""
                    self.marked = False
                    self.attributes = ['level', 'prepared', 'cast', 'name', 'school', 'subschool', 'notes', 'marked']

                def create_from_json(self, json_slotted_data):
                    attributes_str = ['name', 'school', 'subschool', 'notes']
                    attributes_int = ['level', 'prepared', 'cast']
                    if json_slotted_data:
                        for attribute in attributes_str:
                            data = json_slotted_data.get(attribute)
                            setattr(self, attribute, data)
                        for attribute in attributes_int:
                            data = json_slotted_data.get(attribute)
                            setattr(self, attribute, data)

                def __eq__(self, other):
                    for attribute in self.attributes:
                        if getattr(self, attribute) != getattr(other, attribute):
                            return False
                    return True

    class Skills:
        def __init__(self, abilities):
            self.acrobatics = self.SkillData('dex', abilities)
            self.appraise = self.SkillData('int', abilities)
            self.bluff = self.SkillData('cha', abilities)
            self.climb = self.SkillData('str', abilities)
            self.craft1 = self.SkillData('int', abilities)
            self.craft2 = self.SkillData('int', abilities)
            self.craft3 = self.SkillData('int', abilities)
            self.diplomacy = self.SkillData('cha', abilities)
            self.disableDevice = self.SkillData('dex', abilities)
            self.disguise = self.SkillData('cha', abilities)
            self.escapeArtist = self.SkillData('dex', abilities)
            self.fly = self.SkillData('dex', abilities)
            self.handleAnimal = self.SkillData('cha', abilities)
            self.heal = self.SkillData('wis', abilities)
            self.intimidate = self.SkillData('cha', abilities)
            self.knowledgeArcana = self.SkillData('int', abilities)
            self.knowledgeDungeoneering = self.SkillData('int', abilities)
            self.knowledgeEngineering = self.SkillData('int', abilities)
            self.knowledgeGeography = self.SkillData('int', abilities)
            self.knowledgeHistory = self.SkillData('int', abilities)
            self.knowledgeLocal = self.SkillData('int', abilities)
            self.knowledgeNature = self.SkillData('int', abilities)
            self.knowledgeNobility = self.SkillData('int', abilities)
            self.knowledgePlanes = self.SkillData('int', abilities)
            self.knowledgeReligion = self.SkillData('int', abilities)
            self.linguistics = self.SkillData('int', abilities)
            self.perception = self.SkillData('wis', abilities)
            self.perform1 = self.SkillData('cha', abilities)
            self.perform2 = self.SkillData('cha', abilities)
            self.profession1 = self.SkillData('wis', abilities)
            self.profession2 = self.SkillData('wis', abilities)
            self.ride = self.SkillData('dex', abilities)
            self.senseMotive = self.SkillData('wis', abilities)
            self.sleightOfHand = self.SkillData('dex', abilities)
            self.spellcraft = self.SkillData('int', abilities)
            self.stealth = self.SkillData('dex', abilities)
            self.survival = self.SkillData('wis', abilities)
            self.swim = self.SkillData('str', abilities)
            self.useMagicDevice = self.SkillData('cha', abilities)
            self.conditionalModifiers = ""
            self.languages = ""
            self.xp = self.XP()
            self.totalRanks = ""
            self.attributes = [
                "acrobatics", "appraise", "bluff", "climb", "craft1", "craft2", "craft3",
                "diplomacy", "disableDevice", "disguise", "escapeArtist", "fly", "handleAnimal", "heal",
                "intimidate", "knowledgeArcana", "knowledgeDungeoneering", "knowledgeEngineering",
                "knowledgeGeography", "knowledgeHistory", "knowledgeLocal", "knowledgeNature",
                "knowledgeNobility", "knowledgePlanes", "knowledgeReligion", "linguistics",
                "perception", "perform1", "perform2", "profession1", "profession2",
                "senseMotive", "sleightOfHand", "spellcraft", "stealth",
                "useMagicDevice", "survival", "swim", "ride"]

        def create_from_json(self, json_data):
            json_skills_data = json_data.get("skills")
            if json_skills_data:
                for attribute in self.attributes:
                    if json_skills_data.get(attribute):
                        skill = getattr(self, attribute)
                        skill.create_from_json(json_skills_data.get(attribute))
                        setattr(self, attribute, skill)
                self.conditionalModifiers = json_skills_data.get("conditionalModifiers", "")
                self.languages = json_data.get("languages", "")
                self.xp.create_from_json(json_data)
                self.count_ranks()

        def count_ranks(self):
            self.totalRanks = 0
            for attribute in self.attributes:
                skill = getattr(self, attribute)
                if str.isnumeric(skill.ranks):
                    self.totalRanks += int(skill.ranks)
            self.totalRanks = str(self.totalRanks)

        def update_skills(self, abilities):
            self.count_ranks()
            for attribute in self.attributes:
                skill = getattr(self, attribute)
                skill.update_skill_data(abilities)

        def __str__(self):
            string = "\tSkills:\n\n"
            for attribute in self.attributes:
                string = string + attribute + "\n" + str(getattr(self, attribute)) + "\n\n"
            string = string + "conditionalModifiers:\n" + self.conditionalModifiers + "\n"
            return string

        def __eq__(self, other):
            for attribute in self.attributes:
                if getattr(self, attribute) != getattr(other, attribute):
                    return False
            return True

        class XP:
            def __init__(self):
                self.total = ""
                self.toNextLevel = ""
                self.attributes = ['total', 'toNextLevel']

            def create_from_json(self, json_data):
                data = json_data.get("xp")
                if data:
                    self.total = data.get("total", "")
                    self.toNextLevel = data.get("toNextLevel", "")

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

        class SkillData:
            def __init__(self, modifier, abilities):
                self.classSkill = False
                self.ranks = ""
                self.misc = ""
                self.total = ""
                self.racial = ""
                self.trait = ""
                self.name = ""
                self.attributes = ['classSkill', 'ranks', 'misc', 'total', 'racial', 'trait', 'name']
                self.abilityModifier = modifier
                self.abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) \
                    if getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) != '' \
                    else getattr(abilities, qtl.ability_modifier.get(self.abilityModifier))

            def create_from_json(self, json_data):
                if json_data:
                    attributes = ["ranks", "misc", "total", "racial", "trait", "name"]
                    self.classSkill = json_data.get("classSkill", False)
                    for attribute in attributes:
                        setattr(self, attribute, json_data.get(attribute, ""))

            def update_skill_data(self, abilities):
                attributes = ["ranks", "misc", "racial", "trait"]
                total_score = 0
                for attribute in attributes:
                    if str.isnumeric(getattr(self, attribute)):
                        total_score += int(getattr(self, attribute))
                if self.classSkill and str.isnumeric(self.ranks) and int(self.ranks) > 0:
                    total_score += 3
                self.abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) \
                    if getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) != '' \
                    else getattr(abilities, qtl.ability_modifier.get(self.abilityModifier))
                total_score += str_to_int(self.abilityModifierData)
                self.total = str(total_score)

            def __str__(self):
                string = str.format("clssSkill: {}\nranks: {}\nmisc: {}\ntotal: {}\nracial: {}\ntrait: {}",
                                    self.classSkill, self.ranks, self.misc, self.total, self.racial, self.trait)
                return string

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

    class Offense:
        def __init__(self, abilities):
            self.initiative = self.Initiative()
            self.bab = ""
            self.conditionalOffenseModifiers = ""
            self.speed = self.Speed()
            self.cmb = self.CMB(abilities)
            self.melee = []
            self.ranged = []
            self.attributes = ['initiative', 'bab', 'conditionalOffenseModifiers', 'speed', 'cmb']

        def create_from_json(self, json_data):
            self.initiative.create_from_json(json_data)
            self.bab = json_data.get("bab", "")
            self.conditionalOffenseModifiers = json_data.get("conditionalOffenseModifiers", "")
            self.speed.create_from_json(json_data)
            self.cmb.create_from_json(json_data)
            self.melee = json_data.get("melee", [])
            self.ranged = json_data.get("ranged", [])

        def update_offense_data(self, abilities):
            self.cmb.update_cmb_data(abilities, self.bab)
            self.initiative.update_initiative_data(abilities)

        def __eq__(self, other):
            for attribute in self.attributes:
                if getattr(self, attribute) != getattr(other, attribute):
                    return False
            if self.melee != other.melee or self.ranged != other.ranged:
                return False
            return True

        class Initiative:
            def __init__(self):
                self.total = ""
                self.miscModifier = ""
                self.attributes = ['total', 'miscModifier']

            def create_from_json(self, json_data):
                data = json_data.get("initiative")
                if data:
                    self.total = data.get("total", "")
                    self.miscModifier = data.get("miscModifier", "")

            def update_initiative_data(self, abilities):
                attributes = ["miscModifier"]
                total_score = 0
                for attribute in attributes:
                    if str.isnumeric(getattr(self, attribute)):
                        total_score += int(getattr(self, attribute))
                abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get('dex')) \
                    if getattr(abilities, qtl.temp_ability_modifier.get('dex')) != '' \
                    else getattr(abilities, qtl.ability_modifier.get('dex'))
                total_score += str_to_int(abilityModifierData)
                self.total = str(total_score)

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

        class Speed:
            def __init__(self):
                self.base = ""
                self.withArmor = ""
                self.fly = ""
                self.swim = ""
                self.climb = ""
                self.burrow = ""
                self.tempModifiers = ""
                self.attributes = ['base', 'withArmor', 'fly', 'swim', 'climb', 'burrow', 'tempModifiers']

            def create_from_json(self, json_data):
                attributes = ["base", "withArmor", "fly", "swim", "climb", "burrow", "tempModifiers"]
                data = json_data.get("speed")
                if data:
                    for attribute in attributes:
                        setattr(self, attribute, data.get(attribute, ""))

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

        class CMB:
            def __init__(self, abilities):
                self.miscModifiers = ""
                self.sizeModifier = ""
                self.total = ""
                self.tempModifiers = ""
                self.attributes = ['miscModifiers', 'sizeModifier', 'total', 'tempModifiers']

            def create_from_json(self, json_data):
                attributes = ["miscModifiers", "sizeModifier", "total", "tempModifiers"]
                data = json_data.get("cmb")
                if data:
                    for attribute in attributes:
                        setattr(self, attribute, data.get(attribute, ""))

            def update_cmb_data(self, abilities, bab):
                attributes = ["miscModifiers", "sizeModifier", "tempModifiers"]
                total_score = 0
                if str.isnumeric(bab):
                    total_score += int(bab)
                for attribute in attributes:
                    if str.isnumeric(getattr(self, attribute)):
                        total_score += int(getattr(self, attribute))
                self.abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get('str')) \
                    if getattr(abilities, qtl.temp_ability_modifier.get('str')) != '' \
                    else getattr(abilities, qtl.ability_modifier.get('str'))
                total_score += str_to_int(self.abilityModifierData)
                self.total = str(total_score)

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

    class Money:
        def __init__(self):
            self.pp = ""
            self.gp = ""
            self.sp = ""
            self.cp = ""
            self.gems = ""
            self.other = ""
            self.attributes = ['pp', 'gp', 'sp', 'cp', 'gems', 'other']

        def create_from_json(self, json_data):
            attributes = ["pp", "gp", "sp", "cp", "gems", "other"]
            data = json_data.get("money")
            if data:
                for attribute in attributes:
                    setattr(self, attribute, data.get(attribute, ""))

        def __eq__(self, other):
            for attribute in self.attributes:
                if getattr(self, attribute) != getattr(other, attribute):
                    return False
            return True

    class Gears:
        def __init__(self):
            self.list = []

        def create_from_json(self, json_data):
            data = json_data.get('gear')
            if data:
                for item in data:
                    gear = self.Gear()
                    gear.create_from_json(item)
                    self.list.append(gear)

        def add_gear(self, type='', item='', location='', quantity='', weight='', notes=''):
            gear = self.Gear(type, item, location, quantity, weight, notes)
            self.list.append(gear)

        def delete_gear(self, delete_list):
            for index in sorted(delete_list, reverse=True):
                del self.list[index]

        def __eq__(self, other):
            if self.list == other.list:
                return True
            return False

        class Gear:
            def __init__(self, type='', item='', location='', quantity='', weight='', notes=''):
                self.type = type
                self.item = item
                self.location = location
                self.quantity = quantity
                self.weight = weight
                self.notes = notes
                self.attributes = ['type', 'item', 'location', 'quantity', 'weight', 'notes']

            def create_from_json(self, json_data):
                if json_data:
                    attributes = ["type", "location", "quantity", "weight", "notes"]
                    for attribute in attributes:
                        setattr(self, attribute, json_data.get(attribute, ""))
                    self.item = json_data.get('name', "")

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

    class Traits:
        def __init__(self):
            self.list = []

        def create_from_json(self, json_data):
            data = json_data.get('traits')
            if data:
                for item in data:
                    trait = self.Trait()
                    trait.create_from_json(item)
                    self.list.append(trait)

        def add_trait(self, type='', name='', notes=''):
            trait = self.Trait(type, name, notes)
            self.list.append(trait)

        def delete_traits(self, delete_list):
            for index in sorted(delete_list, reverse=True):
                del self.list[index]

        def __eq__(self, other):
            if self.list == other.list:
                return True
            return False

        class Trait:
            def __init__(self, type='', name='', notes=''):
                self.type = type
                self.name = name
                self.notes = notes
                self.attributes = ['type', 'name', 'notes']

            def create_from_json(self, json_data):
                attributes = ['type', 'name', 'notes']
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

    class SpecialAbilities:
        def __init__(self):
            self.list = []

        def create_from_json(self, json_data):
            data = json_data.get('specialAbilities')
            if data:
                for item in data:
                    specialAbility = self.SpecialAbility()
                    specialAbility.create_from_json(item)
                    self.list.append(specialAbility)

        def add_special_ability(self, type='', name='', notes=''):
            trait = self.SpecialAbility(type, name, notes)
            self.list.append(trait)

        def delete_special_ability(self, delete_list):
            for index in sorted(delete_list, reverse=True):
                del self.list[index]

        def __eq__(self, other):
            if self.list == other.list:
                return True
            return False

        class SpecialAbility:
            def __init__(self, type='', name='', notes=''):
                self.type = type
                self.name = name
                self.notes = notes
                self.attributes = ['type', 'name', 'notes']

            def create_from_json(self, json_data):
                attributes = ['type', 'name', 'notes']
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

    class Feats:
        def __init__(self):
            self.list = []

        def create_from_json(self, json_data):
            data = json_data.get('feats')
            if data:
                for item in data:
                    feat = self.Feat()
                    feat.create_from_json(item)
                    self.list.append(feat)

        def add_feat(self, type='', name='', notes=''):
            trait = self.Feat(type, name, notes)
            self.list.append(trait)

        def delete_feat(self, delete_list):
            for index in sorted(delete_list, reverse=True):
                del self.list[index]

        def __eq__(self, other):
            if self.list == other.list:
                return True
            return False

        class Feat:
            def __init__(self, type='', name='', notes=''):
                self.type = type
                self.name = name
                self.notes = notes
                self.attributes = ['type', 'name', 'notes']

            def create_from_json(self, json_data):
                attributes = ['type', 'name', 'notes']
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True

    class Attacks:
        def __init__(self):
            self.melee = []
            self.ranged = []

        def create_from_json(self, json_data):
            meleeAttackData = json_data.get('melee')
            if meleeAttackData:
                for attack in meleeAttackData:
                    meleeAttack = self.MeleeAttack()
                    meleeAttack.create_from_json(attack)
                    self.melee.append(meleeAttack)
            rangedAttackData = json_data.get('ranged')
            if rangedAttackData:
                for attack in rangedAttackData:
                    rangedAttack = self.RangedAttack()
                    rangedAttack.create_from_json(attack)
                    self.ranged.append(rangedAttack)

        def add_melee_attack(self, weapon='', attackBonus='', damage='', critical='', type='', notes=''):
            self.melee.append(self.MeleeAttack(weapon, attackBonus, damage, critical, type, notes))

        def add_ranged_attack(self, weapon='', attackBonus='', damage='', critical='', type='', ammunition=''):
            self.ranged.append(self.MeleeAttack(weapon, attackBonus, damage, critical, type, ammunition))

        def delete_melee_attacks(self, delete_list):
            for index in sorted(delete_list, reverse=True):
                del self.melee[index]

        def delete_ranged_attacks(self, delete_list):
            for index in sorted(delete_list, reverse=True):
                del self.ranged[index]

        def __eq__(self, other):
            if self.melee == other.melee and self.ranged == self.ranged:
                return True
            return False

        class MeleeAttack:
            def __init__(self, weapon='', attackBonus='', damage='', critical='', type='', notes=''):
                self.weapon = weapon
                self.attackBonus = attackBonus
                self.damage = damage
                self.critical = critical
                self.type = type
                self.notes = notes
                self.attributes = ['weapon', 'attackBonus', 'damage', 'critical', 'type', 'notes']

            def create_from_json(self, json_data):
                attributes = ['weapon', 'attackBonus', 'damage', 'critical', 'type', 'notes']
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True


        class RangedAttack:
            def __init__(self, weapon='', attackBonus='', damage='', critical='', type='', ammunition=''):
                self.weapon = weapon
                self.attackBonus = attackBonus
                self.damage = damage
                self.critical = critical
                self.type = type
                self.ammunition = ammunition
                self.attributes = ['weapon', 'attackBonus', 'damage', 'critical', 'type', 'ammunition']

            def create_from_json(self, json_data):
                attributes = ['weapon', 'attackBonus', 'damage', 'critical', 'type', 'ammunition']
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))

            def __eq__(self, other):
                for attribute in self.attributes:
                    if getattr(self, attribute) != getattr(other, attribute):
                        return False
                return True
