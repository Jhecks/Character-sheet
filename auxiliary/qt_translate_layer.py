general_attributes = [
    'name', 'alignment', 'playerName', 'level', 'deity', 'homeland', 'race',
    'size', 'gender', 'age', 'height', 'weight', 'hair', 'eyes'
]

ability_editable_attributes = [
    'str',
    'tempStr',
    'int',
    'tempInt',
    'dex',
    'tempDex',
    'wis',
    'tempWis',
    'con',
    'tempCon',
    'cha',
    'tempCha'
]

defence_ac_editable_attributes = [
    'ac_armorBonus',
    'ac_shieldBonus',
    'ac_sizeModifier',
    'ac_naturalArmor',
    'ac_DeflectionModifier',
    'ac_miscModifier',
    'ac_touch',
    'ac_flatFooted',
    'ac_otherModifiers'
]

defence_hp_editable_attributes = [
    'hp_total',
    'hp_wounds',
    'hp_nonLethal',
]

defence_fort_editable_attributes = [
    'fort_base',
    'fort_magicModifier',
    'fort_miscModifier',
    'fort_tempModifier',
    'fort_otherModifiers',
]

defence_reflex_editable_attributes = [
    'reflex_base',
    'reflex_magicModifier',
    'reflex_miscModifier',
    'reflex_tempModifier',
    'reflex_otherModifiers',
]

defence_will_editable_attributes = [
    'will_base',
    'will_magicModifier',
    'will_miscModifier',
    'will_tempModifier',
    'will_otherModifiers',
]

defence_cmd_editable_attributes = [
    'cmd_sizeModifier',
    'cmd_miscModifiers',
    'cmd_tempModifiers'
]

defence_editable_attributes = [
    'resistances',
    'immunities',
    'damageReduction',
    'spellResistance',
]

skills_editable_attributes = [
    'acrobatics',
    'appraise', 'bluff', 'climb', 'craft1', 'craft2', 'craft3', 'diplomacy', 'disableDevice', 'disguise',
    'escapeArtist', 'fly', 'handleAnimal', 'heal', 'intimidate', 'knowledgeArcana', 'knowledgeDungeoneering',
    'knowledgeEngineering', 'knowledgeGeography', 'knowledgeHistory', 'knowledgeLocal', 'knowledgeNature',
    'knowledgeNobility', 'knowledgePlanes', 'knowledgeReligion', 'linguistics', 'perception', 'perform1', 'perform2',
    'profession1', 'profession2', 'senseMotive', 'sleightOfHand', 'spellcraft', 'stealth', 'useMagicDevice', 'survival',
    'swim', 'ride']

ability_attributes = [
    'str',
    'strModifier',
    'tempStr',
    'tempStrModifier',
    # 'int',
    'intModifier',
    'tempInt',
    'tempIntModifier',
    'dex',
    'dexModifier',
    'tempDex',
    'tempDexModifier',
    'wis',
    'wisModifier',
    'tempWis',
    'tempWisModifier',
    'con',
    'conModifier',
    'tempCon',
    'tempConModifier',
    'cha',
    'chaModifier',
    'tempCha',
    'tempChaModifier'
]

offence_attributes = [
    'initiative_miscModifier',
    'bab',
    'conditionalOffenseModifiers',
    'speed_base',
    'speed_withArmor',
    'speed_fly',
    'speed_swim',
    'speed_climb',
    'speed_burrow',
    'speed_tempModifiers',
    'cmb_sizeModifier',
    'cmb_miscModifiers',
    'cmb_tempModifiers'
]

skill_attributes = {
    'acrobatics': 'dex',
    'appraise': 'int',
    'bluff': 'cha',
    'climb': 'str',
    'craft1': 'int',
    'craft2': 'int',
    'craft3': 'int',
    'diplomacy': 'cha',
    'disableDevice': 'dex',
    'disguise': 'cha',
    'escapeArtist': 'dex',
    'fly': 'dex',
    'handleAnimal': 'cha',
    'heal': 'wis',
    'intimidate': 'cha',
    'knowledgeArcana': 'int',
    'knowledgeDungeoneering': 'int',
    'knowledgeEngineering': 'int',
    'knowledgeGeography': 'int',
    'knowledgeHistory': 'int',
    'knowledgeLocal': 'int',
    'knowledgeNature': 'int',
    'knowledgeNobility': 'int',
    'knowledgePlanes': 'int',
    'knowledgeReligion': 'int',
    'linguistics': 'int',
    'perception': 'wis',
    'perform1': 'cha',
    'perform2': 'cha',
    'profession1': 'wis',
    'profession2': 'wis',
    'ride': 'dex',
    'senseMotive': 'wis',
    'sleightOfHand': 'dex',
    'spellcraft': 'int',
    'stealth': 'dex',
    'survival': 'wis',
    'swim': 'str',
    'useMagicDevice': 'cha'
}

