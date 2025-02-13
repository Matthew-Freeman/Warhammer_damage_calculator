#calculate average damage.
import numpy as np
import matplotlib.pyplot as plt 


pt_scale = 100   #plot avg wounds per this many points

scale_for_inefficiency = True # When shooting 3-wound models with 2-damage weapons, 25% of the damage is overkill.

def main():

	#ranged_weapon(name, attacks, skill, strength, armour penetration, damage,special)

	death_spinner = weapon('Death spinner','D6','N/A',4,0,1,'ranged',special=['torrent','devastating_wounds'])
	fusion_gun = weapon('Dragon fusion gun',1, 2,9,-4,'D6','ranged',special=['melta_3'])
	reaper_launcher_starshot = weapon('Reaper launcher - starshot',1, 3, 8, -2, 2,'ranged')
	reaper_launcher_starswarm = weapon('Reaper launcher - starswarm',2, 3, 5, -1, 1,'ranged')

	starcannon = weapon('Starcannon',2, 3, 8, -3, 2,'ranged')
	shuriken_cannon = weapon('Shuriken cannon',3, 3, 6, -1, 2,'ranged',special=['sustained_hits'])
	scatter_laser = weapon('Scatter laser',6, 3, 5, 0, 1,'ranged')
	avenger_catapult = weapon('Avenger catapult',3, 3, 4, -1, 1,'ranged',special=['lethal_hits'])
	destructor = weapon('Destructor','D6', 3, 5, -1, 1,'ranged',special=['torrent'])
	singing_spear = weapon('Singing Spear',1,3,9,0,3,'ranged')
	m_marine = model('Marine',t=4,w=2,sv=3,guns=[],special=[])
	u_marines = unit('5 Marines',[m_marine]*5,tag='infantry')

	m_guardsman = model('10 Guardsmen',t=3,w=1,sv=5,guns=[],special=[])
	u_guardsmen = unit('10 Guardsmen',[m_guardsman]*10,tag='infantry')

	m_dire_avenger = model('Dire Avenger',t=3,w=1,sv=4,guns=[avenger_catapult],special=[])
	m_dire_avenger_exarch = model('Dire Avenger Exarch',t=3,w=2,sv=4,guns=[avenger_catapult,avenger_catapult],special=[])
	u_dire_avengers = unit('5 Dire Avengers',[m_dire_avenger]*4 + [m_dire_avenger_exarch],tag='infantry',cost=70)

	m_warlock = model('Warlock',t=3,w=1,sv=6,guns=[destructor,singing_spear],invuln=4,special=[])
	u_warlocks = unit('2 Warlocks', [m_warlock]*2,tag='infantry',cost=60)

	# target_list = [u_guardsmen,u_marines,u_skorpekh_destroyers,u_war_walker_scatter,u_falcon_scatter]


	# plot_dmg([u_striking_scorpions,u_striking_scorpions_c,u_striking_scorpions_np,u_striking_scorpions_c_np],target_list)
	# plot_dmg_per_pt([u_striking_scorpions,u_striking_scorpions_c,u_striking_scorpions_np,u_striking_scorpions_c_np],target_list)


	# avg_dmg, eff = weapon_attack(fusion_gun,u_marines,[],'ranged')
	# print(avg_dmg,eff)
	weapon_list = [death_spinner,fusion_gun,reaper_launcher_starshot,reaper_launcher_starswarm]
	# plot_wpn_dmg(weapon_list,[u_marines,u_guardsmen])

	# plot_wpn_dmg([scatter_laser,shuriken_cannon,starcannon],[u_marines,u_guardsmen])


	plot_wpn_dmg([avenger_catapult,destructor],[u_marines,u_guardsmen])

	plot_dmg_per_pt([u_dire_avengers, u_warlocks],[u_marines,u_guardsmen])

	plt.show()

def dmg_per_pt(attacker,target):
		dmg_per = unit_attack(attacker,target) / (attacker.cost) *100
		print('{} vs {} = {:.4f} damage per 100 points'.format(attacker.name,target.name,dmg_per))	



