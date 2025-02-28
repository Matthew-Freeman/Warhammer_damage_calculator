#calculate average damage.
import numpy as np
import matplotlib.pyplot as plt 
import math

from weapons import *
from units import *

pt_scale = 100   #plot avg wounds per this many points

scale_for_wounded_models = True 
# i.e. When shooting 3-wound models with 2-damage weapons, 25% of the damage is wasted as overkill on wounded models.
# If true, damage will be scaled down by the efficiency percentage. Not implemented for random damage weapons.

def main():
	#ranged_weapon(name, attacks, ballistic skill, strength, armour penetration, damage, ranged/melee, special rules)
	eldar_heavy_weapons = [scatter_laser,shuriken_cannon,starcannon,bright_lance,missile_launcher_starshot,missile_launcher_sunburst]

	#manual vyper vs marines
	# print("manual vyper v marines",3 * 3/6 * 4/6 * 3/6 * 2, 3 * 1/6 * 6/6 * 3/6 * 2, 2 * 4/6 * 3/4 * 3/6 * 1)

	plot_dmg_per_pt([u_dark_reapers,u_war_walker_starcannons,u_fire_prism_dispersed,u_fire_prism_focused],[u_marines,u_terminators,u_falcon])

	plot_wpn_dmg(eldar_heavy_weapons,[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers])

	plot_unit_dmg([u_rangers,u_vyper_shuriken_cannon],[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers])

	# for item in Weapon.list:
	# 	print(item.name)

	plt.show()

# def dmg_per_pt(attacker,target):
# 		dmg_per = unit_attack(attacker,target) / (attacker.cost) *100
# 		print('{} vs {} = {:.4f} damage per 100 points'.format(attacker.name,target.name,dmg_per))	


def unit_attack(attacking_unit,target_unit):
	total_damage = 0
	squad_efficiency = []
	print("{0} vs {1} ".format(attacking_unit.name,target_unit.name))
	for attacking_model in attacking_unit.members:
		temp_damage, efficiency = model_attack(attacking_model,target_unit,attacking_unit.special_rules)
		total_damage += temp_damage
		squad_efficiency.append(efficiency)
	print('= {0:.3f} total wounds on average. Min {1:.0f}% efficiency'.format(total_damage,efficiency*100))
	# print('Squad efficiency = {}'.format(squad_efficiency))
	return total_damage

def model_attack(attacking_model,target_unit,special_rules,phase='shooting'):
	total_average_wounds = 0
	efficiencies = []

	special_rules = attacking_model.special + special_rules

	if phase == 'shooting' or phase == 'both':
		for n, weapon in enumerate(attacking_model.guns):
			avg_wounds, efficiency = weapon_attack(weapon,target_unit,special_rules,a_type='ranged')
			print('{:.4f} wounds with {}'.format(avg_wounds,weapon.name))
			total_average_wounds += avg_wounds
			efficiencies.append(efficiency)
	
	if phase == 'fight' or phase == 'both':
		for n, weapon in enumerate(attacking_model.swords):
			avg_wounds, efficiency = weapon_attack(weapon,target_unit,special_rules,a_type='melee')
			print('{:.4f} wounds with {}'.format(avg_wounds,weapon.name))
			total_average_wounds += avg_wounds
			efficiencies.append(efficiency)

	return total_average_wounds, min(efficiencies)	

