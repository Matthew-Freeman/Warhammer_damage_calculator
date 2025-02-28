from weapons import *

class Unit():
	list = []
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
		Unit.list.append(self)
		
class Model():
	list = []
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
		Model.list.append(self)



m_marine = Model('Marine',t=4,w=2,sv=3,guns=[],special=[])
u_marines = Unit('5 Marines',[m_marine]*5,tag='infantry')

m_terminator = Model('Terminator',t=5,w=3,sv=2,guns=[],invuln=4,special=[])
u_terminators = Unit('5 Terminators',[m_terminator]*5,tag='infantry')

m_guardsman = Model('10 Guardsmen',t=3,w=1,sv=5,guns=[],special=[])
u_guardsmen = Unit('10 Guardsmen',[m_guardsman]*10,tag='infantry')

m_dire_avenger = Model('Dire Avenger',t=3,w=1,sv=4,guns=[avenger_catapult],invuln=5,special=[])
m_dire_avenger_exarch = Model('Dire Avenger Exarch',t=3,w=2,sv=4,guns=[avenger_catapult,avenger_catapult],invuln=5,special=[])
u_dire_avengers = Unit('5 Dire Avengers',[m_dire_avenger]*4 + [m_dire_avenger_exarch],tag='infantry',cost=75)

m_warlock = Model('Warlock',t=3,w=1,sv=6,guns=[destructor,singing_spear],invuln=4,special=[])
u_warlocks = Unit('2 Warlocks', [m_warlock]*2,tag='infantry',cost=55)

m_falcon = Model('Falcon',t=9,w=12,sv=3,guns=[],special=[])
u_falcon = Unit('Falcon',[m_falcon],tag='vehicle',cost=130)

m_fire_prism_dispersed = Model('Fire Prism dispersed',t=9,w=12,sv=3,guns=[prism_cannon_dispersed],special=[])
u_fire_prism_dispersed = Unit('Fire Prism dispersed',[m_fire_prism_dispersed],tag='vehicle',cost=160)

m_fire_prism_focused = Model('Fire Prism focused',t=9,w=12,sv=3,guns=[prism_cannon_focused],special=[])
u_fire_prism_focused = Unit('Fire Prism focused',[m_fire_prism_focused],tag='vehicle',cost=160)

m_lokhust_destroyer = Model('Lokust Destroyer',t=6,w=3,sv=3,guns=[],special=[])
u_lokhust_destroyers = Unit('3 Lokhust Destroyers',[m_lokhust_destroyer]*3,tag='mounted',cost=90)

m_war_walker_starcannons = Model('War Walker with starcannons',t=7,w=6,sv=3,guns=[starcannon]*2,invuln=5,special=[])
u_war_walker_starcannons = Unit('War Walker with starcannons',[m_war_walker_starcannons],tag='vehicle',cost=95)

m_vyper_shuriken_cannon = Model('Vyper with shuriken cannon',t=6,w=6,sv=3,guns=[shuriken_cannon,twin_shuriken_catapult],special=[])
u_vyper_shuriken_cannon = Unit('Vyper with shuriken cannon',[m_vyper_shuriken_cannon],tag='vehicle',cost=65)

m_dark_reaper = Model('Dark Reaper',t=3,w=1,sv=3,guns=[reaper_launcher_starshot],invuln=5,special=[])
m_dark_reaper_exarch = Model('Dark Reaper Exarch',t=3,w=2,sv=3,guns=[reaper_launcher_starshot],invuln=5,special=[])
u_dark_reapers = Unit('5 Dark Reapers',[m_dark_reaper]*4 + [m_dark_reaper_exarch],tag='infantry',cost=90)

m_ranger = Model('Ranger',t=3,w=1,sv=5,guns=[ranger_long_rifle],invuln=5,special=['stealth'])
u_rangers = Unit('5 Rangers',[m_ranger]*5,tag='infantry',cost=55)