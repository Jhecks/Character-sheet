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
        self.name = ""
        self.modified = ""
        self.alignment = ""
        self.spells = []
        self.abilities = Abilities()
        self.skills = Skills()

        self.height = ""
        self.weight = ""
        self.hair = ""
        self.eyes = ""


class Abilities:
    def __init__(self):
        self.str = 0
        self.int = 0
        self.wis = 0
        self.dex = 0
        self.con = 0
        self.cha = 0

        self.tempStr = 0
        self.tempInt = 0
        self.tempWis = 0
        self.tempDex = 0
        self.tempCon = 0
        self.tempCha = 0

    def create_from_json(self, json_data):
        attributes = ["str", "int", "wis", "dex", "con", "cha",
                      "tempStr", "tempInt", "tempWis", "tempDex", "tempCon", "tempCha"]
        json_ability_data = json_data.get("abilities")
        for attribute in attributes:
            if json_ability_data.get(attribute):
                setattr(self, attribute, json_ability_data.get(attribute))

    def __str__(self):
        string = str.format("\tAbilities\n\nstr: {} {}\tdex: {} {}\tcon: {} {}\nint: {} {}\twis: {} {}\tcha: {} {}",
                            self.str, self.tempStr, self.dex, self.tempDex, self.con, self.tempCon,
                            self.int, self.tempInt, self.wis, self.tempWis, self.cha, self.tempCha)
        return string


class Spell:
    def __init__(self):
        self.level = 0
        self.prepared = 0
        self.cast = 0
        self.name = ""
        self.school = ""
        self.subschool = ""
        self.notes = ""


class SkillData:
    def __init__(self):
        self.classSkill = False
        self.ranks = ""
        self.misc = ""
        self.total = ""
        self.racial = ""
        self.trait = ""

    def create_from_json(self, json_data):
        attributes = ["classSkill", "ranks", "misc", "total", "racial", "trait"]
        for attribute in attributes:
            setattr(self, attribute, json_data.get(attribute, False))

    def __str__(self):
        string = str.format("clssSkill: {}\nranks: {}\nmisc: {}\ntotal: {}\nracial: {}\ntrait: {}",
                            self.classSkill, self.ranks, self.misc, self.total, self.racial, self.trait)
        return string


class Skills:
    def __init__(self):
        self.acrobatics = {}
        self.appraise = {}
        self.bluff = {}
        self.climb = {}
        self.craft1 = {}
        self.craft2 = {}
        self.craft3 = {}
        self.diplomacy = {}
        self.disableDevice = {}
        self.disguise = {}
        self.escapeArtist = {}
        self.fly = {}
        self.heal = {}
        self.intimidate = {}
        self.knowledgeArcana = {}
        self.knowledgeDungeoneering = {}
        self.knowledgeEngineering = {}
        self.knowledgeGeography = {}
        self.knowledgeHistory = {}
        self.knowledgeLocal = {}
        self.knowledgeNature = {}
        self.knowledgeNobility = {}
        self.knowledgePlanes = {}
        self.knowledgeReligion = {}
        self.linguistics = {}
        self.perception = {}
        self.perform1 = {}
        self.perform2 = {}
        self.profession1 = {}
        self.profession2 = {}
        self.senseMotive = {}
        self.sleightOfHand = {}
        self.spellcraft = {}
        self.stealth = {}
        self.useMagicDevice = {}
        self.survival = {}
        self.swim = {}
        self.ride = {}
        self.attributes = []
        self.conditionalModifiers = ""

    def create_from_json(self, json_data):
        self.attributes = [
            "acrobatics", "appraise", "bluff", "climb", "craft1", "craft2", "craft3",
            "diplomacy", "disableDevice", "disguise", "escapeArtist", "fly", "heal",
            "intimidate", "knowledgeArcana", "knowledgeDungeoneering", "knowledgeEngineering",
            "knowledgeGeography", "knowledgeHistory", "knowledgeLocal", "knowledgeNature",
            "knowledgeNobility", "knowledgePlanes", "knowledgeReligion", "linguistics",
            "perception", "perform1", "perform2", "profession1", "profession2",
            "senseMotive", "sleightOfHand", "spellcraft", "stealth",
            "useMagicDevice", "survival", "swim", "ride"]

        json_skills_data = json_data.get("skills")
        for attribute in self.attributes:
            if json_skills_data.get(attribute):
                skill = SkillData()
                skill.create_from_json(json_skills_data.get(attribute))
                setattr(self, attribute, skill)
        self.conditionalModifiers = json_skills_data.get("conditionalModifiers")

    def __str__(self):
        string = "\tSkills:\n\n"
        for attribute in self.attributes:
            string = string + attribute + "\n" + str(getattr(self, attribute)) + "\n\n"
        string = string + "conditionalModifiers:\n" + self.conditionalModifiers + "\n"
        return string