def weapon_attack(weapon,target_unit,special_rules,a_type):
	target_model = target_unit.members[0]
	a = weapon.attacks
	bs = weapon.skill
	s = weapon.s
	ap = weapon.ap	
	damage = weapon.damage
	sv = target_model.sv
	inv = target_model.invuln
	
	hit_mod = 0
	wound_mod = 0
	indirect = False

	if '-1ap' in target_model.special:
			ap = min(weapon.ap+1,0)
	if '-1h' in target_model.special:
			hit_mod = hit_mod -1
	if 'stealth' in target_model.special:
			hit_mod = hit_mod -1
	if 'heavy' in weapon.special:
			hit_mod = hit_mod +1
	if 'indirect' in special_rules:
		hit_mod = hit_mod-1
		indirect=True
		# bs = min(weapon.bs+1,6)
		# sv = target_model.sv-1 
		cover=True
	
	if 'ignore_hit_mod' in weapon.special:
		hit_mod=0
	if 'no invuln' in weapon.special:
		inv = None

	n_attacks = avg_attacks(a,weapon,target_unit.size)


	if 'torrent' in weapon.special or 'autohit' in special_rules:
		p_hit = 1
	else:
		if 'rr_hits' in special_rules:
			rr_hits = True
		else:
			rr_hits=False
		if 'rr_h1' in weapon.special:
			rrh1 = True
		else:
			rrh1 = False

		p_hit = hit(bs,hit_mod,rr_hits,rrh1,indirect)
		# p_hit_base = p_hit
		# if 'sustained_hits_1' in weapon.special:
		# 	p_hit = p_hit + 1/6


	wound_modifier=0
	if '+1w' in special_rules:
		wound_modifier = 1

	rr_wounds = False
	if 'twin_linked' in weapon.special:
		# print('weapon is twin linked')
		rr_wounds = True
	
		

	autowound=False
	if 'autowound_m_nmv' in special_rules and a_type=='melee' and not(target_unit.tag=='vehicle' or target_unit.tag=='monster'):
		print('autowounding with',weapon.name)
		autowound = True
		p_wound = 1
	else:
		p_wound = wound(weapon.s,target_model.t,wound_modifier,rr_wounds=rr_wounds)
	

	p_fail_save = fail_save(sv,inv,ap)
	average_damage, efficiency = avg_damage(weapon,target_model,mortal=False)
	# mortal_damage, efficiency = avg_damage(weapon,target_model,mortal=True)
	if 'witch' in weapon.special:
		p_wound = 5/6

	rrw1=False	
	if 'rrw1' in special_rules:
		rrw1=True
	if 'rrw1_v' in special_rules and (target_unit.tag=='vehicle' or target_unit.tag=='monster'):
		# print('rerolling 1\'s to wound')
		rrw1=True

	p_crit_hit = 1/6
	p_crit_wound = 1/6
	if 'sustained_hits' in weapon.special:
		sustained_hits = weapon.special['sustained_hits']
	else:
		sustained_hits = 0
	if 'lethal_hits' in weapon.special:
		lethal_hits = True
	else:
		lethal_hits = False
	
	if 'devastating_wounds' in weapon.special:
		non_crit_hit_wounds = (n_attacks * (p_hit-p_crit_hit) * (p_wound-critical_wound_chance) * p_fail_save * average_damage
						+ n_attacks * (p_hit-p_crit_hit) * critical_wound_chance * 1 * average_damage)
		sustained_wounds = (n_attacks * p_crit_hit*sustained_hits * (p_wound-critical_wound_chance) * p_fail_save * average_damage
						+ n_attacks * p_crit_hit*sustained_hits * critical_wound_chance * 1 * average_damage)
		if lethal_hits:
			crit_hit_wounds = n_attacks * p_crit_hit * 1 * p_fail_save * average_damage
		else:
			crit_hit_wounds = (n_attacks * p_crit_hit * (p_wound-critical_wound_chance) * p_fail_save * average_damage
							+ n_attacks * p_crit_hit * critical_wound_chance * 1 * average_damage)

	else:
		non_crit_hit_wounds = n_attacks * (p_hit-p_crit_hit) * p_wound * p_fail_save * average_damage
		sustained_wounds = n_attacks * p_crit_hit*sustained_hits * p_wound * p_fail_save * average_damage
		if lethal_hits:
			crit_hit_wounds = n_attacks * p_crit_hit * 1 * p_fail_save * average_damage
		else:
			crit_hit_wounds = n_attacks * p_crit_hit * p_wound * p_fail_save * average_damage


	avg_wounds = non_crit_hit_wounds + sustained_wounds + crit_hit_wounds
	return avg_wounds, efficiency


def avg_attacks(a,weapon,size): #Returns average number of shots fired
	#a will either be an integer, or a string like 2D6+3
	if type(a) is int:
		avg = a 
	else:
		if a.index('D') == 0:
			n_dice = 1
		else:
			n_dice = int(a[a.index('D')-1])
		dice_size = int(a[a.index('D')+1])
		avg = n_dice * (dice_size/2 + 0.5)
		if "+" in a:
			avg+= int(a[a.index('+')+1])
	if 'blast' in weapon.special:
		avg+= size//5
	return avg

def hit(bs,hit_mod=0,rr_hits=False,rr_1s=False,indirect=False):
	if hit_mod > 1:
		hit_mod = 1
	elif hit_mod <-1:
		hit_mod = -1
	bs = bs - hit_mod
	if bs <= 1:
		p = 5/6
	elif bs >= 6:
		p = 1/6 
	else:
		p = (7-bs)/6
	if indirect and p > 3/6:
		p = 3/6
	if rr_hits:
		p = 1-(1-p)**2
	elif rr_1s:
		p = p + 1/6*p
	return p

def wound(s,t,wound_mod=0,rr_wounds=False,rr_1s=False):
	#returns the probability of strength s wounding toughness t
	if wound_mod > 1:
		wound_mod = 1
	elif wound_mod <-1:
		wound_mod = -1
	if s == t:
		p = 3
	elif s >= 2*t:
		p = 5
	elif s <= t/2:
		p = 1
	elif s > t:
		p = 4
	elif s < t:
		p = 2
	p+=wound_mod
	if p > 5:
		p = 5
	elif p < 1:
		p = 1
	p = p/6
	if rr_wounds:
		# print('rr_wounds:', p)
		p = 1-(1-p)**2
		# print('goes to:', p)
	elif rr_1s:
		p = p + 1/6*p
	return p

def fail_save(sv,inv,ap,cover=False):
	sv2 = sv - ap 
	if cover:
		sv2-= 1
	if inv is not None and inv < sv2:
		sv3 = inv
	else:
		sv3 = sv2
	if sv3 > 7:
		p = 1
	elif sv3 <= 1:
		p = 1/6
	else:
		p = (sv3-1)/6
	return p