class  weapon():
	def __init__(self, name,attacks,skill,strength,ap,damage,type,special=[]):
		self.name = name
		self.attacks = attacks
		self.skill = skill
		self.s = strength
		self.ap = ap
		self.damage = damage
		self.type = type
		self.special = special


class unit():
	def __init__(self, name,members,tag=None,special_rules=[],cost=None):
		self.name = name
		self.members = members
		self.size = len(members)
		self.special_rules = special_rules
		self.tag = tag
		if cost is not None:
			self.cost = cost
		elif members[0].cost is not None:
			self.cost = sum(m.cost for m in members)
		else:
			self.cost = None

class model():
	def __init__(self,name,t,w,sv,guns=[],swords=[],invuln=None,special=[],cost=None):
		self.name = name
		self.t = t
		self.sv = sv
		self.w = w
		self.invuln=invuln
		self.special = special
		self.guns = guns
		self.swords = swords
		self.cost = cost


def unit_attack(attacking_unit,target_unit):
	total_damage = 0
	squad_efficiency = []
	for attacking_model in attacking_unit.members:
		temp_damage, efficiency = model_attack(attacking_model,target_unit,attacking_unit.special_rules)
		total_damage += temp_damage
		squad_efficiency.append(efficiency)
	print('{0:36} = {1:.3f} total wounds on average. {2:.0f}% efficiency'.format(attacking_unit.name+' vs '+target_unit.name,total_damage,efficiency*100))
	# print('Squad efficiency = {}'.format(squad_efficiency))
	return total_damage

# def sim(weapon,unit):
# 	avg = attack(weapon,unit)
# 	# print(weapon.name + ' vs ' + unit.name + ':', avg, 'wounds on average')
# 	print('{0:36}  {1:.3f} wounds on average'.format(weapon.name + ' vs ' + unit.name + ':', avg))
# 	return avg

def model_attack(attacking_model,target_unit,special_rules,):
	total_average_wounds = 0

	special_rules = attacking_model.special + special_rules

	for n, weapon in enumerate(attacking_model.guns):
		avg_wounds, efficiency = weapon_attack(weapon,target_unit,special_rules,a_type='ranged')
		print('{} wounds with {}'.format(avg_wounds,weapon.name))
		total_average_wounds += avg_wounds

	for n, weapon in enumerate(attacking_model.swords):
		avg_wounds, efficiency = weapon_attack(weapon,target_unit,special_rules,a_type='melee')
		print('{} wounds with {}'.format(avg_wounds,weapon.name))
		total_average_wounds += avg_wounds
	
	return total_average_wounds, efficiency

