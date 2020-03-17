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
		self.role = r			# 0 = Dictator / 1 = Recipient, control variable, not used yet
		self.asp = np.random.uniform(0.0,1.0)
		self.don = end - self.asp
		self.payoff = self.asp 	# ????
		self.my_donations = []
		self.my_aspirations = []

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



class PairEnvironment:
	def __init__(self):
		self.dictator = Individual(0)
		self.recipient = Individual(1)

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


	def swap_roles(self):
		if np.random.randint(0,2): 
			self.dictator, self.recipient = self.recipient, self.dictator 
			#print(" >> Roles swapped")
			'''self.dictator.my_donations.append("SWAP")
			self.recipient.my_donations.append("SWAP")
			self.dictator.my_aspirations.append("SWAP")
			self.recipient.my_aspirations.append("SWAP")'''
		else:
			0
			#print(" > Roles stay equal")


	def get_state(self):
		'''print("dictator donation = ", self.dictator.donation())
		print("recipient donation = ", self.recipient.donation())
		print("dictator aspiration = ", self.dictator.asp)
		print("recipient aspiration = ", self.recipient.asp)
		print("dictator payoff = ", self.dictator.payoff)
		print("recipient payoff = ", self.recipient.payoff)'''
		return self.dictator.donation(), self.dictator.asp, self.recipient.donation(), self.recipient.asp


	def ind_exchange(self, e):
		if np.random.randint(0,2): 
			r = self.recipient
			self.recipient = e.recipient
			e.recipient = r
		else:
			d = self.dictator
			self.dictator = e.dictator
			e.dictator = d
		e.swap_roles()
		self.swap_roles()


# Aquí todo


#########################################################################
#########################################################################
###########       MODEL EXTENSION: ENVIOUS INDIVIDUALS       ############
#########################################################################
#########################################################################

### Creating an environment with N pairs of individuals ###
M = 1000	# number of iterations
IT = M
N = 500	# number of pairs
epsilon = 0.01
pairs = []
for i in range(N):
	pairs.append(PairEnvironment())
envious_donations = []	# List with all the donations for stochastic model
envious_aspirations = []	# List with all the aspirations for stochastic model
envious_prob = 0.1
l = 0.2
h = 0.2
envious_pairs = [1] * int(N * envious_prob) + [0] * int(N * (1 - envious_prob))
random.shuffle(envious_pairs)


while( M > 0 ):
	don_mean = 0.0
	asp_mean = 0.0
	### STEP 1. Each pair make the donation ###
	#print("ITERATION ", M)
	for (p, env) in zip(pairs, envious_pairs):
		#print("*** State previous to the donation ***")
		don_d, asp_d, don_r, asp_r = p.get_state()
		p.dictator.my_donations.append(don_d)		# me interesa la evolución de cada individuo de cada pareja así que todo esto lo guardo
		p.dictator.my_aspirations.append(asp_d)		# idem
		p.recipient.my_donations.append(don_r)		# idem
		p.recipient.my_aspirations.append(asp_r)	# idem
		don_mean += don_r
		asp_mean += asp_r
		if env:
			p.make_envious_donation(l, h, epsilon)
		else:
			p.make_stoch_donation(l, h, epsilon)
		#print("Donation made")
		#print("*** State back to the donation ***")
		#p.get_state()
		#print("-------------------------------------")
	envious_donations.append(don_mean / N)		# todas las donaciones (en cada make_donation() sólo se actualiza la donación del recipient)
	envious_aspirations.append(asp_mean / N)		# todas las aspiraciones (en cada make_donation() sólo se actualiza la aspiración del recipient)

	### STEP 2. Shuffling the pairs and swapping the roles (inside ind_exchange) randomly ###
	exchanges = random.sample(range(N), N)
	index = list(range(N))

	for (i, j) in zip(exchanges, index):
		if (i == j):
			p.swap_roles()
			index.remove(i)
			exchanges.remove(i)
		else:
			pairs[i].ind_exchange(pairs[j])
			exchanges.remove(i)
			index.remove(i)
			exchanges.remove(j)
			index.remove(j)
		#print("* * * * * * * * * * * * * * * * * * * *")
		#print(exchanges)
		#print(index)
	M -= 1


########################################################
######## Donation and aspiration mean evolution ########
########################################################


plt.figure(5)
plt.plot(list(range(IT)), envious_donations)
plt.axis([0, IT, 0, 1])
plt.title("Donations means")
plt.xlabel("Iterations")
plt.ylabel("Donations means")
plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/envious/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(N)+"_mean_don_l_"+str(int(l*10))+"_h_"+str(int(h*10))+".png")
plt.close()


plt.figure(6)
plt.plot(list(range(IT)), envious_aspirations)
plt.axis([0, IT, 0, 1])
plt.title("Aspirations means")
plt.xlabel("Iterations")
plt.ylabel("Aspirations means")
plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/envious/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(N)+"_mean_asp_l_"+str(int(l*10))+"_h_"+str(int(h*10))+".png")
plt.close()


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


