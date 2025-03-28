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


	run_tests()

	# plot_unit_dmg_per_pt([u_dark_reapers,u_war_walker_starcannons,u_fire_prism_dispersed,u_fire_prism_focused],[u_marines,u_terminators,u_falcon])


	# plot_unit_dmg([u_rangers,u_vyper_shuriken_cannon],[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers])

	# plot_unit_dmg([u_dire_avengers, u_fire_dragons],[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'shooting')

	# plot_unit_dmg_per_pt([u_dire_avengers, u_warp_spiders, u_fire_dragons],[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'both')


	# plot_unit_dmg([u_warp_spiders_1,u_warp_spiders_2,u_warp_spiders_3],[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'both')

	# plot_unit_dmg_per_pt([u_striking_scorpions,u_howling_banshees],[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'fight')

	# plot_unit_dmg([u_dire_avengers, u_warp_spiders_2, u_fire_dragons,u_dark_reapers],[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'shooting')
	# plot_unit_dmg_per_pt([u_dire_avengers, u_warp_spiders_2, u_fire_dragons,u_dark_reapers],[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'shooting')
	# plot_unit_dmg_per_pt([u_warlock_conclave],[u_marines,u_marines_cover,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'shooting')
	
	plot_wpn_dmg(eldar_heavy_weapons,[u_marines,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers])

	# plot_unit_dmg([u_dire_avengers, u_dire_avengers_blitz, u_warp_spiders_2, u_fire_dragons,u_dark_reapers_1,u_dark_reapers_2,u_warlock_conclave,u_warlock_conclave_blitz],[u_marines,u_marines_cover,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'shooting')

	plot_unit_dmg([u_falcon_scatter,u_falcon_lance,u_fire_prism_focused,u_fire_prism_dispersed],[u_marines,u_marines_cover,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'shooting')

	# plot_unit_dmg([u_wraithguard,u_wraithguard_blitz,u_wraithlord],[u_marines,u_marines_cover,u_guardsmen,u_dire_avengers,u_terminators, u_falcon,u_lokhust_destroyers],'shooting')

	# for item in Weapon.list:
	# 	print(item.name)

	plt.show()


def unit_attack(attacking_unit,target_unit,phase,verbose=1):
	total_damage = 0
	squad_efficiency = []
	if verbose > 0:
		print("{0} vs {1} ".format(attacking_unit.name,target_unit.name))
	for attacking_model in attacking_unit.members:
		temp_damage, efficiency = model_attack(attacking_model,target_unit,attacking_unit.special,phase,verbose)
		total_damage += temp_damage
		squad_efficiency.append(efficiency)
	if verbose > 0:
		print('= {0:.3f} total wounds on average. Min {1:.0f}% efficiency'.format(total_damage,efficiency*100))
	return total_damage

def model_attack(attacking_model,target_unit,attacking_unit_special_rules,phase='shooting',verbose=0):
	total_average_wounds = 0
	efficiencies = []

	attacker_special_rules = attacking_model.special | attacking_unit_special_rules # | merges dictionaries

	if phase == 'shooting' or phase == 'both':
		for n, weapon in enumerate(attacking_model.guns):
			avg_wounds, efficiency = weapon_attack(weapon,target_unit,attacker_special_rules,a_type='ranged')
			if verbose > 0:
				print('{:.4f} wounds with {}'.format(avg_wounds,weapon.name))
			total_average_wounds += avg_wounds
			efficiencies.append(efficiency)
	
	if phase == 'fight' or phase == 'both':
		for n, weapon in enumerate(attacking_model.swords):
			avg_wounds, efficiency = weapon_attack(weapon,target_unit,attacker_special_rules,a_type='melee')
			if verbose > 0:
				print('{:.4f} wounds with {}'.format(avg_wounds,weapon.name))
			total_average_wounds += avg_wounds
			efficiencies.append(efficiency)

	return total_average_wounds, min(efficiencies)	

def weapon_attack(weapon,target_unit,attacker_special_rules,a_type):
	target_model = target_unit.members[0]
	a = weapon.attacks
	bs = weapon.skill
	s = weapon.s
	ap = weapon.ap	
	damage = weapon.damage
	sv = target_model.sv
	inv = target_model.invuln
	
	attacker_special_rules = weapon.special | attacker_special_rules

	hit_mod = 0
	wound_mod = 0
	indirect = False
	if '-1ap' in target_model.special:
		ap = min(weapon.ap+1,0)
	if '-1h' in target_model.special:
		hit_mod -=1
	if 'stealth' in target_model.special:
		hit_mod -=1
	if 'heavy' in attacker_special_rules:
		hit_mod +=1
	if '+1h' in attacker_special_rules:
		hit_mod +=1


	
	cover = False
	if 'indirect' in attacker_special_rules:
		hit_mod -=1
		indirect=True
		# bs = min(weapon.bs+1,6)
		# sv = target_model.sv-1 
		cover=True
	if 'cover' in target_unit.special:
		cover = True

	if 'ignores_hit_mod' in attacker_special_rules:
		hit_mod=0
	# if 'no invuln' in weapon.special:
	# 	inv = None
	if 'ignores_cover' in attacker_special_rules:
		cover = False

	n_attacks = avg_attacks(a,weapon,target_unit.size)

	rr_hits = False
	rr_hits1 = False
	if 'rr_hits' in attacker_special_rules: 
		if type(attacker_special_rules['rr_hits'])==bool:
			rr_hits = attacker_special_rules['rr_hits'] #Should always be True
		elif target_unit.tag in attacker_special_rules['rr_hits']:
			rr_hits = True
		
	if 'rr_hits1' in attacker_special_rules:
		if type(attacker_special_rules['rr_hit1s'])==bool:
			rr_hits = attacker_special_rules['rr_hits1']
		elif target_unit.tag in attacker_special_rules['rr_hits1']:
			rr_hits = True		

	crit_hit = 1/6
	if 'critical_hits' in attacker_special_rules:
		crit_hit = 1 - (attacker_special_rules['critical_hits']-1)/6

	if 'torrent' in attacker_special_rules or 'autohit' in attacker_special_rules:
		p_normal_hit = 1
		p_crit_hit = 0
	else:
		p_normal_hit, p_crit_hit, p_miss = hit(bs,hit_mod,crit_hit,rr_hits,rr_hits1,indirect)

	wound_modifier=0
	if '+1w' in attacker_special_rules:
		wound_modifier += 1
	if '-1w' in target_model.special:
		wound_modifier -= 1

	rr_wounds = False
	if 'twin_linked' in attacker_special_rules:
		rr_wounds = True	
	if 'rr_wounds' in attacker_special_rules: 
		if type(attacker_special_rules['rr_wounds'])==bool:
			rr_wounds = attacker_special_rules['rr_wounds'] #Should always be True
		elif target_unit.tag in attacker_special_rules['rr_wounds']:
			rr_wounds = True

	rr_wounds1 = False
	if 'rr_wounds1' in attacker_special_rules: 		
		if type(attacker_special_rules['rr_wounds1'])==bool:
			rr_wounds1 = attacker_special_rules['rr_wounds1'] #Should always be True
		elif target_unit.tag in attacker_special_rules['rr_wounds1']:
			rr_wounds1 = True

	crit_wound = 1/6
	if 'anti_infantry' in attacker_special_rules and target_unit.tag=='infantry':
		crit_wound = 1 - (attacker_special_rules['anti_infantry']-1)/6
	if 'anti_vehicle' in attacker_special_rules and target_unit.tag=='vehicle':
		crit_wound = 1 - (attacker_special_rules['anti_vehicle']-1)/6
	if 'anti_monster' in attacker_special_rules and target_unit.tag=='monster':
		crit_wound = 1 - (attacker_special_rules['anti_monster']-1)/6

	p_normal_wound, p_crit_wound, p_fail_wound= wound(weapon.s,target_model.t,wound_modifier,crit_wound,rr_wounds=rr_wounds,rr_1s=rr_wounds1)

	p_fail_save = fail_save(sv,inv,ap,cover)

	rr_damage = False
	# if 'rr_damage_vehicle' in attacker_special_rules and target_unit.tag == 'vehicle':
	# 	print('rerolling damage against vehicle')
	# 	rr_damage = True
	# if 'rr_damage_monster' in attacker_special_rules and target_unit.tag == 'monster':
	# 	rr_damage = True
	if 'rr_damage' in attacker_special_rules: 		
		if type(attacker_special_rules['rr_damage'])==bool:
			rr_damage = attacker_special_rules['rr_damage'] #Should always be True
		elif target_unit.tag in attacker_special_rules['rr_damage']:
			rr_damage = True



	average_damage, efficiency = avg_damage(weapon,target_model,mortal=False,rr_damage=rr_damage)
	# mortal_damage, efficiency = avg_damage(weapon,target_model,mortal=True)
	
	sustained_hits = 0
	if 'sustained_hits' in attacker_special_rules:
		sustained_hits = attacker_special_rules['sustained_hits']



	lethal_hits = False
	if 'lethal_hits' in attacker_special_rules:
		lethal_hits = True


	if 'rr_one_hit' in attacker_special_rules:
		p_miss, p_normal_hit, p_crit_hit = rr_one(p_miss,p_normal_hit,p_crit_hit,n_attacks,True)

	if 'rr_one_wound' in attacker_special_rules:  #this doesn't really work, the maths assumes all successful hits.
		p_fail_wound, p_normal_wound, p_crit_wound = rr_one(p_fail_wound,p_normal_wound,p_crit_wound,n_attacks,True)		

	if 'devastating_wounds' in attacker_special_rules:
		non_crit_hit_wounds = (n_attacks * p_normal_hit * p_normal_wound * p_fail_save * average_damage
						+ n_attacks * p_normal_hit * p_crit_wound * 1 * average_damage)
		sustained_wounds = (n_attacks * p_crit_hit*sustained_hits * p_normal_wound * p_fail_save * average_damage
						+ n_attacks * p_crit_hit*sustained_hits * p_crit_wound * 1 * average_damage)
		if lethal_hits:
			crit_hit_wounds = n_attacks * p_crit_hit * 1 * p_fail_save * average_damage
		else:
			crit_hit_wounds = (n_attacks * p_crit_hit * p_normal_wound * p_fail_save * average_damage
							+ n_attacks * p_crit_hit * p_crit_wound * 1 * average_damage)

	else:
		non_crit_hit_wounds = n_attacks * p_normal_hit * (p_normal_wound+p_crit_wound) * p_fail_save * average_damage
		sustained_wounds = n_attacks * p_crit_hit*sustained_hits * (p_normal_wound+p_crit_wound) * p_fail_save * average_damage
		if lethal_hits:
			crit_hit_wounds = n_attacks * p_crit_hit * 1 * p_fail_save * average_damage
		else:
			crit_hit_wounds = n_attacks * p_crit_hit * (p_normal_wound+p_crit_wound) * p_fail_save * average_damage



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

def hit(bs,hit_mod=0,crit_hit_chance=1/6,rr_hits=False,rr_1s=False,indirect=False):
	if hit_mod > 1:
		hit_mod = 1
	elif hit_mod <-1:
		hit_mod = -1
	bs = bs - hit_mod
	if bs <= 1:
		hit_chance = 5/6
	elif bs >= 6:
		hit_chance = 1/6 
	else:
		hit_chance = (7-bs)/6
	if indirect and hit_chance > 3/6:
		hit_chance = 3/6
	
	p_normal_hit = max(hit_chance-crit_hit_chance,0)
	p_crit_hit = crit_hit_chance
	p_miss = 1-(p_normal_hit+p_crit_hit)

	if rr_hits:
		p_crit_hit = crit_hit_chance + p_miss*crit_hit_chance
		p_normal_hit = 1 - (p_miss)**2 - p_crit_hit
	elif rr_1s:
		p_crit_hit = crit_hit_chance + 1/6*crit_hit_chance
		p_normal_hit = p_normal_hit + 1/6*p_normal_hit
	



	return p_normal_hit, p_crit_hit, p_miss

def wound(s,t,wound_mod=0,crit_wound_chance=1/6,rr_wounds=False,rr_1s=False):
	#returns the probability of strength s wounding toughness t
	if wound_mod > 1:
		wound_mod = 1
	elif wound_mod <-1:
		wound_mod = -1
	if s == t:
		wound_chance = 3/6
	elif s >= 2*t:
		wound_chance = 5/6
	elif s <= t/2:
		wound_chance = 1/6
	elif s > t:
		wound_chance = 4/6
	elif s < t:
		wound_chance = 2/6
	wound_chance+=wound_mod/6
	if wound_chance > 5/6:
		wound_chance = 5/6
	elif wound_chance < 1/6:
		wound_chance = 1/6

	p_normal_wound = max(wound_chance-crit_wound_chance,0)
	p_crit_wound = crit_wound_chance
	p_fail = 1-(p_normal_wound+p_crit_wound)

	if rr_wounds:
		p_crit_wound = crit_wound_chance + p_fail*crit_wound_chance
		p_normal_wound = 1 - (p_fail)**2 - p_crit_wound
	elif rr_1s:
		p_crit_wound = crit_wound_chance + 1/6*crit_wound_chance
		p_normal_wound = p_normal_wound + 1/6*p_normal_wound

	return p_normal_wound, p_crit_wound, p_fail

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

def avg_damage(weapon,target_model,rr_damage=False,mortal=False):
	d = weapon.damage
	w = target_model.w
	if 'melta' in weapon.special:
		d = d + '+' + str(weapon.special['melta'])
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
		roll_results = roll_recursion(n_dice,dice_size,[])
		if '+' in d:
			# added_damage = int(d[d.index('+')+1])
			added_damage = int(d.split('+')[-1])
			roll_results = [i + added_damage for i in roll_results]	

	damage = []
	for roll in roll_results:
		roll2 = max(math.ceil(roll*damage_multiplier+resist),1)
		damage.append(min(roll2,w))
	average_damage = sum(damage)/len(damage)

	if rr_damage:
		damage = []
		for roll in roll_results:
			roll3 = max(math.ceil(roll*damage_multiplier+resist),1)
			inflicted = min(roll3,w)
			if inflicted < average_damage:
				damage.append(average_damage)
			else:
				damage.append(inflicted)
		average_damage = sum(damage)/len(damage)

	efficiency = 1.0
	if scale_for_wounded_models:
		if len(roll_results) == 1: #if fixed damage, then scale
			shots_to_kill = np.ceil(w/damage[0])
			efficiency = w/(damage[0]*shots_to_kill)
			average_damage = average_damage*efficiency

	return average_damage, efficiency

def roll_recursion(n_dice,D_size,roll_results,sum=0): #rolls all possible combinations of n dice, returns a list of the sums.
	if n_dice == 0:
		roll_results.append(sum)
	else:
		for i in range(1,D_size+1):  
			roll_recursion(n_dice-1,D_size,roll_results,sum=i+sum)
	return roll_results


def rr_one(p_miss,p_normal_hit,p_crit,shots_fired,reroll_remaining):  #calculates chance of hitting when allowed one reroll.
	
	sequences, probabilties = rr_one_sequence(p_miss,p_normal_hit,p_crit,[],1,[],[],shots_fired,reroll_remaining)
	
	avg_misses = 0
	avg_hits = 0
	avg_crits = 0

	for i, sequence in enumerate(sequences):
		avg_misses += max(sequence.count('miss')-1,0)*probabilties[i] # -1 because one one of the misses is rerolled and doesn't count as a shot. Max to avoid negative misses.
		avg_hits += sequence.count('hit')*probabilties[i]
		avg_crits += sequence.count('crit')*probabilties[i]
	
	avg_misses = avg_misses / shots_fired
	avg_hits = avg_hits / shots_fired
	avg_crits = avg_crits / shots_fired

	return  avg_misses, avg_hits, avg_crits, 

def rr_one_sequence(p_miss,p_normal_hit,p_crit,current_sequence,current_probability,all_sequences,all_probabilities,shots_remaining,reroll_remaining):
	if shots_remaining == 0:
		all_sequences.append(current_sequence)
		all_probabilities.append(current_probability)
	else:
		if reroll_remaining:
			rr_one_sequence(p_miss,p_normal_hit,p_crit,current_sequence+['miss'], current_probability*p_miss, all_sequences,all_probabilities,shots_remaining, False)
		else:
			rr_one_sequence(p_miss,p_normal_hit,p_crit,current_sequence+['miss'], current_probability*p_miss, all_sequences,all_probabilities,shots_remaining-1, reroll_remaining)
		rr_one_sequence(p_miss,p_normal_hit,p_crit,current_sequence+['hit'], current_probability*p_normal_hit, all_sequences,all_probabilities,shots_remaining-1,reroll_remaining)
		rr_one_sequence(p_miss,p_normal_hit,p_crit,current_sequence+['crit'], current_probability*p_crit,all_sequences,all_probabilities,shots_remaining-1,reroll_remaining)

	return all_sequences, all_probabilities


def plot_unit_dmg_per_pt(attacker_list,target_list,phase):
	results = np.zeros((len(attacker_list),len(target_list)))
	for i, enemy in enumerate(target_list):
		for j, attacker in enumerate(attacker_list):
			average_wounds = unit_attack(attacker,enemy,phase,verbose=1)
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
	plt.title("Wounds per {} points. Phase = {}".format(pt_scale,phase))
	plt.xticks(r + len(attacker_list)*width/2, [k.name for k in target_list])
	plt.legend(loc='best')
	plt.grid(zorder=0)
	# plt.show()

def plot_unit_dmg(attacker_list,target_list,phase):
	results = np.zeros((len(attacker_list),len(target_list)))
	for i, enemy in enumerate(target_list):
		for j, attacker in enumerate(attacker_list):
			results[j,i] = unit_attack(attacker,enemy,phase,verbose=1) 
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
	plt.title("Wounds. Phase = {}".format(phase))
	plt.xticks(r + len(attacker_list)*width/2, [k.name for k in target_list])
	plt.legend(loc='best')
	plt.grid(zorder=0)
	# plt.show()

def plot_wpn_dmg(weapon_list,target_list):
	results = np.zeros((len(weapon_list),len(target_list)))
	for i, enemy in enumerate(target_list):
		for j, weapon in enumerate(weapon_list):
			results[j,i], efficiency = weapon_attack(weapon,enemy,{},weapon.type)
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


def test_unit_attack(attacker,enemy,phase,expected):
	sim_result = unit_attack(attacker,enemy,phase,verbose=0)
	assert abs(sim_result - expected) < 0.001, '{} vs {}. Sim result = {:.4f}. Expected result = {:.4f}'.format(attacker.name,enemy.name,sim_result,expected)

def run_tests():
	print('Running tests')
	test_unit_attack(u_dire_avengers,u_marines,'shooting',6*4*5/6*3/6*3/6*1)
	test_unit_attack(u_vyper_shuriken_cannon,u_marines,'shooting',3 * 3/6 * 4/6 * 3/6 * 2 + 3 * 1/6 * 6/6 * 3/6 * 2 + 2 * 4/6 * 3/4 * 3/6 * 1)
	test_unit_attack(u_howling_banshees,u_falcon,'fight',4*2 * 5/6 * 1/6 * 4/6 * 2 + 3 * 5/6 * 2/6 * 5/6 * 3)
	test_unit_attack(u_warlock_conclave,u_marines,'shooting',4 * 5.5 * 1 * 4/6 * 3/6 * 1 + 5 * 1 * 5/6 * 5/6 * 2/6 *2 + 1*4.5*5/6*4/6*4/6*5/3)
	test_unit_attack(u_howling_banshees,u_marines,'fight',4* 2 * 5/6 * 4/6 * 4/6 * 2 + 3*5/6*4/6*5/6*2)
	test_unit_attack(u_fire_dragons,u_falcon,'shooting',4*8/9*3/4*1*(6.5+6.5+6.5+7+8+9)/6 + 1*8/9*8/9*1*(6.5+6.5+6.5+7+8+9)/6)
	print("All tests passed\n")

if __name__ == "__main__":
    main()