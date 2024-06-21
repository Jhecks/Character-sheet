import operator

import qtTranslateLayer as qtl


def update_window(self):
    # Write data to general block in gui
    for attribute in qtl.general_attributes:
        widget = getattr(self, attribute)
        value = getattr(self.data_frame.general, attribute, "")
        widget.setText(value)

    # Write data to attributes block in gui
    for attribute_name in qtl.ability_attributes:
        widget = getattr(self, attribute_name)
        attribute_value = getattr(self.data_frame.abilities, attribute_name)
        widget.setText(attribute_value)
    self.scoreCalc.setText(self.data_frame.abilities.scoreCalc)
    self.int.setText(self.data_frame.abilities.int)

    # Write data to skills block in gui
    for skill_name, modifier in qtl.skill_attributes.items():
        skill_data = getattr(self.data_frame.skills, skill_name)
        actual_modifier = getattr(self.data_frame.abilities, qtl.temp_ability_modifier.get(modifier)) \
            if getattr(self.data_frame.abilities, qtl.temp_ability_modifier.get(modifier)) != '' \
            else getattr(self.data_frame.abilities, qtl.ability_modifier.get(modifier))
        self.set_skill_attributes(skill_name, skill_data, actual_modifier)

    self.craft10.setText(self.data_frame.skills.craft1.name)
    self.craft20.setText(self.data_frame.skills.craft2.name)
    self.craft30.setText(self.data_frame.skills.craft3.name)

    self.perform10.setText(self.data_frame.skills.perform1.name)
    self.perform20.setText(self.data_frame.skills.perform2.name)

    self.profession10.setText(self.data_frame.skills.profession1.name)
    self.profession20.setText(self.data_frame.skills.profession2.name)

    self.conditionalModifiers.setText(self.data_frame.skills.conditionalModifiers)

    self.languages.setText(self.data_frame.skills.languages)
    self.levelTotal.setText(self.data_frame.skills.xp.total)
    self.levelNext.setText(self.data_frame.skills.xp.toNextLevel)

    self.totalRanks.setText(self.data_frame.skills.totalRanks)

    # Write data to defense block in gui
    self.ac_total.setText(self.data_frame.defense.ac.total)
    self.ac_armorBonus.setText(self.data_frame.defense.ac.armorBonus)
    self.ac_shieldBonus.setText(self.data_frame.defense.ac.shieldBonus)
    self.ac_dexModifier.setText(self.data_frame.abilities.tempDexModifier
                                if self.data_frame.abilities.tempDexModifier != ""
                                else self.data_frame.abilities.dexModifier)
    self.ac_sizeModifier.setText(self.data_frame.defense.ac.sizeModifier)
    self.ac_naturalArmor.setText(self.data_frame.defense.ac.naturalArmor)
    self.ac_DeflectionModifier.setText(self.data_frame.defense.ac.deflectionModifier)
    self.ac_miscModifier.setText(self.data_frame.defense.ac.miscModifier)
    self.ac_touch.setText(self.data_frame.defense.ac.touch)
    self.ac_flatFooted.setText(self.data_frame.defense.ac.flatFooted)
    self.ac_otherModifiers.setText(self.data_frame.defense.ac.otherModifiers)

    self.hp_total.setText(self.data_frame.defense.hp.total)
    self.hp_wounds.setText(self.data_frame.defense.hp.wounds)
    self.hp_nonLethal.setText(self.data_frame.defense.hp.nonLethal)
    self.damageReduction.setText(self.data_frame.defense.damageReduction)
    self.spellResistance.setText(self.data_frame.defense.spellResistance)

    self.fort_total.setText(self.data_frame.defense.fort.total)
    self.fort_base.setText(self.data_frame.defense.fort.base)
    self.fort_abilityModifier.setText(self.data_frame.abilities.tempConModifier
                                      if self.data_frame.abilities.tempConModifier != ""
                                      else self.data_frame.abilities.conModifier)
    self.fort_magicModifier.setText(self.data_frame.defense.fort.magicModifier)
    self.fort_miscModifier.setText(self.data_frame.defense.fort.miscModifier)
    self.fort_tempModifier.setText(self.data_frame.defense.fort.tempModifier)
    self.fort_otherModifiers.setText(self.data_frame.defense.fort.otherModifiers)

    self.reflex_total.setText(self.data_frame.defense.reflex.total)
    self.reflex_base.setText(self.data_frame.defense.reflex.base)
    self.reflex_abilityModifier.setText(self.data_frame.abilities.tempDexModifier
                                        if self.data_frame.abilities.tempDexModifier != ""
                                        else self.data_frame.abilities.dexModifier)
    self.reflex_magicModifier.setText(self.data_frame.defense.reflex.magicModifier)
    self.reflex_miscModifier.setText(self.data_frame.defense.reflex.miscModifier)
    self.reflex_tempModifier.setText(self.data_frame.defense.reflex.tempModifier)
    self.reflex_otherModifiers.setText(self.data_frame.defense.reflex.otherModifiers)

    self.will_total.setText(self.data_frame.defense.will.total)
    self.will_base.setText(self.data_frame.defense.will.base)
    self.will_abilityModifier.setText(self.data_frame.abilities.tempWisModifier
                                      if self.data_frame.abilities.tempWisModifier != ""
                                      else self.data_frame.abilities.wisModifier)
    self.will_magicModifier.setText(self.data_frame.defense.will.magicModifier)
    self.will_miscModifier.setText(self.data_frame.defense.will.miscModifier)
    self.will_tempModifier.setText(self.data_frame.defense.will.tempModifier)
    self.will_otherModifiers.setText(self.data_frame.defense.will.otherModifiers)

    self.cmd_total.setText(self.data_frame.defense.cmd.total)
    self.cmd_strModifier.setText(self.data_frame.abilities.tempStrModifier
                                 if self.data_frame.abilities.tempStrModifier != ""
                                 else self.data_frame.abilities.strModifier)
    self.cmd_dexModifier.setText(self.data_frame.abilities.tempDexModifier
                                 if self.data_frame.abilities.tempDexModifier != ""
                                 else self.data_frame.abilities.dexModifier)
    self.cmd_sizeModifier.setText(self.data_frame.defense.cmd.sizeModifier)
    self.cmd_miscModifiers.setText(self.data_frame.defense.cmd.miscModifiers)
    self.cmd_tempModifiers.setText(self.data_frame.defense.cmd.tempModifiers)

    self.resistances.setText(self.data_frame.defense.resistances)
    self.immunities.setText(self.data_frame.defense.immunities)

    self.cmd_bab.setText(self.data_frame.offense.bab)

    # Write data to offense block in gui
    self.initiative_total.setText(self.data_frame.offense.initiative.total)
    self.initiative_dexModifier.setText(self.data_frame.abilities.tempDexModifier
                                        if self.data_frame.abilities.tempDexModifier != ""
                                        else self.data_frame.abilities.dexModifier)
    self.initiative_miscModifier.setText(self.data_frame.offense.initiative.miscModifier)
    self.bab.setText(self.data_frame.offense.bab)
    self.conditionalOffenseModifiers.setText(self.data_frame.offense.conditionalOffenseModifiers)
    self.speed_base.setText(self.data_frame.offense.speed.base)
    self.speed_withArmor.setText(self.data_frame.offense.speed.withArmor)
    self.speed_fly.setText(self.data_frame.offense.speed.fly)
    self.speed_swim.setText(self.data_frame.offense.speed.swim)
    self.speed_climb.setText(self.data_frame.offense.speed.climb)
    self.speed_burrow.setText(self.data_frame.offense.speed.burrow)
    self.speed_tempModifiers.setText(self.data_frame.offense.speed.tempModifiers)
    self.cmb_total.setText(self.data_frame.offense.cmb.total)
    self.cmb_bab.setText(self.data_frame.offense.bab)
    self.cmb_strModifier.setText(self.data_frame.abilities.tempStrModifier
                                 if self.data_frame.abilities.tempStrModifier != ""
                                 else self.data_frame.abilities.strModifier)
    self.cmb_sizeModifier.setText(self.data_frame.offense.cmb.sizeModifier)
    self.cmb_miscModifiers.setText(self.data_frame.offense.cmb.miscModifiers)
    self.cmb_tempModifiers.setText(self.data_frame.offense.cmb.tempModifiers)

    # money data
    self.pp.setText(self.data_frame.money.pp)
    self.gp.setText(self.data_frame.money.gp)
    self.sp.setText(self.data_frame.money.sp)
    self.cp.setText(self.data_frame.money.cp)
    self.gems.setText(self.data_frame.money.gems)
    self.other.setText(self.data_frame.money.other)

    self.ac_item_total.setText(self.data_frame.defense.ac.itemsTotals.bonus)
    self.ac_item_check_penalty.setText(self.data_frame.defense.ac.itemsTotals.armorCheckPenalty)
    self.ac_item_spell_penalty.setText(self.data_frame.defense.ac.itemsTotals.spellFailure)
    self.ac_item_weight.setText(self.data_frame.defense.ac.itemsTotals.weight)

    # spells data
    for data_frame_path, gui_path in qtl.spells_data.items():
        getattr(self, gui_path).setText(operator.attrgetter(data_frame_path)(self.data_frame.spells))
    self.spellsConditionalModifiers.setText(self.data_frame.spells.spellsConditionalModifiers)
    self.spellsSpeciality.setText(self.data_frame.spells.spellsSpeciality)

    # adding notes data
    self.notes.setPlainText(self.data_frame.notes)