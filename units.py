from weapons import *

class Unit():
	list = []
	def __init__(self, name,members,tag=None,special={},cost=None):
		self.name = name
		self.members = members
		self.size = len(members)
		self.special = special
		self.tag = tag
		if cost is not None:
			self.cost = cost
		elif members[0].cost is not None:
			self.cost = sum(m.cost for m in members)
		else:
			self.cost = None
		Unit.list.append(self)
		
class Model():
	list = []
	def __init__(self,name,t,w,sv,guns=[],swords=[],invuln=None,special={},cost=None):
		self.name = name
		self.t = t
		self.sv = sv
		self.w = w
		self.invuln=invuln
		self.special = special
		self.guns = guns
		self.swords = swords
		self.cost = cost
		Model.list.append(self)



m_marine = Model('Marine',t=4,w=2,sv=3,guns=[],special={})
u_marines = Unit('5 Marines',[m_marine]*5,tag='infantry')
u_marines_cover = Unit('5 Marines in cover',[m_marine]*5,tag='infantry',special={'cover':True})

m_terminator = Model('Terminator',t=5,w=3,sv=2,guns=[],invuln=4,special={})
u_terminators = Unit('5 Terminators',[m_terminator]*5,tag='infantry')

m_guardsman = Model('10 Guardsmen',t=3,w=1,sv=5,guns=[],special={})
u_guardsmen = Unit('10 Guardsmen',[m_guardsman]*10,tag='infantry')

m_dire_avenger = Model('Dire Avenger',t=3,w=1,sv=4,guns=[avenger_catapult],swords=[aspect_close_combat_weapon],invuln=5,special={})
m_dire_avenger_exarch = Model('Dire Avenger Exarch',t=3,w=2,sv=4,guns=[avenger_catapult,avenger_catapult],swords=[aspect_close_combat_weapon],invuln=5,special={})
u_dire_avengers = Unit('5 Dire Avengers',[m_dire_avenger]*4 + [m_dire_avenger_exarch],tag='infantry',cost=75)
u_dire_avengers_blitz = Unit('5 Dire Avengers Blitzing Firepower',[m_dire_avenger]*4 + [m_dire_avenger_exarch],tag='infantry',special={'critical_hits':5},cost=75)



m_fire_dragon = Model('Fire Dragon',t=3,w=1,sv=3,guns=[dragon_fusion_gun],swords=[aspect_close_combat_weapon],invuln=5,special={'rr_hits':['monster','vehicle'],'rr_wounds':['monster','vehicle'],'rr_damage':['monster','vehicle']})
m_fire_dragon_exarch = Model('Fire Dragon Exarch',t=3,w=2,sv=3,guns=[firepike],swords=[aspect_close_combat_weapon],invuln=5,special={'rr_hits':['monster','vehicle'],'rr_wounds':['monster','vehicle'],'rr_damage':['monster','vehicle']})
u_fire_dragons = Unit("5 Fire Dragons",[m_fire_dragon]*4 + [m_fire_dragon_exarch],tag='infrantry',cost=100)

m_howling_banshee = Model('Howling Banshee',t=3,w=1,sv=4,guns=[shuriken_pistol],swords=[banshee_blade],invuln=5,special={})
m_howling_banshee_exarch = Model('Howling Banshee Exarch',t=3,w=2,sv=4,guns=[shuriken_pistol],swords=[executioner],invuln=5,special={})
u_howling_banshees = Unit('5 Howling Banshees',[m_howling_banshee]*4 + [m_howling_banshee_exarch],tag='infantry',cost=90)

m_striking_scorpion = Model('Striking Scorpion',t=3,w=1,sv=3,guns=[shuriken_pistol],swords=[scorpion_chainsword],invuln=5,special={'critical_hits':5,'stealth':True})
m_striking_scorpion_exarch = Model('Striking Scorpion Exarch',t=3,w=2,sv=3,guns=[shuriken_pistol],swords=[biting_blade],invuln=5,special={'critical_hits':5,'stealth':True})
u_striking_scorpions = Unit('5 Striking Scorpions',[m_striking_scorpion]*4 + [m_striking_scorpion_exarch],tag='infantry',cost=75)

m_dark_reaper_1 = Model('Dark Reaper',t=3,w=1,sv=3,guns=[reaper_launcher_starshot],swords=[aspect_close_combat_weapon],invuln=5,special={})
m_dark_reaper_exarch_1 = Model('Dark Reaper Exarch',t=3,w=2,sv=3,guns=[reaper_missile_launcher_starshot],swords=[aspect_close_combat_weapon],invuln=5,special={})
u_dark_reapers_1 = Unit('5 Dark Reapers (starshot)',[m_dark_reaper_1]*4 + [m_dark_reaper_exarch_1],tag='infantry',cost=90)

m_dark_reaper_2 = Model('Dark Reaper',t=3,w=1,sv=3,guns=[reaper_launcher_starswarm],swords=[aspect_close_combat_weapon],invuln=5,special={})
m_dark_reaper_exarch_2 = Model('Dark Reaper Exarch',t=3,w=2,sv=3,guns=[reaper_missile_launcher_sunburst],swords=[aspect_close_combat_weapon],invuln=5,special={})
u_dark_reapers_2 = Unit('5 Dark Reapers (starswarm)',[m_dark_reaper_2]*4 + [m_dark_reaper_exarch_2],tag='infantry',cost=90)