skill_craft_perform_prof_attributes = [
    'craft10',
    'craft20',
    'craft30',
    'perform10',
    'perform20',
    'profession10',
    'profession20'
]

money_attributes = [
    'pp',
    'gp',
    'sp',
    'cp',
    'gems',
    'other'
]

skill_ranks = {
    'acrobatics': 'acrobatics3',
    'appraise': 'appraise3',
    'bluff': 'bluff3',
    'climb': 'climb3',
    'craft1': 'craft13',
    'craft2': 'craft23',
    'craft3': 'craft33',
    'diplomacy': 'diplomacy3',
    'disableDevice': 'disableDevice3',
    'disguise': 'disguise3',
    'escapeArtist': 'escapeArtist3',
    'fly': 'fly3',
    'handleAnimal': 'handleAnimal3',
    'heal': 'heal3',
    'intimidate': 'intimidate3',
    'knowledgeArcana': 'knowledgeArcana3',
    'knowledgeDungeoneering': 'knowledgeDungeoneering3',
    'knowledgeEngineering': 'knowledgeEngineering3',
    'knowledgeGeography': 'knowledgeGeography3',
    'knowledgeHistory': 'knowledgeHistory3',
    'knowledgeLocal': 'knowledgeLocal3',
    'knowledgeNature': 'knowledgeNature3',
    'knowledgeNobility': 'knowledgeNobility3',
    'knowledgePlanes': 'knowledgePlanes3',
    'knowledgeReligion': 'knowledgeReligion3',
    'linguistics': 'linguistics3',
    'perception': 'perception3',
    'perform1': 'perform13',
    'perform2': 'perform23',
    'profession1': 'profession13',
    'profession2': 'profession23',
    'ride': 'ride3',
    'senseMotive': 'senseMotive3',
    'sleightOfHand': 'sleightOfHand3',
    'spellcraft': 'spellcraft3',
    'stealth': 'stealth3',
    'survival': 'survival3',
    'swim': 'swim3',
    'useMagicDevice': 'useMagicDevice3'
}

skill_racial = {
    'acrobatics': 'acrobatics5',
    'appraise': 'appraise5',
    'bluff': 'bluff5',
    'climb': 'climb5',
    'craft1': 'craft15',
    'craft2': 'craft25',
    'craft3': 'craft35',
    'diplomacy': 'diplomacy5',
    'disableDevice': 'disableDevice5',
    'disguise': 'disguise5',
    'escapeArtist': 'escapeArtist5',
    'fly': 'fly5',
    'handleAnimal': 'handleAnimal5',
    'heal': 'heal5',
    'intimidate': 'intimidate5',
    'knowledgeArcana': 'knowledgeArcana5',
    'knowledgeDungeoneering': 'knowledgeDungeoneering5',
    'knowledgeEngineering': 'knowledgeEngineering5',
    'knowledgeGeography': 'knowledgeGeography5',
    'knowledgeHistory': 'knowledgeHistory5',
    'knowledgeLocal': 'knowledgeLocal5',
    'knowledgeNature': 'knowledgeNature5',
    'knowledgeNobility': 'knowledgeNobility5',
    'knowledgePlanes': 'knowledgePlanes5',
    'knowledgeReligion': 'knowledgeReligion5',
    'linguistics': 'linguistics5',
    'perception': 'perception5',
    'perform1': 'perform15',
    'perform2': 'perform25',
    'profession1': 'profession15',
    'profession2': 'profession25',
    'ride': 'ride5',
    'senseMotive': 'senseMotive5',
    'sleightOfHand': 'sleightOfHand5',
    'spellcraft': 'spellcraft5',
    'stealth': 'stealth5',
    'survival': 'survival5',
    'swim': 'swim5',
    'useMagicDevice': 'useMagicDevice5'
}

