import numpy as np
import random
import matplotlib.pyplot as plt

end = 1.0						# endowment
random.seed(0)
np.random.seed(0)
#l = np.random.uniform(0.0,1.0)	# learning rate
#h = np.random.uniform(0.0,1.0)	# habituation parameter



class Individual:
	def __init__(self, r):
		#self.role = r			# 0 = Dictator / 1 = Recipient, control variable, not used yet
		self.asp = np.random.uniform(0.0,1.0)
		self.don = end - self.asp
		self.payoff = self.asp 	# ????
		self.my_donations = []
		self.my_aspirations = []
		self.envious = False
		self.free_rider = False

	def is_envious(self):
		return self.envious

	def is_free_rider(self):
		return self.free_rider

	def update_role(self, r):
		self.r = r

	### Recipient methods ###

	def stimuli(self, d, a):
		s = (d - self.asp) # / (end - a) if end != a else 0		## ERROR? no need to normalization
		return s

	def update_asp(self, s, l):
		new_asp = self.asp + (end - self.asp)*l*s if s >= 0 else self.asp*(1 + l*s)
		self.asp = new_asp
		return new_asp

	def update_payoff(self, don):
		self.payoff = don

	### Dictator methods ###

	def calculate_don(self, h):
		don_0 = (1 - h) * self.don + h * self.payoff
		# the donation cannot exceed the amount resulting from substracting
		# the aspiration of the individual from the endowment
		new_don = np.maximum(0.0, np.minimum(don_0, end-self.asp))
		self.don = new_don

	def calculate_stoch_don(self, h, ep):
		don_0 = (1 - h) * self.don + h * self.payoff
		# the donation cannot exceed the amount resulting from substracting
		# the aspiration of the individual from the endowment
		new_don = np.maximum(0.0, np.minimum(don_0, end-self.asp))
		sg = random.randint(-1, 2)
		self.don = (1 + sg * ep) * new_don

	def calculate_envious_don(self, h, ep):
		don_0 = (1 - h) * self.don + h * self.payoff
		# the donation cannot exceed the amount resulting from substracting
		# the aspiration of the individual from the endowment
		new_don = np.maximum(0.0, np.minimum(don_0, end-self.asp))
		sg = random.randint(-1, 2)
		new_don = (1 + sg * ep) * new_don
		self.don = np.minimum(new_don, 0.5)


	def donation(self):
		return self.don


	def features_exchange(self, ind):
		copyd = self.don
		self.don = ind.don
		ind.don = copyd
		copya = self.asp
		self.asp = ind.asp
		ind.asp = copya
		copyp = self.payoff
		self.payoff = ind.payoff
		ind.payoff = copyp

		copyd, copya = self.my_donations, self.my_aspirations
		self.my_donations, self.my_aspirations = ind.my_donations, ind.my_aspirations
		ind.my_donations, ind.my_aspirations = copyd, copya

		copyd, copya = self.envious, self.free_rider
		self.envious, self.free_rider = ind.envious, ind.free_rider
		ind.envious, ind.free_rider = copyd, copya



