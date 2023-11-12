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
        self.notes = ""

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
        self.notes = json_data.get("notes")

    def update_data(self):
        self.abilities.count_score()
        self.abilities.update_modifiers()
        self.skills.update_skills(self.abilities)
        self.defense.update_defence(self.abilities, self.offense)
        self.offense.update_offense_data(self.abilities)

    def __str__(self):
        string = str.format("{}\n{}\n{}", self.general, self.abilities, self.skills)
        return string

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
                    setattr(self, attribute, json_data.get(attribute))

        def __str__(self):
            string = str.format("\tGeneral\n\nCharacter Name: {}\tAlignment: {}\tPlayer Name:\n"
                                "Character Class & Level: {}\tDeity: {}\tHomeland: {}\n"
                                "Race: {}\tSize: {}\tGender: {}\tAge: {}\tHeight: {}\tWeight: {}\tHair: {}\tEyes: {}",
                                self.name, self.alignment,
                                self.level, self.deity, self.homeland,
                                self.race, self.size, self.gender, self.age, self.height, self.weight, self.hair,
                                self.eyes)
            return string

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

        def create_from_json(self, json_data):
            self.ac.create_from_json(json_data.get("ac", ""))
            self.hp.create_from_json(json_data.get("hp", ""))
            self.damageReduction = json_data.get("damageReduction", "")
            self.spellResistance = json_data.get("spellResistance", "")
            self.fort.create_from_json(json_data.get("saves").get("fort"))
            self.reflex.create_from_json(json_data.get("saves").get("reflex"))
            self.will.create_from_json(json_data.get("saves").get("will"))
            self.resistances = json_data.get("resistances", "")
            self.immunities = json_data.get("immunities", "")
            self.cmd.create_from_json(json_data.get("cmd"))

        def update_defence(self, abilities, offense):
            self.ac.update_ac_data(abilities)
            self.fort.update_save_data(abilities)
            self.reflex.update_save_data(abilities)
            self.will.update_save_data(abilities)
            self.cmd.update_cmd_data(abilities, offense)

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
                self.items = []
                self.attributes = [
                    "total", "armorBonus", "shieldBonus", "sizeModifier",
                    "naturalArmor", "deflectionModifier", "miscModifier",
                    "touch", "flatFooted", "otherModifiers"
                ]

            def create_from_json(self, json_ac_data):
                for attribute in self.attributes:
                    if json_ac_data.get(attribute):
                        setattr(self, attribute, json_ac_data.get(attribute))
                if json_ac_data.get("items"):
                    for item in json_ac_data.get("items"):
                        item_input = self.Item()
                        self.items.append(self.Item.create_from_json(item_input, item))

            def update_ac_data(self, abilities):
                attributes = ["armorBonus", "shieldBonus", "sizeModifier",
                              "naturalArmor", "deflectionModifier", "miscModifier"]
                total_score = 0
                for attribute in attributes:
                    if str.isnumeric(getattr(self, attribute)):
                        total_score += int(getattr(self, attribute))
                abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get('dex')) \
                    if getattr(abilities, qtl.temp_ability_modifier.get('dex')) != '' \
                    else getattr(abilities, qtl.ability_modifier.get('dex'))
                total_score += str_to_int(abilityModifierData)
                self.total = str(total_score)

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
                    for attribute in self.attributes:
                        if json_items_data.get(attribute):
                            setattr(self, attribute, json_items_data.get(attribute))

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

        class CMD:
            def __init__(self, offense):
                self.total = ""
                self.sizeModifier = ""
                self.miscModifier = ""
                self.tempModifier = ""
                self.attributes = [
                    "total", "sizeModifier", "miscModifier", "tempModifier"
                ]

            def create_from_json(self, json_items_data):
                for attribute in self.attributes:
                    if json_items_data.get(attribute):
                        setattr(self, attribute, json_items_data.get(attribute))

            def update_cmd_data(self, abilities, offence):
                attributes = ["sizeModifier", "miscModifier", "tempModifier"]
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

        class HP:
            def __init__(self):
                self.total = ""
                self.wounds = ""
                self.nonLethal = ""
                self.attributes = [
                    "total", "wounds", "nonLethal"
                ]

            def create_from_json(self, json_items_data):
                for attribute in self.attributes:
                    if json_items_data.get(attribute):
                        setattr(self, attribute, json_items_data.get(attribute))

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

        def create_from_json(self, json_data):
            spells_data = json_data.get('spells')
            attributes = ['zeroLevel', 'firstLevel', 'secondLevel', 'thirdLevel', 'fourthLevel',
                          'fifthLevel', 'sixthLevel', 'seventhLevel', 'eighthLevel', 'ninthLevel']
            for nLevel, attribute in zip(spells_data, attributes):
                getattr(self, attribute).create_from_json(nLevel)
            spellLike_data = json_data.get('spellLikes')
            for n_spellLike_data in spellLike_data:
                spellLike = self.SpellLikes()
                self.spellLikes.append(spellLike.create_from_json(n_spellLike_data))
            self.spellsConditionalModifiers = json_data.get('spellsConditionalModifiers', '')
            self.spellsSpeciality = json_data.get('spellsSpeciality', '')

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

            def create_from_json(self, json_spellLike_data):
                attributes = ['prepared', 'cast', 'name', 'level', 'school', 'subschool', 'notes', 'atWill', 'marked']
                for attribute in attributes:
                    setattr(self, attribute, json_spellLike_data.get(attribute))

        class NLevelSpells:
            def __init__(self):
                self.totalKnown = ""
                self.dc = ""
                self.totalPerDay = ""
                self.bonusSpells = ""
                self.slotted = []

            def create_from_json(self, json_nLevel_data):
                attributes = ['totalKnown', 'dc', 'totalPerDay', 'bonusSpells']
                for attribute in attributes:
                    setattr(self, attribute, json_nLevel_data.get(attribute, ''))
                json_slotted = json_nLevel_data.get('slotted')
                for json_slotted_data in json_slotted:
                    spell = self.Spell()
                    self.slotted.append(spell.create_from_json(json_slotted_data))

            class Spell:
                def __init__(self):
                    self.level = 0
                    self.prepared = 0
                    self.cast = 0
                    self.name = ""
                    self.school = ""
                    self.subschool = ""
                    self.notes = ""

                def create_from_json(self, json_slotted_data):
                    attributes = ['level', 'prepared', 'cast', 'name', 'school', 'subschool', 'notes']
                    for attribute in attributes:
                        setattr(self, attribute, json_slotted_data.get(attribute))

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

        class XP:
            def __init__(self):
                self.total = ""
                self.toNextLevel = ""

            def create_from_json(self, json_data):
                data = json_data.get("xp", None)
                if data is not None:
                    self.total = data.get("total", "")
                    self.toNextLevel = data.get("toNextLevel", "")

        class SkillData:
            def __init__(self, modifier, abilities):
                self.classSkill = False
                self.ranks = ""
                self.misc = ""
                self.total = ""
                self.racial = ""
                self.trait = ""
                self.name = ""
                self.abilityModifier = modifier
                self.abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) \
                    if getattr(abilities, qtl.temp_ability_modifier.get(self.abilityModifier)) != '' \
                    else getattr(abilities, qtl.ability_modifier.get(self.abilityModifier))

            def create_from_json(self, json_data):
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
                if self.classSkill:
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

    class Offense:
        def __init__(self, abilities):
            self.initiative = self.Initiative()
            self.bab = ""
            self.conditionalOffenseModifiers = ""
            self.speed = self.Speed()
            self.cmb = self.CMB(abilities)
            self.melee = []
            self.ranged = []

        def create_from_json(self, json_data):
            self.initiative.create_from_json(json_data)
            self.bab = json_data.get("bab", "")
            self.conditionalOffenseModifiers = json_data.get("conditionalOffenseModifiers", "")
            self.speed.create_from_json(json_data)
            self.cmb.create_from_json(json_data)
            self.melee = json_data.get("melee", [])
            self.ranged = json_data.get("ranged", [])

        def update_offense_data(self, abilities):
            self.cmb.update_cmb_data(abilities)
            self.initiative.update_initiative_data(abilities)

        class Initiative:
            def __init__(self):
                self.total = ""
                self.miscModifier = ""

            def create_from_json(self, json_data):
                data = json_data.get("initiative", None)
                if data is not None:
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

        class Speed:
            def __init__(self):
                self.base = ""
                self.withArmor = ""
                self.fly = ""
                self.swim = ""
                self.climb = ""
                self.burrow = ""
                self.tempModifiers = ""

            def create_from_json(self, json_data):
                attributes = ["base", "withArmor", "fly", "swim", "climb", "burrow", "tempModifiers"]
                data = json_data.get("speed", None)
                if data is not None:
                    for attribute in attributes:
                        setattr(self, attribute, data.get(attribute, ""))

        class CMB:
            def __init__(self, abilities):
                self.miscModifiers = ""
                self.sizeModifier = ""
                self.total = ""
                self.tempModifiers = ""

            def create_from_json(self, json_data):
                attributes = ["miscModifiers", "sizeModifier", "total", "tempModifiers"]
                data = json_data.get("cmb", None)
                if data is not None:
                    for attribute in attributes:
                        setattr(self, attribute, data.get(attribute, ""))

            def update_cmb_data(self, abilities):
                attributes = ["miscModifiers", "sizeModifier", "tempModifiers"]
                total_score = 0
                for attribute in attributes:
                    if str.isnumeric(getattr(self, attribute)):
                        total_score += int(getattr(self, attribute))
                self.abilityModifierData = getattr(abilities, qtl.temp_ability_modifier.get('str')) \
                    if getattr(abilities, qtl.temp_ability_modifier.get('str')) != '' \
                    else getattr(abilities, qtl.ability_modifier.get('str'))
                total_score += str_to_int(self.abilityModifierData)
                self.total = str(total_score)
    class Money:
        def __init__(self):
            self.pp = ""
            self.gp = ""
            self.sp = ""
            self.cp = ""
            self.gems = ""
            self.other = ""

        def create_from_json(self, json_data):
            attributes = ["pp", "gp", "sp", "cp", "gems", "other"]
            data = json_data.get("money", None)
            if data is not None:
                for attribute in attributes:
                    setattr(self, attribute, data.get(attribute, ""))

    class Gears:
        def __init__(self):
            self.gears = []

        def create_from_json(self, json_data):
            data = json_data.get('gear')
            for item in data:
                gear = self.Gear()
                gear.create_from_json(item)
                self.gears.append(gear)

        def add_gear(self, type, name, location, quantity, weight, notes):
            gear = self.Gear(type, name, location, quantity, weight, notes)
            self.gears.append(gear)

        def delete_gear(self, delete_list):
            for index in delete_list:
                del self.gears[index]

        class Gear:
            def __init__(self, type='', name='', location='', quantity='', weight='', notes=''):
                self.type = type
                self.name = name
                self.location = location
                self.quantity = quantity
                self.weight = weight
                self.notes = notes

            def create_from_json(self, json_data):
                attributes = ["type", "name", "location", "quantity", "weight", "notes"]
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))

    class Traits:
        def __init__(self):
            self.traits = []

        def create_from_json(self, json_data):
            data = json_data.get('traits')
            for item in data:
                trait = self.Trait()
                trait.create_from_json(item)
                self.traits.append(trait)

        def add_trait(self, type, name, notes):
            trait = self.Trait(type, name, notes)
            self.traits.append(trait)

        def delete_traits(self, delete_list):
            for index in delete_list:
                del self.traits[index]

        class Trait:
            def __init__(self, type='', name='', notes=''):
                self.type = type
                self.name = name
                self.notes = notes

            def create_from_json(self, json_data):
                attributes = ['type', 'name', 'notes']
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))

    class SpecialAbilities:
        def __init__(self):
            self.specialAbilities = []

        def create_from_json(self, json_data):
            data = json_data.get('specialAbilities')
            for item in data:
                specialAbility = self.SpecialAbility()
                specialAbility.create_from_json(item)
                self.specialAbilities.append(specialAbility)

        def add_trait(self, type, name, notes):
            trait = self.SpecialAbility(type, name, notes)
            self.specialAbilities.append(trait)

        def delete_traits(self, delete_list):
            for index in delete_list:
                del self.specialAbilities[index]

        class SpecialAbility:
            def __init__(self, type='', name='', notes=''):
                self.type = type
                self.name = name
                self.notes = notes

            def create_from_json(self, json_data):
                attributes = ['type', 'name', 'notes']
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))

    class Feats:
        def __init__(self):
            self.feats = []

        def create_from_json(self, json_data):
            data = json_data.get('feats')
            for item in data:
                feat = self.Feat()
                feat.create_from_json(item)
                self.feats.append(feat)

        def add_trait(self, type, name, notes):
            trait = self.Feat(type, name, notes)
            self.feats.append(trait)

        def delete_traits(self, delete_list):
            for index in delete_list:
                del self.feats[index]

        class Feat:
            def __init__(self, type='', name='', notes=''):
                self.type = type
                self.name = name
                self.notes = notes

            def create_from_json(self, json_data):
                attributes = ['type', 'name', 'notes']
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))