skill_trait = {
    'acrobatics': 'acrobatics6',
    'appraise': 'appraise6',
    'bluff': 'bluff6',
    'climb': 'climb6',
    'craft1': 'craft16',
    'craft2': 'craft26',
    'craft3': 'craft36',
    'diplomacy': 'diplomacy6',
    'disableDevice': 'disableDevice6',
    'disguise': 'disguise6',
    'escapeArtist': 'escapeArtist6',
    'fly': 'fly6',
    'handleAnimal': 'handleAnimal6',
    'heal': 'heal6',
    'intimidate': 'intimidate6',
    'knowledgeArcana': 'knowledgeArcana6',
    'knowledgeDungeoneering': 'knowledgeDungeoneering6',
    'knowledgeEngineering': 'knowledgeEngineering6',
    'knowledgeGeography': 'knowledgeGeography6',
    'knowledgeHistory': 'knowledgeHistory6',
    'knowledgeLocal': 'knowledgeLocal6',
    'knowledgeNature': 'knowledgeNature6',
    'knowledgeNobility': 'knowledgeNobility6',
    'knowledgePlanes': 'knowledgePlanes6',
    'knowledgeReligion': 'knowledgeReligion6',
    'linguistics': 'linguistics6',
    'perception': 'perception6',
    'perform1': 'perform16',
    'perform2': 'perform26',
    'profession1': 'profession16',
    'profession2': 'profession26',
    'ride': 'ride6',
    'senseMotive': 'senseMotive6',
    'sleightOfHand': 'sleightOfHand6',
    'spellcraft': 'spellcraft6',
    'stealth': 'stealth6',
    'survival': 'survival6',
    'swim': 'swim6',
    'useMagicDevice': 'useMagicDevice6'
}

skill_misc = {
    'acrobatics': 'acrobatics7',
    'appraise': 'appraise7',
    'bluff': 'bluff7',
    'climb': 'climb7',
    'craft1': 'craft17',
    'craft2': 'craft27',
    'craft3': 'craft37',
    'diplomacy': 'diplomacy7',
    'disableDevice': 'disableDevice7',
    'disguise': 'disguise7',
    'escapeArtist': 'escapeArtist7',
    'fly': 'fly7',
    'handleAnimal': 'handleAnimal7',
    'heal': 'heal7',
    'intimidate': 'intimidate7',
    'knowledgeArcana': 'knowledgeArcana7',
    'knowledgeDungeoneering': 'knowledgeDungeoneering7',
    'knowledgeEngineering': 'knowledgeEngineering7',
    'knowledgeGeography': 'knowledgeGeography7',
    'knowledgeHistory': 'knowledgeHistory7',
    'knowledgeLocal': 'knowledgeLocal7',
    'knowledgeNature': 'knowledgeNature7',
    'knowledgeNobility': 'knowledgeNobility7',
    'knowledgePlanes': 'knowledgePlanes7',
    'knowledgeReligion': 'knowledgeReligion7',
    'linguistics': 'linguistics7',
    'perception': 'perception7',
    'perform1': 'perform17',
    'perform2': 'perform27',
    'profession1': 'profession17',
    'profession2': 'profession27',
    'ride': 'ride7',
    'senseMotive': 'senseMotive7',
    'sleightOfHand': 'sleightOfHand7',
    'spellcraft': 'spellcraft7',
    'stealth': 'stealth7',
    'survival': 'survival7',
    'swim': 'swim7',
    'useMagicDevice': 'useMagicDevice7'
}

spells_data = {
    'zeroLevel.totalKnown': 'zeroLevelTotalKnown',
    'zeroLevel.dc': 'zeroLevelDC',
    'zeroLevel.totalPerDay': 'zeroLevelTotalPerDay',
    'firstLevel.totalKnown': 'firstLevelTotalKnown',
    'firstLevel.dc': 'firstLevelDC',
    'firstLevel.totalPerDay': 'firstLevelTotalPerDay',
    'firstLevel.bonusSpells': 'firstLevelBonusSpells',
    'secondLevel.totalKnown': 'secondLevelTotalKnown',
    'secondLevel.dc': 'secondLevelDC',
    'secondLevel.totalPerDay': 'secondLevelTotalPerDay',
    'secondLevel.bonusSpells': 'secondLevelBonusSpells',
    'thirdLevel.totalKnown': 'thirdLevelTotalKnown',
    'thirdLevel.dc': 'thirdLevelDC',
    'thirdLevel.totalPerDay': 'thirdLevelTotalPerDay',
    'thirdLevel.bonusSpells': 'thirdLevelBonusSpells',
    'fourthLevel.totalKnown': 'fourthLevelTotalKnown',
    'fourthLevel.dc': 'fourthLevelDC',
    'fourthLevel.totalPerDay': 'fourthLevelTotalPerDay',
    'fourthLevel.bonusSpells': 'fourthLevelBonusSpells',
    'fifthLevel.totalKnown': 'fifthLevelTotalKnown',
    'fifthLevel.dc': 'fifthLevelDC',
    'fifthLevel.totalPerDay': 'fifthLevelTotalPerDay',
    'fifthLevel.bonusSpells': 'fifthLevelBonusSpells',
    'sixthLevel.totalKnown': 'sixthLevelTotalKnown',
    'sixthLevel.dc': 'sixthLevelDC',
    'sixthLevel.totalPerDay': 'sixthLevelTotalPerDay',
    'sixthLevel.bonusSpells': 'sixthLevelBonusSpells',
    'seventhLevel.totalKnown': 'seventhLevelTotalKnown',
    'seventhLevel.dc': 'seventhLevelDC',
    'seventhLevel.totalPerDay': 'seventhLevelTotalPerDay',
    'seventhLevel.bonusSpells': 'seventhLevelBonusSpells',
    'eighthLevel.totalKnown': 'eighthLevelTotalKnown',
    'eighthLevel.dc': 'eighthLevelDC',
    'eighthLevel.totalPerDay': 'eighthLevelTotalPerDay',
    'eighthLevel.bonusSpells': 'eighthLevelBonusSpells',
    'ninthLevel.totalKnown': 'ninthLevelTotalKnown',
    'ninthLevel.dc': 'ninthLevelDC',
    'ninthLevel.totalPerDay': 'ninthLevelTotalPerDay',
    'ninthLevel.bonusSpells': 'ninthLevelBonusSpells',
}