class PairEnvironment:
	def __init__(self):
		self.dictator = Individual(0)
		self.recipient = Individual(1)

	def set_envious(self, b):
		self.dictator.envious = b

	def set_free_rider(self, b):
		self.dictator.free_rider = b

	def is_envious(self):
		return self.dictator.is_envious()

	def is_free_rider(self):
		return self.dictator.is_free_rider()

	def make_donation(self, l, h):
		# we get the donation from the dictator:
		donation = self.dictator.donation()
		# we compute the stimuli and update the aspiration for the recipient:
		#print("####### stimuli = ", self.recipient.stimuli(donation, self.dictator.asp))
		self.recipient.update_asp(self.recipient.stimuli(donation, self.dictator.asp), l)
		# we update the payoff for the recipient:
		self.recipient.update_payoff(donation)
		# we compute the next donation for the dictator:
		#self.dictator.calculate_don()
		# we compute the next donation for the recipient:
		self.recipient.calculate_don(h)


	def make_stoch_donation(self, l, h, ep):
		# we get the donation from the dictator:
		donation = self.dictator.donation()
		# we compute the stimuli and update the aspiration for the recipient:
		#print("####### stimuli = ", self.recipient.stimuli(donation, self.dictator.asp))
		self.recipient.update_asp(self.recipient.stimuli(donation, self.dictator.asp), l)
		# we update the payoff for the recipient:
		self.recipient.update_payoff(donation)
		# we compute the next donation for the dictator:
		#self.dictator.calculate_don()
		# we compute the next donation for the recipient:
		self.recipient.calculate_stoch_don(h, ep)


	def make_envious_donation(self, l, h, ep):
		# we get the donation from the dictator:
		donation = self.dictator.donation()
		# we compute the stimuli and update the aspiration for the recipient:
		#print("####### stimuli = ", self.recipient.stimuli(donation, self.dictator.asp))
		self.recipient.update_asp(self.recipient.stimuli(donation, self.dictator.asp), l)
		# we update the payoff for the recipient:
		self.recipient.update_payoff(donation)
		# we compute the next donation for the dictator:
		#self.dictator.calculate_don()
		# we compute the next donation for the recipient:
		self.recipient.calculate_envious_don(h, ep)


	def make_freerider_donation(self, l, h, ep):
		# we get the donation from the dictator:
		donation = 0.0
		# we compute the stimuli and update the aspiration for the recipient:
		#print("####### stimuli = ", self.recipient.stimuli(donation, self.dictator.asp))
		self.recipient.update_asp(self.recipient.stimuli(donation, self.dictator.asp), l)
		# we update the payoff for the recipient:
		self.recipient.update_payoff(donation)
		# the dictator does not update its donation (?):
		#self.dictator.calculate_don()
		# we compute the next donation for the recipient:
		self.recipient.don = 0.0


	def swap_roles(self):
		if np.random.randint(0,2):
			'''if(self.is_free_rider()):
				fr = True 
				print(" >> Roles swapped")
				print("dictator donation = ", self.dictator.don)
				print("recipient donation = ", self.recipient.don)
				print("dictator aspiration = ", self.dictator.asp)
				print("recipient aspiration = ", self.recipient.asp)
			else:
				fr = False'''

			self.dictator.features_exchange(self.recipient)
			#self.dictator, self.recipient = self.recipient, self.dictator 
			'''
			if fr:
				print("- - - - -")
				print("dictator donation = ", self.dictator.don)
				print("recipient donation = ", self.recipient.don)
				print("dictator aspiration = ", self.dictator.asp)
				print("recipient aspiration = ", self.recipient.asp)'''
		else:
			0
			#print(" > Roles stay equal")


	def get_state(self, b):
		if b:
			print("dictator donation = ", self.dictator.donation())
			print("recipient donation = ", self.recipient.donation())
			print("dictator aspiration = ", self.dictator.asp)
			print("recipient aspiration = ", self.recipient.asp)
			print("dictator payoff = ", self.dictator.payoff)
			print("recipient payoff = ", self.recipient.payoff)
		return self.dictator.donation(), self.dictator.asp, self.recipient.donation(), self.recipient.asp


	def ind_exchange(self, e):
		if np.random.randint(0,2):
			self.recipient.features_exchange(e.recipient) 
			'''r = self.recipient
			self.recipient = e.recipient
			e.recipient = r'''
		else:
			self.dictator.features_exchange(e.dictator)
			'''d = self.dictator
			self.dictator = e.dictator
			e.dictator = d'''
		e.swap_roles()
		self.swap_roles()





#########################################################################
#########################################################################
###########                DETERMINISTIC MODEL                ###########
#########################################################################
#########################################################################

