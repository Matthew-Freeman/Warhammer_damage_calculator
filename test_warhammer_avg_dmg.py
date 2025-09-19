import unittest
import warhammer_avg_dmg
from units import *
# import weapons

class TestAvgDmg(unittest.TestCase):

	def test_unit_attack(self):
		self.assertAlmostEqual(warhammer_avg_dmg.unit_attack(u_dire_avengers,u_marines,'shooting',verbose=0),6*4*5/6*3/6*3/6*1,3)
		self.assertAlmostEqual(warhammer_avg_dmg.unit_attack(u_vyper_shuriken_cannon,u_marines,'shooting',verbose=0),3 * 3/6 * 4/6 * 3/6 * 2 + 3 * 1/6 * 6/6 * 3/6 * 2 + 2 * 4/6 * 3/4 * 3/6 * 1, 3)
		self.assertAlmostEqual(warhammer_avg_dmg.unit_attack(u_howling_banshees,u_falcon,'fight',verbose=0),4*2 * 5/6 * 1/6 * 4/6 * 2 + 3 * 5/6 * 2/6 * 5/6 * 3, 3)
		self.assertAlmostEqual(warhammer_avg_dmg.unit_attack(u_warlock_conclave,u_marines,'shooting',verbose=0),4 * 5.5 * 1 * 4/6 * 3/6 * 1 + 5 * 1 * 5/6 * 5/6 * 2/6 *2 + 1*4.5*5/6*4/6*4/6*5/3, 3)
		self.assertAlmostEqual(warhammer_avg_dmg.unit_attack(u_howling_banshees,u_marines,'fight',verbose=0),4* 2 * 5/6 * 4/6 * 4/6 * 2 + 3*5/6*4/6*5/6*2, 3)
		self.assertAlmostEqual(warhammer_avg_dmg.unit_attack(u_fire_dragons,u_falcon,'shooting',verbose=0),4*8/9*3/4*1*(6.5+6.5+6.5+7+8+9)/6 + 1*8/9*8/9*1*(6.5+6.5+6.5+7+8+9)/6, 3)

if __name__ == '__main__':
	unittest.main()