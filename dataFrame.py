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
        self.spells = []

        self.skills = self.Skills()

    def create_from_json(self, json_data):
        self.general.create_from_json(json_data)
        self.abilities.create_from_json(json_data)
        self.skills.create_from_json(json_data)

    def __str__(self):
        string = str.format("{}\n{}\n{}", self.general, self.abilities, self.skills)
        return string

    class General:
        def __init__(self):
            self.name = ""   # Character Name
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

        def create_from_json(self, json_data):
            attributes = ["str", "int", "wis", "dex", "con", "cha",
                          "tempStr", "tempInt", "tempWis", "tempDex", "tempCon", "tempCha"]
            json_ability_data = json_data.get("abilities")
            for attribute in attributes:
                if json_ability_data.get(attribute):
                    setattr(self, attribute, json_ability_data.get(attribute))
                    modifier = str(attribute) + "Modifier"
                    setattr(self, modifier, self.get_ability_modifier(json_ability_data.get(attribute)))

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
        def __init__(self):
            self.ac = self.AC()

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

            # class Item:
            #     def __init__(self):

    class Spell:
        def __init__(self):
            self.level = 0
            self.prepared = 0
            self.cast = 0
            self.name = ""
            self.school = ""
            self.subschool = ""
            self.notes = ""

    class Skills:
        def __init__(self):
            self.acrobatics = self.SkillData()
            self.appraise = self.SkillData()
            self.bluff = self.SkillData()
            self.climb = self.SkillData()
            self.craft1 = self.SkillData()
            self.craft2 = self.SkillData()
            self.craft3 = self.SkillData()
            self.diplomacy = self.SkillData()
            self.disableDevice = self.SkillData()
            self.disguise = self.SkillData()
            self.escapeArtist = self.SkillData()
            self.fly = self.SkillData()
            self.heal = self.SkillData()
            self.intimidate = self.SkillData()
            self.knowledgeArcana = self.SkillData()
            self.knowledgeDungeoneering = self.SkillData()
            self.knowledgeEngineering = self.SkillData()
            self.knowledgeGeography = self.SkillData()
            self.knowledgeHistory = self.SkillData()
            self.knowledgeLocal = self.SkillData()
            self.knowledgeNature = self.SkillData()
            self.knowledgeNobility = self.SkillData()
            self.knowledgePlanes = self.SkillData()
            self.knowledgeReligion = self.SkillData()
            self.linguistics = self.SkillData()
            self.perception = self.SkillData()
            self.perform1 = self.SkillData()
            self.perform2 = self.SkillData()
            self.profession1 = self.SkillData()
            self.profession2 = self.SkillData()
            self.senseMotive = self.SkillData()
            self.sleightOfHand = self.SkillData()
            self.spellcraft = self.SkillData()
            self.stealth = self.SkillData()
            self.useMagicDevice = self.SkillData()
            self.survival = self.SkillData()
            self.swim = self.SkillData()
            self.ride = self.SkillData()
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
                    skill = self.SkillData()
                    skill.create_from_json(json_skills_data.get(attribute))
                    setattr(self, attribute, skill)
            self.conditionalModifiers = json_skills_data.get("conditionalModifiers")

        def __str__(self):
            string = "\tSkills:\n\n"
            for attribute in self.attributes:
                string = string + attribute + "\n" + str(getattr(self, attribute)) + "\n\n"
            string = string + "conditionalModifiers:\n" + self.conditionalModifiers + "\n"
            return string

        class SkillData:
            def __init__(self):
                self.classSkill = False
                self.ranks = ""
                self.misc = ""
                self.total = ""
                self.racial = ""
                self.trait = ""
                self.name = ""

            def create_from_json(self, json_data):
                attributes = ["classSkill", "ranks", "misc", "total", "racial", "trait", "name"]
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, False))

            def __str__(self):
                string = str.format("clssSkill: {}\nranks: {}\nmisc: {}\ntotal: {}\nracial: {}\ntrait: {}",
                                    self.classSkill, self.ranks, self.misc, self.total, self.racial, self.trait)
                return string