m_warp_spider = Model('Warp Spider',t=3,w=1,sv=3,guns=[death_spinner],swords=[aspect_close_combat_weapon],invuln=5,special={})
m_warp_spider_exarch_1 = Model('Warp Spider Exarch',t=3,w=2,sv=3,guns=[death_weavers,spinneret_rifle],swords=[aspect_close_combat_weapon],invuln=5,special={})
m_warp_spider_exarch_2 = Model('Warp Spider Exarch',t=3,w=2,sv=3,guns=[death_weavers],swords=[powerblades],invuln=5,special={})
m_warp_spider_exarch_3 = Model('Warp Spider Exarch',t=3,w=2,sv=3,guns=[],swords=[powerblade_array],invuln=5,special={})
u_warp_spiders_1 = Unit("5 Warp Spiders (spinneret rifle)",[m_warp_spider]*4 + [m_warp_spider_exarch_1],tag='infrantry',cost=95)
u_warp_spiders_2 = Unit("5 Warp Spiders (powerblades)",[m_warp_spider]*4 + [m_warp_spider_exarch_2],tag='infrantry',cost=95)
u_warp_spiders_3 = Unit("5 Warp Spiders (powerblade array)",[m_warp_spider]*4 + [m_warp_spider_exarch_3],tag='infrantry',cost=95)

m_farseer = Model('Farseer',t=3,w=4,sv=6,guns=[eldritch_storm,singing_spear_f],invuln=4,special={'-1w':True})
m_warlock = Model('Warlock',t=3,w=2,sv=6,guns=[destructor_3,singing_spear_w],invuln=4,special={'-1w':True})
u_warlock_conclave = Unit('Farseer, 4 Warlocks, Guide', [m_warlock]*4+[m_farseer],tag='infantry',special={'+1h':True},cost=70+110)
u_warlock_conclave_blitz = Unit('Farseer, 4 Warlocks, Guide, Blitzing Firepower', [m_warlock]*4+[m_farseer],tag='infantry',special={'+1h':True,'sustained_hits':1},cost=70+110)

m_falcon = Model('Falcon',t=9,w=12,sv=3,guns=[],special={})
u_falcon = Unit('Falcon',[m_falcon],tag='vehicle',cost=130)

m_fire_prism_dispersed = Model('Fire Prism dispersed',t=9,w=12,sv=3,guns=[prism_cannon_dispersed],special={})
u_fire_prism_dispersed = Unit('Fire Prism dispersed',[m_fire_prism_dispersed],tag='vehicle',cost=160)

m_fire_prism_focused = Model('Fire Prism focused',t=9,w=12,sv=3,guns=[prism_cannon_focused],special={})
u_fire_prism_focused = Unit('Fire Prism focused',[m_fire_prism_focused],tag='vehicle',cost=160)

m_falcon_scatter = Model('Falcon',t=9,w=12,sv=3,guns=[pulse_laser,scatter_laser,shuriken_cannon],special={})
m_falcon_lance = Model('Falcon',t=9,w=12,sv=3,guns=[pulse_laser,bright_lance,shuriken_cannon],special={})
u_falcon_scatter = Unit('Falcon (scatter laser)',[m_falcon_scatter],tag='vehicle',cost=130)
u_falcon_lance = Unit('Falcon (bright lance)',[m_falcon_lance],tag='vehicle',cost=130)

m_lokhust_destroyer = Model('Lokust Destroyer',t=6,w=3,sv=3,guns=[],special={})
u_lokhust_destroyers = Unit('3 Lokhust Destroyers',[m_lokhust_destroyer]*3,tag='mounted',cost=90)

m_war_walker_starcannons = Model('War Walker with starcannons',t=7,w=6,sv=3,guns=[starcannon]*2,invuln=5,special={})
u_war_walker_starcannons = Unit('War Walker with starcannons',[m_war_walker_starcannons],tag='vehicle',cost=95)

m_vyper_shuriken_cannon = Model('Vyper with shuriken cannon',t=6,w=6,sv=3,guns=[shuriken_cannon,twin_shuriken_catapult],special={})
u_vyper_shuriken_cannon = Unit('Vyper with shuriken cannon',[m_vyper_shuriken_cannon],tag='vehicle',cost=65)

m_ranger = Model('Ranger',t=3,w=1,sv=5,guns=[ranger_long_rifle],invuln=5,special=['stealth'])
u_rangers = Unit('5 Rangers',[m_ranger]*5,tag='infantry',cost=55)

m_wraithguard = Model('Wraithguard',t=6,w=3,sv=2,guns=[wraithcannon])
u_wraithguard = Unit('5 Wraithguard',[m_wraithguard]*5,tag='infantry',special={'+1h':True},cost=170)
u_wraithguard_blitz = Unit('5 Wraithguard Blitzing Firepower',[m_wraithguard]*5,tag='infantry',special={'+1h':True,'sustained_hits':1},cost=170)

m_wraithlord = Model('Wraithlord',t=10,w=10,sv=2,guns=[shuriken_cannon,shuriken_cannon,flamer,flamer])
# m_wraithlord = Model('Wraithlord',t=10,w=10,sv=2,guns=[shuriken_cannon_wl,shuriken_cannon_wl,flamer,flamer])
u_wraithlord = Unit('Wraithlord',[m_wraithlord],tag='monster',cost=140)