def weapon_attack(weapon,target_unit,special_rules,a_type):
	target_model = target_unit.members[0]
	a = weapon.attacks
	bs = weapon.skill
	s = weapon.s
	ap = weapon.ap	
	damage = weapon.damage
	sv = target_model.sv
	inv = target_model.invuln
	
	h_mod = 0
	w_mod = 0

	if '-1ap' in target_model.special:
			ap = min(weapon.ap+1,0)
	if '-1h' in target_model.special:
			h_mod = h_mod -1

	if 'indirect' in special_rules:
		bs = min(weapon.bs+1,6)
		sv = target_model.sv-1 
	
	if 'no invuln' in weapon.special:
			inv = None

	n_attacks = avg_attacks(a,weapon,target_unit.size)

	rr_hits=False
	if 'rr_hits' in special_rules:
		rr_hits = True
	expl6 = False	
	if 'sustained_hits' in weapon.special:
		expl6 = True
	if 'torrent' in weapon.special or 'autohit' in special_rules:
		p_hit = 1
	else:
		p_hit = hit(bs,h_mod,rr_hits)
		p_hit_base = p_hit
		if expl6:
			# print("exploding 6's")
			p_hit = p_hit + 1/6


	wound_modifier=0
	if '+1w' in special_rules:
		wound_modifier = 1

	autowound=False
	if 'autowound_m_nmv' in special_rules and a_type=='melee' and not(target_unit.tag=='vehicle' or target_unit.tag=='monster'):
		print('autowounding with',weapon.name)
		autowound = True
		p_wound = 1
	else:
		p_wound = wound(weapon.s,target_model.t,wound_modifier)
	

	p_fail_save = fail_save(sv,inv,ap)
	average_damage, efficiency = avg_damage(weapon.damage,target_model.w,target_model.special,mortal=False)
	mortal_damage, efficiency = avg_damage(weapon.damage,target_model.w,target_model.special,mortal=True)
	if 'witch' in weapon.special:
		p_wound = 5/6

	rrw1=False	
	if 'rrw1' in special_rules:
		rrw1=True
	if 'rrw1_v' in special_rules and (target_unit.tag=='vehicle' or target_unit.tag=='monster'):
		# print('rerolling 1\'s to wound')
		rrw1=True


	# if weapon.special == 'shuriken':
	if 'devastating_wounds' in weapon.special:
		avg_wounds = roll_devastating_attack(n_attacks,p_hit,p_wound,p_fail_save,average_damage,rrw1)
	elif 'lethal_hits' in weapon.special:
		avg_wounds = roll_lethal_attack(n_attacks,p_hit,p_wound,p_fail_save,average_damage,rrw1)
	else:
		avg_wounds = roll_regular_attack(n_attacks,p_hit,p_wound,p_fail_save,average_damage,rrw1)
	return avg_wounds, efficiency

def roll_regular_attack(n_attacks,p_hit,p_wound,p_fail_save,avg_damage,rrw1=False):
	avg_wounds = n_attacks * p_hit * p_wound * p_fail_save * avg_damage
	if rrw1:
		avg_wounds = n_attacks * p_hit * (p_wound + p_wound/6) * p_fail_save * avg_damage
	return avg_wounds

def roll_devastating_attack(n_attacks,p_hit,p_wound,p_fail_save,avg_damage,rrw1=False):
	# print()
	regular_wounds = n_attacks * p_hit * (p_wound-1/6) * p_fail_save * avg_damage
	ap_wounds = n_attacks * p_hit * 1/6 * avg_damage
	# avg_wounds = regular_wounds + ap_wounds
	if rrw1:
		p_dev_wound = 1/6
		p_regular_wound = p_wound-p_dev_wound
		regular_wounds = n_attacks * p_hit * (p_regular_wound + p_regular_wound*1/6) * p_fail_save * avg_damage
		ap_wounds = n_attacks * p_hit * (p_dev_wound + p_dev_wound*1/6) * avg_damage
	avg_wounds = regular_wounds + ap_wounds
	return avg_wounds

def roll_devastating_attack_old(n_attacks,p_hit,p_wound,p_fail_save,avg_damage,mortal_damage,rrw1=False):
	# print()
	regular_wounds = n_attacks * p_hit * (p_wound-1/6) * p_fail_save * avg_damage
	ap_wounds = n_attacks * p_hit * 1/6 * mortal_damage
	# avg_wounds = regular_wounds + ap_wounds
	if rrw1:
		p_dev_wound = 1/6
		p_regular_wound = p_wound-p_dev_wound
		regular_wounds = n_attacks * p_hit * (p_regular_wound + p_regular_wound*1/6) * p_fail_save * avg_damage
		ap_wounds = n_attacks * p_hit * (p_dev_wound + p_dev_wound*1/6) * mortal_damage
	avg_wounds = regular_wounds + ap_wounds
	return avg_wounds