'''
l = [0.2, 0.4, 0.6, 0.8]
h = [0.2, 0.4, 0.6, 0.8]
spd = 1
spa = 1
for learn in l:
	for habit in h:
		### Creating an environment with N pairs of individuals ###
		M = 50	# number of iterations
		IT = M
		N = 500	# number of pairs
		pairs = []
		for i in range(N):
			pairs.append(PairEnvironment())

		deterministic_donations = []	# List with all the donations for deterministic model
		deterministic_aspirations = []	# List with all the aspirations for deterministic model
		while( M > 0 ):
			don_mean = 0.0
			asp_mean = 0.0

			### STEP 1. Each pair make the donation ###
			for p in pairs:
				#print("*** State previous to the donation ***")
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


########################################################
##########      Donation mean evolution      ###########
########################################################
		plt.figure(1)
		plt.subplot(4, 4, spd)
		spd += 1
		plt.plot(list(range(IT)), deterministic_donations)
		plt.axis([0, IT, 0, 1])
		plt.xticks(fontsize='xx-small')
		plt.yticks(fontsize='xx-small')
		plt.text(IT*0.75, 0.76,'l = '+str(learn)+'\nh = '+str(habit),
			{'color': 'b', 'fontsize': 'x-small',
			'bbox': dict(boxstyle="square", fc="white", ec="black", pad=0.25, alpha=0.5)}, family='monospace')	
		plt.suptitle("Deterministic model \nDonations mean evolution for different values of learning rate and habituation parameter", size='medium')	


########################################################
#########      Aspiration mean evolution      ##########
########################################################

		plt.figure(2)
		plt.subplot(4, 4, spa)
		spa += 1
		plt.plot(list(range(IT)), deterministic_aspirations)
		plt.axis([0, IT, 0, 1])
		plt.xticks(fontsize='xx-small')
		plt.yticks(fontsize='xx-small')
		plt.text(IT*0.75, 0.76,'l = '+str(learn)+'\nh = '+str(habit),
			{'color': 'b', 'fontsize': 'x-small',
			'bbox': dict(boxstyle="square", fc="white", ec="black", pad=0.25, alpha=0.5)}, family='monospace')	
		plt.suptitle("Deterministic model \nAspirations mean evolution for different values of learning rate and habituation parameter", size='medium')	
		

plt.show()


#########################################################################
#########################################################################
#############               STOCHASTIC MODEL                #############
#########################################################################
#########################################################################

l = [0.2, 0.4, 0.6, 0.8]
h = [0.2, 0.4, 0.6, 0.8]
spd = 1
spa = 1
for learn in l:
	for habit in h:
		### Creating an environment with N pairs of individuals ###
		M = 50	# number of iterations
		IT = M
		N = 500	# number of pairs
		epsilon = 0.1
		pairs = []
		for i in range(N):
			pairs.append(PairEnvironment())
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


########################################################
##########      Donation mean evolution      ###########
########################################################
		plt.figure(1)
		plt.subplot(4, 4, spd)
		spd += 1
		plt.plot(list(range(IT)), stochastic_donations)
		plt.axis([0, IT, 0, 1])
		plt.xticks(fontsize='xx-small')
		plt.yticks(fontsize='xx-small')
		plt.text(IT*0.75, 0.75,'l = '+str(learn)+'\nh = '+str(habit),
			{'color': 'b', 'fontsize': 'x-small',
			'bbox': dict(boxstyle="square", fc="white", ec="black", pad=0.25, alpha=0.5)}, family='monospace')	
		plt.suptitle("Stochastic model \nDonations mean evolution for different values of learning rate and habituation parameter\n\u03B5=0.01", size='medium')	


########################################################
#########      Aspiration mean evolution      ##########
########################################################

		plt.figure(2)
		plt.subplot(4, 4, spa)
		spa += 1
		plt.plot(list(range(IT)), stochastic_aspirations)
		plt.axis([0, IT, 0, 1])
		plt.xticks(fontsize='xx-small')
		plt.yticks(fontsize='xx-small')
		plt.text(IT*0.75, 0.75,'l = '+str(learn)+'\nh = '+str(habit),
			{'color': 'b', 'fontsize': 'x-small',
			'bbox': dict(boxstyle="square", fc="white", ec="black", pad=0.25, alpha=0.5)}, family='monospace')	
		plt.suptitle("Stochastic model \nAspirations mean evolution for different values of learning rate and habituation parameter\n\u03B5=0.01", size='medium')	
		

plt.show()

'''

#########################################################################
#########################################################################
####      MODEL EXTENSION: ENVIOUS INDIVIDUALS AND FREE_RIDERS       ####
#########################################################################
#########################################################################


l = [0.2, 0.4, 0.6, 0.8]	# learning rate
h = [0.2, 0.4, 0.6, 0.8]	# habituation parameter
spd = 1
spa = 1
for learn in l:
	for habit in h:
		### Creating an environment with N pairs of individuals ###
		M = 100		# number of iterations
		IT = M 			# auxiliar value
		N = 500			# number of pairs
		epsilon = 0.1	# trembling hand
		pairs = []		# list of pairs
		fr = 50			# number of free-riders

		for i in range(N):
			pairs.append(PairEnvironment())
		envious_donations = []		# List with all the donations for stochastic model
		envious_aspirations = []	# List with all the aspirations for stochastic model
		envious_prob = 0.05			# probability of being envious


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
			#cnt = 0

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
				#cnt += 1
				
			envious_donations.append(don_mean / N)		# todas las donaciones (en cada make_donation() sólo se actualiza la donación del recipient)
			envious_aspirations.append(asp_mean / N)	# todas las aspiraciones (en cada make_donation() sólo se actualiza la aspiración del recipient)

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

