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

        self.defense = self.Defense()
        self.offense = self.Offense()
        self.skills = self.Skills()

    def create_from_json(self, json_data):
        self.general.create_from_json(json_data)
        self.abilities.create_from_json(json_data)
        self.defense.create_from_json(json_data)
        self.offense.create_from_json(json_data)
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

        def create_from_json(self, json_data):
            attributes = ["str", "int", "wis", "dex", "con", "cha",
                          "tempStr", "tempInt", "tempWis", "tempDex", "tempCon", "tempCha"]
            json_ability_data = json_data.get("abilities")
            for attribute in attributes:
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
            self.hp = self.HP()
            self.damageReduction = ""
            self.spellResistance = ""
            self.fort = self.Save()
            self.reflex = self.Save()
            self.will = self.Save()
            self.resistances = ""
            self.immunities = ""
            self.cmd = self.CMD()

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
            def __init__(self):
                self.total = ""
                self.base = ""
                self.magicModifier = ""
                self.miscModifier = ""
                self.tempModifier = ""
                self.otherModifiers = ""
                self.attributes = [
                    "total", "base", "magicModifier", "miscModifier",
                    "tempModifier", "otherModifiers"
                ]

            def create_from_json(self, json_items_data):
                for attribute in self.attributes:
                    if json_items_data.get(attribute):
                        setattr(self, attribute, json_items_data.get(attribute))

        class CMD:
            def __init__(self):
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
            self.handleAnimal = self.SkillData()
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
            self.languages = ""
            self.xp = self.XP()
            self.totalRanks = ""

        def create_from_json(self, json_data):
            self.attributes = [
                "acrobatics", "appraise", "bluff", "climb", "craft1", "craft2", "craft3",
                "diplomacy", "disableDevice", "disguise", "escapeArtist", "fly", "handleAnimal", "heal",
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
            self.conditionalModifiers = json_skills_data.get("conditionalModifiers", "")
            self.languages = json_data.get("languages", "")
            self.xp.create_from_json(json_data)

            self.totalRanks = 0
            for attribute in self.attributes:
                skill = getattr(self, attribute)
                if str.isnumeric(skill.ranks):
                    self.totalRanks += int(skill.ranks)
            self.totalRanks = str(self.totalRanks)

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
            def __init__(self):
                self.classSkill = False
                self.ranks = ""
                self.misc = ""
                self.total = ""
                self.racial = ""
                self.trait = ""
                self.name = ""

            def create_from_json(self, json_data):
                attributes = ["ranks", "misc", "total", "racial", "trait", "name"]
                self.classSkill = json_data.get("classSkill", False)
                for attribute in attributes:
                    setattr(self, attribute, json_data.get(attribute, ""))

            def __str__(self):
                string = str.format("clssSkill: {}\nranks: {}\nmisc: {}\ntotal: {}\nracial: {}\ntrait: {}",
                                    self.classSkill, self.ranks, self.misc, self.total, self.racial, self.trait)
                return string

    class Offense:
        def __init__(self):
            self.initiative = self.Initiative()
            self.bab = ""
            self.conditionalOffenseModifiers = ""
            self.speed = self.Speed()
            self.cmb = self.CMB()
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

        class Initiative:
            def __init__(self):
                self.total = ""
                self.miscModifier = ""

            def create_from_json(self, json_data):
                data = json_data.get("initiative", None)
                if data is not None:
                    self.total = data.get("total", "")
                    self.miscModifier = data.get("miscModifier", "")

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
            def __init__(self):
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
