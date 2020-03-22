import numpy as np
import random
import matplotlib.pyplot as plt

end = 1.0						# endowment
random.seed(0)
np.random.seed(0)


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
		self.random_ind = False

	def is_envious(self):
		return self.envious

	def is_free_rider(self):
		return self.free_rider

	def is_random_ind(self):
		return self.random_ind

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
		sg = 1 * random.randint(-1, 2)
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

	def set_random_ind(self, b):
		self.dictator.random_ind = b

	def is_random_ind(self):
		return self.dictator.is_random_ind()

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
