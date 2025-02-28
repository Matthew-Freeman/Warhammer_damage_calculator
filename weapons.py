
class  Weapon():
	list = [] #a list of all created weapons
	def __init__(self, name,attacks,skill,strength,ap,damage,type,special=[]):
		self.name = name
		self.attacks = attacks
		self.skill = skill
		self.s = strength
		self.ap = ap
		self.damage = damage
		self.type = type #ranged or melee
		self.special = special
		Weapon.list.append(self)

	def delete(self):
		Weapon.list.remove(self)


starcannon = Weapon('Starcannon',2, 3, 8, -3, 2,'ranged')
shuriken_cannon = Weapon('Shuriken cannon',3, 3, 6, -1, 2,'ranged',special={'lethal_hits':True})
scatter_laser = Weapon('Scatter laser',6, 3, 5, 0, 1,'ranged',special={'sustained_hits':1})
missile_launcher_starshot = Weapon('Missile launcher - starshot',1, 3, 10,-2,'D6','ranged')
missile_launcher_sunburst = Weapon('Missile launcher - sunburst','D6', 3, 4, -1,1,'ranged',special={'blast':True})
bright_lance = Weapon('Bright Lance',1, 3, 12, -3, 'D6+2','ranged')

death_spinner = Weapon('Death spinner','D6','N/A',4,-1,1,'ranged',special={'torrent':True,'ignores_cover':True})
fusion_gun = Weapon('Dragon fusion gun',1, 3,9,-4,'D6','ranged',special={'melta':3})
reaper_launcher_starshot = Weapon('Reaper launcher - starshot',1, 3, 10, -2, 3,'ranged',special={'ignores_cover':True,'ignore_hit_mod':True})
reaper_launcher_starswarm = Weapon('Reaper launcher - starswarm',2, 3, 5, -2, 1,'ranged',special={'ignores_cover':True,'ignore_hit_mod':True})
avenger_catapult = Weapon('Avenger catapult',4, 3, 4, -1, 1,'ranged',special={'sustained_hits':1})
destructor = Weapon('Destructor','D6+2', 'N/A', 7, -1, 1,'ranged',special={'torrent':True})
singing_spear = Weapon('Singing Spear',1,3,9,0,3,'ranged')
prism_cannon_dispersed = Weapon('Prism Cannon dispersed','2D6',3,6,-2,2,'ranged',special={'rr_h1':True}) #haven't coded 1 reroll, so rerolling 1s instead.
prism_cannon_focused = Weapon('Prism Cannon focused',2,3,18,-4,6,'ranged',special={'rr_h1':True})
shuriken_catapult = Weapon('Shuriken catapult',2, 3, 4, -1, 1,'ranged',special={})
twin_shuriken_catapult = Weapon('Twin Shuriken catapult',2, 3, 4, -1, 1,'ranged',special={'twin_linked':True})
ranger_long_rifle = Weapon('Ranger Long Rifle',1, 3, 4, -1, 2,'ranged',special={'heavy':True})