########################################################
##########      Donation mean evolution      ###########
########################################################
		plt.figure(1)
		plt.subplot(4, 4, spd)
		spd += 1
		plt.plot(list(range(IT)), envious_donations)
		plt.axis([0, IT, 0, 1])
		plt.xticks(fontsize='xx-small')
		plt.yticks(fontsize='xx-small')
		plt.text(IT*0.75, 0.75,'l = '+str(learn)+'\nh = '+str(habit),
			{'color': 'b', 'fontsize': 'x-small',
			'bbox': dict(boxstyle="square", fc="white", ec="black", pad=0.25, alpha=0.5)}, family='monospace')	
		plt.suptitle("Model extension: Stochastic + envious individuals \nDonations mean evolution for different values of learning rate and habituation parameter\n\u03B5="+str(epsilon)+"\n"+str(fr)+" free-riders", size='medium')	


########################################################
#########      Aspiration mean evolution      ##########
########################################################

		plt.figure(2)
		plt.subplot(4, 4, spa)
		spa += 1
		plt.plot(list(range(IT)), envious_aspirations)
		plt.axis([0, IT, 0, 1])
		plt.xticks(fontsize='xx-small')
		plt.yticks(fontsize='xx-small')
		plt.text(IT*0.75, 0.75,'l = '+str(learn)+'\nh = '+str(habit),
			{'color': 'b', 'fontsize': 'x-small',
			'bbox': dict(boxstyle="square", fc="white", ec="black", pad=0.25, alpha=0.5)}, family='monospace')	
		plt.suptitle("Model extension: Stochastic + envious individuals \nAspirations mean evolution for different values of learning rate and habituation parameter\n\u03B5="+str(epsilon)+"\n"+str(fr)+" free-riders", size='medium')	
		

plt.show()


'''
for p in pairs:
	plt.figure(7)
	plt.plot(list(range(IT)), p.recipient.my_donations)
	plt.axis([0, IT, 0, 1])
	plt.title("All recipients donations")
	plt.xlabel("Iterations")
	plt.ylabel("Donations")
plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/deterministic/r_don_total.png")
plt.close()

for p in pairs:
	plt.figure(8)
	plt.plot(list(range(IT)), p.recipient.my_aspirations)
	plt.axis([0, IT, 0, 1])
	plt.title("All recipients aspirations")
	plt.xlabel("Iterations")
	plt.ylabel("Aspirations")
plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/deterministic/r_asp_total.png")
plt.close()
'''


''' Checking donations and swap '''
'''print("*** State previous to the donation ***")
e = PairEnvironment()
e.get_state()
e.make_donation()
print("Donation made")
print("*** State back to the donation ***")	
e.get_state()
e.swap_roles()
print("*** State previous to the donation ***")
e.get_state()
e.make_donation()
print("Donation made")
print("*** State back to the donation ***")	
e.get_state()
e.swap_roles()
print("*** State previous to the donation ***")
e.get_state()
e.make_donation()
print("Donation made")
print("*** State back to the donation ***")	
e.get_state()'''

''' Checking individuals exchange '''
'''
print(pairs)
print("*** State previous to the exchange ***")
e1 = PairEnvironment()
print("* e1:")
e1.get_state()
print("* e2:")
e2 = PairEnvironment()
e2.get_state()
print("*** State back to the exchange ***")
e1.ind_exchange(e2)
print("* e1:")
e1.get_state()
print("* e2:")
e2.get_state()'''



'''
NEGATIVE ASPIRATION??? (payoff initialized to 0)

ITERATION  2
*** State previous to the donation ***
dictator donation =  0.4298710027277891
recipient donation =  0.12718356204432146
dictator aspiration =  0.45636807828406056
recipient aspiration =  0.8728164379556785
dictator payoff =  0.45490537294224387
recipient payoff =  0.9442259488448976
--------stimuli =  -3.482725504051616
Donation made
*** State back to the donation ***
dictator donation =  0.4474305646836651
recipient donation =  0.3394940305089121
dictator aspiration =  0.45636807828406056
recipient aspiration =  -1.9123120425744171
dictator payoff =  0.45490537294224387
recipient payoff =  0.4298710027277891
-------------------------------------
'''