def roll_lethal_attack(n_attacks,p_hit,p_wound,p_fail_save,avg_damage,mortal_damage,rrw1=False):
	# print()
	regular_wounds = n_attacks * (p_hit-1/6) * p_wound * p_fail_save * avg_damage
	lethal_wounds = n_attacks * 1/6 * 1 * p_fail_save * avg_damage
	# avg_wounds = regular_wounds + ap_wounds
	if rrw1:
		p_dev_wound = 1/6
		p_regular_wound = p_wound-p_dev_wound
		regular_wounds = n_attacks * p_hit * (p_regular_wound + p_regular_wound*1/6) * p_fail_save * avg_damage
		ap_wounds = n_attacks * p_hit * (p_dev_wound + p_dev_wound*1/6) * mortal_damage
	avg_wounds = regular_wounds + lethal_wounds
	return avg_wounds

def roll_sniper_attack(n_attacks,p_hit,p_wound,p_fail_save,avg_damage,headshot,mortals,p_hit_base,rrw1=False):
	regular_wounds = n_attacks * p_hit * p_wound * p_fail_save * avg_damage
	mortals = n_attacks * p_hit_base * headshot * mortals
	if rrw1:
		regular_wounds = n_attacks * p_hit * (p_wound + p_wound/6) * p_fail_save * avg_damage
		mortals = n_attacks * p_hit * (headshot+headshot/6) * mortals
	avg_wounds = regular_wounds + mortals
	return avg_wounds

# def roll_witch_attack(n_attacks,p_hit,p_wound,p_fail_save,avg_damage,sv,inv,ap):
# 	avg_wounds = n_attacks * p_hit * p_wound * p_fail_save * avg_damage
# 	return avg_wounds

# def roll_voidsniper_attack(weapon,target_model,n_attacks,p_hit,sv,inv,ap):
# 	regular_wounds = n_attacks * p_hit * wound(weapon.s,target_model.t) * fail_save(sv,inv,ap) * avg_damage(weapon.d,target_model.w,target_model.special)
# 	mortals = n_attacks * p_hit * 3/6 * 2
# 	avg_wounds = regular_wounds + mortals
# 	return avg_wounds


def avg_attacks(a,weapon,size):
	if 'blast' in weapon.special:
		blast_hits = size//5
	else:
		blast_hits = 0
	if a == 'D6':
		avg = 3.5 + blast_hits
	elif a == '2D6':
		avg = 7 + blast_hits
	elif a == 'D3':
		avg = 2 + blast_hits
	elif a == '3D3':
		avg = 6 + blast_hits
	elif a == 'D6+3':
		avg = 6.5 + blast_hits		
	else:
		avg = a + blast_hits
	return avg

def hit(bs,hmod=0,rr_hits=False):
	if hmod > 1:
		hmod = 1
	elif hmod <-1:
		hmod = -1
	bs = bs - hmod
	if bs <= 1:
		p = 5/6
	elif bs >= 6:
		p = 1/6 
	else:
		p = (7-bs)/6
	if rr_hits:
		p = 1-(1-p)**2
	return p

def wound(s,t,w_mod=0):
	#returns the probability of strength s wounding toughness t
	if s == t:
		p = 3+w_mod
	elif s >= 2*t:
		p = 5+w_mod
	elif s <= t/2:
		p = 1+w_mod
	elif s > t:
		p = 4+w_mod
	elif s < t:
		p = 2+w_mod
	if p > 5:
		p = 5
	elif p < 1:
		p = 1
	p = p/6
	return p


def fail_save(sv,inv,ap):
	sv2 = sv - ap
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

