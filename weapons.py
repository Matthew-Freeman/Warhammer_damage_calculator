
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
death_weavers = Weapon('Death weavers','D6','N/A',4,-1,1,'ranged',special={'torrent':True,'ignores_cover':True,'twin_linked':True})
spinneret_rifle = Weapon('Spinneret rifle','D6','N/A',5,-1,1,'ranged',special={'torrent':True,'ignores_cover':True})
dragon_fusion_gun = Weapon('Dragon fusion gun',1, 3,9,-4,'D6','ranged',special={'melta':3})
firepike = Weapon('Firepike',1, 3,12,-4,'D6','ranged',special={'melta':3})
reaper_launcher_starshot = Weapon('Reaper launcher - starshot',1, 3, 10, -2, 3,'ranged',special={'ignores_cover':True,'ignores_hit_mod':True})
reaper_launcher_starswarm = Weapon('Reaper launcher - starswarm',2, 3, 5, -2, 1,'ranged',special={'ignores_cover':True,'ignores_hit_mod':True})
reaper_missile_launcher_sunburst = Weapon('Missile launcher - sunburst','D6', 2, 4, -1,1,'ranged',special={'blast':True,'ignores_cover':True,'ignores_hit_mod':True})
reaper_missile_launcher_starshot = Weapon('Missile launcher - starshot',1, 2, 10,-2,'D6','ranged',special={'ignores_cover':True,'ignores_hit_mod':True})
avenger_catapult = Weapon('Avenger catapult',4, 3, 4, -1, 1,'ranged',special={'sustained_hits':1})


destructor_1 = Weapon('Destructor','D6', 'N/A', 5, -1, 1,'ranged',special={'torrent':True})
destructor_2 = Weapon('Destructor (+1)','D6+1', 'N/A', 6, -1, 1,'ranged',special={'torrent':True})
destructor_3 = Weapon('Destructor (+2)','D6+2', 'N/A', 7, -1, 1,'ranged',special={'torrent':True})
singing_spear_w = Weapon('Singing Spear',1,3,9,0,3,'ranged')
singing_spear_f = Weapon('Singing Spear',1,2,9,0,3,'ranged')
eldritch_storm = Weapon('Eldritch Storm','D6',3,6,-2,'D3','ranged',special={'blast':True})

prism_cannon_dispersed = Weapon('Prism Cannon dispersed','2D6',3,6,-2,2,'ranged',special={'rr_h1':True}) #haven't coded 1 reroll, so rerolling 1s instead.
prism_cannon_focused = Weapon('Prism Cannon focused',2,3,18,-4,6,'ranged',special={'rr_h1':True})
pulse_laser = Weapon('Pulse laser',3,3,9,-2,'D6','ranged')

shuriken_catapult = Weapon('Shuriken catapult',2, 3, 4, -1, 1,'ranged',special={})
shuriken_pistol = Weapon('Shuriken pistol',1, 3, 4, -1, 1,'ranged',special={'pistol':True})
twin_shuriken_catapult = Weapon('Twin Shuriken catapult',2, 3, 4, -1, 1,'ranged',special={'twin_linked':True})
ranger_long_rifle = Weapon('Ranger Long Rifle',1, 3, 4, -1, 2,'ranged',special={'heavy':True})

banshee_blade = Weapon('Banshee blade',2,2,4,-2,2,'melee',special={'anti_infantry':3})
executioner = Weapon('Executioner',3,2,6,-3,3,'melee',special={'anti_infantry':3})
scorpion_chainsword = Weapon('Scorpion chainsword',4,3,4,-1,1,'melee',special={'sustained_hits':1})
biting_blade = Weapon('Biting Blade',4,3,6,-3,1,'melee',special={'sustained_hits':1})
powerblade_array = Weapon('Powerblade array',10,3,4,-2,1,'melee',special={'lethal_hits':True,'twin_linked':True})
powerblades = Weapon('Powerblades',5,3,4,-2,1,'melee',special={'lethal_hits':True,'twin_linked':True})
aspect_close_combat_weapon = Weapon('Close combat weapon',2,3,3,0,1,'melee',special={})