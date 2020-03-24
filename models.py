import numpy as np
import random
from environment import Individual, PairEnvironment


def create_pairs(N, randomp):
	pairs = []
	for i in range(N):
		pairs.append(PairEnvironment())
		if( i == randomp ):
			pairs[i].set_random_ind(True)
	return pairs


#########################################################################
#########################################################################
###########                DETERMINISTIC MODEL                ###########
#########################################################################
#########################################################################


def deterministic(learn, habit, M, N, pairs):
	deterministic_donations = []	# List with all the donations for deterministic model
	deterministic_aspirations = []	# List with all the aspirations for deterministic model
	while( M > 0 ):
		don_mean = 0.0
		asp_mean = 0.0

		### STEP 1. Each pair make the donation ###
		for p in pairs:
			don_d, asp_d, don_r, asp_r = p.get_state(False)
			p.dictator.my_donations.append(don_d)		# me interesa la evolución de cada individuo de cada pareja así que todo esto lo guardo
			p.dictator.my_aspirations.append(asp_d)		# idem
			p.recipient.my_donations.append(don_r)		# idem
			p.recipient.my_aspirations.append(asp_r)	# idem
			don_mean += don_r
			asp_mean += asp_r
			p.make_donation(learn, habit)
		deterministic_donations.append(don_mean / N)		# todas las donaciones (en cada make_donation() sólo se actualiza la donación del recipient)
		deterministic_aspirations.append(asp_mean / N)		# todas las aspiraciones (en cada make_donation() sólo se actualiza la aspiración del recipient)

		### STEP 2. Shuffling the pairs and swapping the roles (inside ind_exchange) randomly ###
		exchanges = random.sample(range(N), N)
		index = list(range(N))
		for (i, j) in zip(exchanges, index):
			if (i == j):
				pairs[i].swap_roles()
				index.remove(i)
				exchanges.remove(i)
			else:
				pairs[i].ind_exchange(pairs[j])
				exchanges.remove(i)
				index.remove(i)
				exchanges.remove(j)
				index.remove(j)

		M -= 1
		### We go to STEP 1 again ###

	return pairs, deterministic_donations, deterministic_aspirations



#########################################################################
#########################################################################
############                STOCHASTIC MODEL                #############
#########################################################################
#########################################################################

def stochastic(learn, habit, M, N, pairs, epsilon):
	stochastic_donations = []	# List with all the donations for stochastic model
	stochastic_aspirations = []	# List with all the aspirations for stochastic model

	while( M > 0 ):
		don_mean = 0.0
		asp_mean = 0.0

		### STEP 1. Each pair make the donation ###
        
		for p in pairs:
			don_d, asp_d, don_r, asp_r = p.get_state(False)
			p.dictator.my_donations.append(don_d)		# me interesa la evolución de cada individuo de cada pareja así que todo esto lo guardo
			p.dictator.my_aspirations.append(asp_d)		# idem
			p.recipient.my_donations.append(don_r)		# idem
			p.recipient.my_aspirations.append(asp_r)	# idem
			don_mean += don_r
			asp_mean += asp_r
			p.make_stoch_donation(learn, habit, epsilon)
		stochastic_donations.append(don_mean / N)		# todas las donaciones (en cada make_donation() sólo se actualiza la donación del recipient)
		stochastic_aspirations.append(asp_mean / N)		# todas las aspiraciones (en cada make_donation() sólo se actualiza la aspiración del recipient)

		### STEP 2. Shuffling the pairs and swapping the roles (inside ind_exchange) randomly ###
		exchanges = random.sample(range(N), N)
		index = list(range(N))

		for (i, j) in zip(exchanges, index):
			if (i == j):
				pairs[i].swap_roles()
				index.remove(i)
				exchanges.remove(i)
			else:
				pairs[i].ind_exchange(pairs[j])
				exchanges.remove(i)
				index.remove(i)
				exchanges.remove(j)
				index.remove(j)

		M -= 1

		### We go to STEP 1 again ###

	return pairs, stochastic_donations, stochastic_aspirations



#########################################################################
#########################################################################
####      MODEL EXTENSION: ENVIOUS INDIVIDUALS AND FREE_RIDERS       ####
#########################################################################
#########################################################################


def extension(learn, habit, M, N, pairs, epsilon, envious_prob, fr):
	extension_donations = []		# List with all the donations for stochastic model
	extension_aspirations = []	# List with all the aspirations for stochastic model


	## Changing the individuals making them have a probability of being envious ##
	envious_pairs = [1] * int(N * envious_prob) + [0] * int(N * (1 - envious_prob))
	random.shuffle(envious_pairs)
	for (env, p) in zip(envious_pairs, pairs):
		if env:
			p.set_envious(True)

	## Changing the individuals making them have a concrete number of free-riders ##
	free_rider = []
	for i in range(fr):
		free_rider.append(random.randint(0, N-1))

	for i in free_rider:
		pairs[i].set_free_rider(True) # IndexError: list index out of range !!


	while( M > 0 ):
		don_mean = 0.0	# in every iteration we calculate the mean of all the donations
		asp_mean = 0.0	# in every iteration we calculate the mean of all the aspirations

		### STEP 1. Each pair make the donation ###
		for p in pairs:
			don_d, asp_d, don_r, asp_r = p.get_state(False)
			p.dictator.my_donations.append(don_d)		# me interesa la evolución de cada individuo de cada pareja así que todo esto lo guardo
			p.dictator.my_aspirations.append(asp_d)		# idem
			p.recipient.my_donations.append(don_r)		# idem
			p.recipient.my_aspirations.append(asp_r)	# idem
			don_mean += don_r
			asp_mean += asp_r
			## if the dictator is a free-rider, make a free-rider donation ##
			if p.is_free_rider():
				p.make_freerider_donation(learn, habit, epsilon)
			else:
				## else, if the dictator is envious, make an envious donation ##
				if p.is_envious():
					p.make_envious_donation(learn, habit, epsilon)
				## else, make an stochastic donation ##
				else:
					p.make_stoch_donation(learn, habit, epsilon)

		extension_donations.append(don_mean / N)		# todas las donaciones (en cada make_donation() sólo se actualiza la donación del recipient)
		extension_aspirations.append(asp_mean / N)		# todas las aspiraciones (en cada make_donation() sólo se actualiza la aspiración del recipient)

		### STEP 2. Shuffling the pairs and swapping the roles (inside ind_exchange) randomly ###
		exchanges = random.sample(range(N), N)
		index = list(range(N))

		for (i, j) in zip(exchanges, index):
			if (i == j):
				pairs[i].swap_roles()
				index.remove(i)
				exchanges.remove(i)
			else:
				pairs[i].ind_exchange(pairs[j])
				exchanges.remove(i)
				index.remove(i)
				exchanges.remove(j)
				index.remove(j)
		M -= 1

		### We go to STEP 1 again ###

	return pairs, extension_donations, extension_aspirations