inverse_spell_data = {
    'zeroLevelTotalKnown': ['zeroLevel', 'totalKnown'],
    'zeroLevelDC': ['zeroLevel', 'dc'],
    'zeroLevelTotalPerDay': ['zeroLevel', 'totalPerDay'],
    'firstLevelTotalKnown': ['firstLevel', 'totalKnown'],
    'firstLevelDC': ['firstLevel', 'dc'],
    'firstLevelTotalPerDay': ['firstLevel', 'totalPerDay'],
    'firstLevelBonusSpells': ['firstLevel', 'bonusSpells'],
    'secondLevelTotalKnown': ['secondLevel', 'totalKnown'],
    'secondLevelDC': ['secondLevel', 'dc'],
    'secondLevelTotalPerDay': ['secondLevel', 'totalPerDay'],
    'secondLevelBonusSpells': ['secondLevel', 'bonusSpells'],
    'thirdLevelTotalKnown': ['thirdLevel', 'totalKnown'],
    'thirdLevelDC': ['thirdLevel', 'dc'],
    'thirdLevelTotalPerDay': ['thirdLevel', 'totalPerDay'],
    'thirdLevelBonusSpells': ['thirdLevel', 'bonusSpells'],
    'fourthLevelTotalKnown': ['fourthLevel', 'totalKnown'],
    'fourthLevelDC': ['fourthLevel', 'dc'],
    'fourthLevelTotalPerDay': ['fourthLevel', 'totalPerDay'],
    'fourthLevelBonusSpells': ['fourthLevel', 'bonusSpells'],
    'fifthLevelTotalKnown': ['fifthLevel', 'totalKnown'],
    'fifthLevelDC': ['fifthLevel', 'dc'],
    'fifthLevelTotalPerDay': ['fifthLevel', 'totalPerDay'],
    'fifthLevelBonusSpells': ['fifthLevel', 'bonusSpells'],
    'sixthLevelTotalKnown': ['sixthLevel', 'totalKnown'],
    'sixthLevelDC': ['sixthLevel', 'dc'],
    'sixthLevelTotalPerDay': ['sixthLevel', 'totalPerDay'],
    'sixthLevelBonusSpells': ['sixthLevel', 'bonusSpells'],
    'seventhLevelTotalKnown': ['seventhLevel', 'totalKnown'],
    'seventhLevelDC': ['seventhLevel', 'dc'],
    'seventhLevelTotalPerDay': ['seventhLevel', 'totalPerDay'],
    'seventhLevelBonusSpells': ['seventhLevel', 'bonusSpells'],
    'eighthLevelTotalKnown': ['eighthLevel', 'totalKnown'],
    'eighthLevelDC': ['eighthLevel', 'dc'],
    'eighthLevelTotalPerDay': ['eighthLevel', 'totalPerDay'],
    'eighthLevelBonusSpells': ['eighthLevel', 'bonusSpells'],
    'ninthLevelTotalKnown': ['ninthLevel', 'totalKnown'],
    'ninthLevelDC': ['ninthLevel', 'dc'],
    'ninthLevelTotalPerDay': ['ninthLevel', 'totalPerDay'],
    'ninthLevelBonusSpells': ['ninthLevel', 'bonusSpells'],
}