def avg_damage(weapon,target_model,mortal=False):
	d = weapon.damage
	w = target_model.w
	if 'melta' in weapon.special:
		d+= weapon.special['melta']
	# if special == '-1D':
	if '-1D' in target_model.special:
		resist = -1
	else:
		resist = 0
	if 'half_D' in target_model.special:
		damage_multiplier = 0.5
	else:
		damage_multiplier = 1


	if type(d) is int:
		roll_results = [d]
	else:
		dice_size = int(d[d.index('D')+1])
		if d.index('D') == 0:
			n_dice = 1
		else:
			n_dice = int(d[d.index('D')-1])
		roll_results = roll_recursion(n_dice,dice_size)
		if '+' in d:
			# added_damage = int(d[d.index('+')+1])
			added_damage = int(d.split('+')[-1])
			roll_results = [i + added_damage for i in roll_results]	

	damage = []
	for roll in roll_results:
		roll2 = max(math.ceil(roll*damage_multiplier+resist),1)
		damage.append(min(roll2,w))
	average_damage = sum(damage)/len(damage)

	efficiency = 1.0
	if scale_for_wounded_models:
		if len(roll_results) == 1: #if fixed damage, then scale
			shots_to_kill = np.ceil(w/damage[0])
			efficiency = w/(damage[0]*shots_to_kill)
			average_damage = average_damage*efficiency
			# print('{} shots to kill. Efficiency = {:.0f}%'.format(shots_to_kill,efficiency*100))
		else:
			pass
			# print('Not scaling for inefficiency, random damage = {}'.format(roll_results))

	return average_damage, efficiency

def roll_recursion(n_dice,D_size,roll_results=[],sum=0): #rolls all possible combinations of n dice, returns a list of the sums.
	if n_dice == 0:
		roll_results.append(sum)
	else:
		for i in range(1,D_size+1):  
			roll_recursion(n_dice-1,D_size,roll_results,sum=i+sum)
	return roll_results

def plot_dmg_per_pt(attacker_list,target_list):
	results = np.zeros((len(attacker_list),len(target_list)))
	for i, enemy in enumerate(target_list):
		for j, attacker in enumerate(attacker_list):
			average_wounds = unit_attack(attacker,enemy)
			results[j,i] = average_wounds / (attacker.cost) *pt_scale  
			print('{:.3f} wounds divided by {} pts = {:.3f} wounds per {} pts\n'.format(average_wounds,attacker.cost,results[j,i],pt_scale))
	print('----------------------------\n')
	r = np.arange(len(target_list))
	width = 0.1	
	plt.figure(figsize=(12,6))
	for i, attacker in enumerate(attacker_list):  
		plt.bar(r + width*i, results[i,:],
				 width = width, edgecolor = 'black',
				label=attacker.name,zorder=3)
	plt.xlabel("Target")
	plt.ylabel("Average wounds per {} pts".format(pt_scale))
	plt.title("Wounds per {} points".format(pt_scale))
	plt.xticks(r + len(attacker_list)*width/2, [k.name for k in target_list])
	plt.legend(loc='best')
	plt.grid(zorder=0)
	# plt.show()
	# print('done')

def plot_unit_dmg(attacker_list,target_list):
	results = np.zeros((len(attacker_list),len(target_list)))
	for i, enemy in enumerate(target_list):
		for j, attacker in enumerate(attacker_list):
			results[j,i] = unit_attack(attacker,enemy) 
			print('') 
	print('----------------------------\n')
	r = np.arange(len(target_list))
	width = 0.1	
	plt.figure(figsize=(12,6))
	for i, attacker in enumerate(attacker_list):  
		plt.bar(r + width*i, results[i,:],
				 width = width, edgecolor = 'black',
				label=attacker.name,zorder=3)
	plt.xlabel("Target")
	plt.ylabel("Average wounds")
	plt.title("Wounds")
	plt.xticks(r + len(attacker_list)*width/2, [k.name for k in target_list])
	plt.legend(loc='best')
	plt.grid(zorder=0)
	# plt.show()
	# print('done')

def plot_wpn_dmg(weapon_list,target_list):
	results = np.zeros((len(weapon_list),len(target_list)))
	for i, enemy in enumerate(target_list):
		for j, weapon in enumerate(weapon_list):
			results[j,i], efficiency = weapon_attack(weapon,enemy,[],weapon.type)
			print('{} vs {}, {:.3f} wounds. {:.0f}% efficiency'.format(weapon.name,enemy.name,results[j,i],efficiency*100))
		print('')
	print('----------------------------\n')
	r = np.arange(len(target_list))
	width = 0.1	
	plt.figure(figsize=(12,6))
	for i, weapon in enumerate(weapon_list):  
		plt.bar(r + width*i, results[i,:],
				 width = width, edgecolor = 'black',
				label=weapon.name,zorder=3)
	plt.xlabel("Target")
	plt.ylabel("Average wounds")
	plt.title("Wounds")
	plt.xticks(r + len(weapon_list)*width/2, [k.name for k in target_list])
	plt.legend(loc='best')
	plt.grid(zorder=0)
	# plt.show()
	# print('done')	


if __name__ == "__main__":
    main()