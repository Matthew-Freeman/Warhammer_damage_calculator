import math



	# for non-independent attacks, like the fire prism's "reroll one hit and wound out of the two"
	# hit chance = 4/6 = 2/3
	# avg number of hits?
	# 2
	#  HH = 2 * 2/3*2/3 = 24/27 hits
	#  HMH = 2 * 2/3*1/3*2/3 = 8/27 hits
	#  HMM = 1 * 2/3*1/3*1/3 = 2/27
	#  MHH                   = 8/27
	#  MHM                   = 2/27
	#  MMH                   = 2/27
	#  MMM                   = 0
	#  = 46/27 = 1.7037 hits per phase
	#  fire 3 shots but subtract the 3 hit case 
	#  3 * 2/3 - 8/27 = 2 - 8/27 = 54/27 - 8/27 = 46/27
	#  For n shots, rerolling one miss:
	#  expected hits = n+1 * p_hit - p_hit^(n+1)
	#  But then there's more branching for the wound roll.
	# Hit Miss Wound Fail
	# HH  WW
	# HH  WFW
	# HH  FWW
	# HH  WFF
	# HH  FWF
	# HH  FFW
	# HH  FFF
	# 49 cases? No, 31

	# HMH WW
	# HMH WFW
	# HMH FWW
	# HMH WFF
	# HMH FWF
	# HMH FFW
	# HMH FFF

	# MHH WW
	# MHH WFW
	# MHH FWW
	# MHH WFF
	# MHH FWF
	# MHH FFW
	# MHH FFF

	# HMM W 
	# HMM	FW
	# HMM	FF

	# MHM W 
	# MHM FW
	# MHM FF

	# MMH W 
	# MMH FW
	# MMH FF

	# MMM F

	#A recursive function?!
	# n attacks with 1 reroll.
	# n successes
	# n-1 successes
	# n-2 successes.  Use the choose function?
	# next step, use the number of successes for the next step.
	#return probability and number of successes.


def hits_with_1_reroll(n,p_hit,r,probability,wound_probabilities,p_wound):
	#takes in some number n of attempts, with probability p of success, and number r of rerolls available. Start with r = 1.
	for successes in range(n+r,-1,-1):
		current_probability = probability * p_hit**successes * (1-p_hit)**(n+r-successes) * n_choose_k(n+r,successes)
		actual_successes = min(successes,n)
		print("Probability of {} successes = {}".format(actual_successes,current_probability))
		
		wounds_with_1_reroll(actual_successes,p_wound,r,current_probability,wound_probabilities)


def wounds_with_1_reroll(n,p_wound,r,probability,wound_probabilities):
	for successes in range(n+r,-1,-1):
		current_probability = probability * p_wound**successes * (1-p_wound)**(n+r-successes) * n_choose_k(n+r,successes)
		actual_successes = min(successes,n)
		print("Probability of {} successes = {}".format(actual_successes,current_probability))
		wound_probabilities[actual_successes] += current_probability

def n_choose_k(n,k):
	return math.factorial(n) / (math.factorial(k)*math.factorial(n-k))


shots = 2
p_hit = 4/6
p_wound = 5/6
rerolls = 1
# depth = 1
# wound_probabilities = {"2":0,"1":0,"0":0}
probability = 1
wound_probabilities = [0]*(shots+1)
hits_with_1_reroll(shots,p_hit,rerolls,probability,wound_probabilities,p_wound)
print('wound_probabilities',wound_probabilities)
print('total probabilty =',sum(wound_probabilities))
expected_wounds = sum([i * wound_probabilities[i] for i in range(shots+1)])
print('Expected wounds = {}'.format(expected_wounds))
print(2*8/9)
print(1/81,p_hit*(1-p_hit)**3)

# Ah, my calculation allows rerolling one shot twice. Oops.
#A hit or two misses ends a dice. 
#HMMH not allowed
#MMMM allowed
#HMHM effectively allowed because the last doesn't matter?
#Allowed 1 hit options: HMM, MHMM, MMH,MMMH 
#Some 2 hits are actually 1 hit
#HMMH.
#MMHH
#1 hits and 3 hits work.

#how to extend this to more shots, or more rerolls?
# 3 shots, 2 rerolls
# 3 hits:
# MHMHH works
# MMHHH doesn't
# HMMHH doesn't
# HHMMH doesn't
# HHHMM does
# # All sequences with a double miss that isn't in the last place. n+r-2 or n chose k?
# 2 hits:
# MMMHH works
# MMHHM works
# MHHHM works
# 1 hit works  

#Is a problem when I use all my dice, without using all my rerolls. one more dice, so 3. 
# hard to see the pattern here.
#Can I just alter my n chose k algorithm? 
#can't use p_hit on the second depth. Its a wound roll.




# print(n_choose_k(3,0))
# print(n_choose_k(3,1))
# print(n_choose_k(3,2))
# print(n_choose_k(3,3))
# print(n_choose_k(4,0))
# print(n_choose_k(4,1))
# print(n_choose_k(4,2))
# print(n_choose_k(4,3))
# print(n_choose_k(4,4))