defense_data = {
    'ac.total': 'ac_total',
    'ac.armorBonus': 'ac_armorBonus',
    'ac.shieldBonus': 'ac_shieldBonus',
    'ac.sizeBonus': 'ac_sizeBonus',
    'ac.naturalArmor': 'ac_naturalArmor',
    'ac.deflection': 'ac_deflection',
    'ac.miscModifier': 'ac_miscModifier',
    'ac.touch': 'ac_touch',
    'ac.flatFooted': 'ac_flatFooted',
    'ac.otherModifiers': 'ac_otherModifiers',
    'hp.total': 'hp_total',
    'hp.wounds': 'hp_wounds',
    'hp.nonLethal': 'hp_nonLethal',
    'damageReduction': 'damageReduction',
    'spellResistance': 'spellResistance',
    'fort.total': 'fort_total',
    'fort.base': 'fort_base',
    'fort.magicModifier': 'fort_magicModifier',
    'fort.miscModifier': 'fort_miscModifier',
    'fort.tempModifiers': 'fort_otherModifiers',
    'reflex.total': 'reflex_total',
    'reflex.base': 'reflex_base',
    'reflex.magicModifier': 'reflex_magicModifier',
    'reflex.miscModifier': 'reflex_miscModifier',
    'reflex.tempModifiers': 'reflex_otherModifiers',
    'will.total': 'will_total',
    'will.base': 'will_base',
    'will.magicModifier': 'will_magicModifier',
    'will.miscModifier': 'will_miscModifier',
    'will.tempModifiers': 'will_otherModifiers',
    'resistances': 'resistances',
    'immunities': 'immunities',
    'cmd.total': 'cmd_total',
    'cmd.sizeModifier': 'cmd_sizeModifier',
    'cmd.miscModifier': 'cmd_miscModifier',
    'cmd.tempModifiers': 'cmd_tempModifiers'
}

inverse_ac_defense_data = {
    'ac_total': 'total',
    'ac_armorBonus': 'armorBonus',
    'ac_shieldBonus': 'shieldBonus',
    'ac_sizeModifier': 'sizeModifier',
    'ac_naturalArmor': 'naturalArmor',
    'ac_DeflectionModifier': 'deflectionModifier',
    'ac_miscModifier': 'miscModifier',
    'ac_touch': 'touch',
    'ac_flatFooted': 'flatFooted',
    'ac_otherModifiers': 'otherModifiers',
}

inverse_hp_defense_data = {
    'hp_total': 'total',
    'hp_wounds': 'wounds',
    'hp_nonLethal': 'nonLethal',
}
inverse_fort_defense_data = {
    'fort_total': 'total',
    'fort_base': 'base',
    'fort_magicModifier': 'magicModifier',
    'fort_miscModifier': 'miscModifier',
    'fort_tempModifier': 'tempModifier',
    'fort_otherModifiers': 'otherModifiers',
}
inverse_reflex_defense_data = {
    'reflex_total': 'total',
    'reflex_base': 'base',
    'reflex_magicModifier': 'magicModifier',
    'reflex_miscModifier': 'miscModifier',
    'reflex_tempModifier': 'tempModifier',
    'reflex_otherModifiers': 'otherModifiers',
}
inverse_will_defense_data = {
    'will_total': 'total',
    'will_base': 'base',
    'will_magicModifier': 'magicModifier',
    'will_miscModifier': 'miscModifier',
    'will_tempModifier': 'tempModifier',
    'will_otherModifiers': 'otherModifiers',
}
inverse_cmd_defense_data = {
    'cmd_total': 'total',
    'cmd_sizeModifier': 'sizeModifier',
    'cmd_miscModifiers': 'miscModifiers',
    'cmd_tempModifiers': 'tempModifiers'
}
inverse_defense_data = {
    'resistances': 'resistances',
    'immunities': 'immunities',
    'damageReduction': 'damageReduction',
    'spellResistance': 'spellResistance',
}

skill_name = {

}

temp_ability_modifier = {
    'str': 'tempStrModifier',
    'int': 'tempIntModifier',
    'dex': 'tempDexModifier',
    'wis': 'tempWisModifier',
    'con': 'tempConModifier',
    'cha': 'tempChaModifier'
}

ability_modifier = {
    'str': 'strModifier',
    'int': 'intModifier',
    'dex': 'dexModifier',
    'wis': 'wisModifier',
    'con': 'conModifier',
    'cha': 'chaModifier'
}

spell_levels = {
    'zero': 0,
    'first': 1,
    'second': 2,
    'third': 3,
    'fourth': 4,
    'fifth': 5,
    'sixth': 6,
    'seventh': 7,
    'eighth': 8,
    'ninth': 9
}