def avg_damage(d,w,special,mortal=False):
	# if special == '-1D':
	if '-1D' in special:
		resist = -1
	else:
		resist = 0

	if isinstance(d, str):
		D_idx = d.find('D')
		D_size = int(d[D_idx+1])
		if D_idx == 0:
			n_D = 1
		else:
			n_D = int(d[D_idx-1])
		plus_idx = d.find('+')
		if plus_idx == -1:
			added_damage = 0
		else:
			added_damage = int(d[plus_idx+1])
		roll_results = roll_recursion(n_D,D_size)
		roll_results = [i + added_damage for i in roll_results]	
	else:
		roll_results = [d]


	damage = []
	if not mortal:
		for roll in roll_results:
			roll2 = max(roll+resist,1)
			damage.append(min(roll2,w))
	elif mortal:
		for roll in roll_results:
			roll2 = max(roll+resist,1)
			damage.append(roll2)
	average_damage = sum(damage)/len(damage)

	#if d = 2, w = 3

	efficiency = 1.0
	if scale_for_inefficiency:
		if len(roll_results) == 1 or damage[0] >= w:
			shots_to_kill = np.ceil(w/damage[0])
			efficiency = w/(damage[0]*shots_to_kill)
			average_damage = average_damage*efficiency
			# print('{} shots to kill. Efficiency = {:.0f}%'.format(shots_to_kill,efficiency*100))
		else:
			pass
			# print('Not scaling for inefficiency, random damage = {}'.format(roll_results))

	return average_damage, efficiency

def roll_recursion(n_dice,D_size,roll_results=[],sum=0):
	if n_dice == 0:
		roll_results.append(sum)
	else:
		for i in range(1,D_size+1):
			roll_recursion(n_dice-1,D_size,roll_results,sum=i+sum)
	return roll_results

# def plot_sims(weapon_list,target_list):
# 	results = np.zeros((len(weapon_list),len(target_list)))
# 	for i, enemy in enumerate(target_list):
# 		for j, gun in enumerate(weapon_list):
# 			results[j,i] = sim(gun,enemy)  
# 		print('----------------------------')
# 	r = np.arange(len(target_list))
# 	width = 0.1	
# 	plt.figure(figsize=(12,6))
# 	for i, gun in enumerate(weapon_list):  
# 		plt.bar(r + width*i, results[i,:],
# 				 width = width, edgecolor = 'black',
# 				label=gun.name,zorder=3)
# 	plt.xlabel("Target")
# 	plt.ylabel("Average wounds inflicted")
# 	plt.title("Weapon Averages")
# 	plt.xticks(r + len(weapon_list)*width/2, [k.name for k in target_list])
# 	plt.legend(loc='best')
# 	plt.grid(zorder=0)
# 	# plt.show()
# 	print('done')

def plot_dmg_per_pt(attacker_list,target_list):
	results = np.zeros((len(attacker_list),len(target_list)))
	for i, enemy in enumerate(target_list):
		for j, attacker in enumerate(attacker_list):
			average_wounds = unit_attack(attacker,enemy)
			results[j,i] = average_wounds / (attacker.cost) *pt_scale  
			print('{:.3f} wounds divided by {} pts = {:.3f} wounds per 100 pts'.format(average_wounds,attacker.cost,results[j,i]))
		print('----------------------------')
	r = np.arange(len(target_list))
	width = 0.1	
	plt.figure(figsize=(12,6))
	for i, attacker in enumerate(attacker_list):  
		plt.bar(r + width*i, results[i,:],
				 width = width, edgecolor = 'black',
				label=attacker.name,zorder=3)
	plt.xlabel("Target")
	plt.ylabel("Average wounds per 100 pts")
	plt.title("Wounds per point")
	plt.xticks(r + len(attacker_list)*width/2, [k.name for k in target_list])
	plt.legend(loc='best')
	plt.grid(zorder=0)
	# plt.show()
	print('done')

def plot_dmg(attacker_list,target_list):
	results = np.zeros((len(attacker_list),len(target_list)))
	for i, enemy in enumerate(target_list):
		for j, attacker in enumerate(attacker_list):
			results[j,i] = unit_attack(attacker,enemy)  
		print('----------------------------')
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
	print('done')

def plot_wpn_dmg(weapon_list,target_list):
	results = np.zeros((len(weapon_list),len(target_list)))
	for i, enemy in enumerate(target_list):
		for j, weapon in enumerate(weapon_list):
			results[j,i], null = weapon_attack(weapon,enemy,[],weapon.type)
			print('{} vs {}, {:.3f} wounds'.format(weapon.name,enemy.name,results[j,i]))
		print('----------------------------')
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
	print('done')	

main()