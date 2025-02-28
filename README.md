# Warhammer_damage_calculator
Calculates average damage for attacks in Warhammer 40000

There are 3 main objects in the code to set up the scenario: weapons, models, and units.

Weapons have the properties: name, weapon skill, attacks, strength, armour penetration, damage, range/melee, and special rules.
Models have the properties: name, toughness, wounds, armour save, [weapons carried], invulnerable save, and special rules.
Units have the properties: name, [models in unit], type, and cost.


There are 3 main funtions to calculate results.

plot_wpn_damage takes a list of weapons and a list of units being targeted. It produces a plot showing the average damage of each weapon against each unit.
plot_unit_dmg is similar, but takes in a list of attacking units instead, and calculates the result from all their weapons.
plot_dmg_per_point does the same calculation as plot_dmg, but divided the result by the points cost, to give the average wounds per 100 pts.