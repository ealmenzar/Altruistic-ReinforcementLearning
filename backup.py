#########################################################################
#########################################################################
###########                DETERMINISTIC MODEL                ###########
#########################################################################
#########################################################################

### Creating an environment with N pairs of individuals ###
M = 1000	# number of iterations
IT = M
N = 504	# number of pairs
pairs = []
for i in range(N):
	pairs.append(PairEnvironment())
deterministic_donations = []	# List with all the donations for deterministic model
deterministic_aspirations = []	# List with all the aspirations for deterministic model
l = 0.2
h = 0.8

while( M > 0 ):
	don_mean = 0.0
	asp_mean = 0.0

	### STEP 1. Each pair make the donation ###
	for p in pairs:
		#print("*** State previous to the donation ***")
		don_d, asp_d, don_r, asp_r = p.get_state()
		p.dictator.my_donations.append(don_d)		# me interesa la evolución de cada individuo de cada pareja así que todo esto lo guardo
		p.dictator.my_aspirations.append(asp_d)		# idem
		p.recipient.my_donations.append(don_r)		# idem
		p.recipient.my_aspirations.append(asp_r)	# idem
		don_mean += don_r
		asp_mean += asp_r
		p.make_donation(l, h)
	deterministic_donations.append(don_mean / N)		# todas las donaciones (en cada make_donation() sólo se actualiza la donación del recipient)
	deterministic_aspirations.append(asp_mean / N)		# todas las aspiraciones (en cada make_donation() sólo se actualiza la aspiración del recipient)

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
	M -= 1

	### We go to STEP 1 again ###
'''

########################################################
### Donation and aspiration evolution per individual ###
########################################################

fi = 0
for p in pairs:
	plt.figure(1)
	plt.plot(list(range(IT)), p.dictator.my_donations)
	plt.axis([0, IT, 0, 1])
	plt.title("Individual "+str(fi)+" donations")
	plt.xlabel("Iterations")
	plt.ylabel("Donations")
	plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/deterministic/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(fi)+"_l_"+str(int(l*10))+"_h_"+str(int(h*10))+"_don.png")
	plt.close()
	plt.figure(2)
	plt.plot(list(range(IT)), p.dictator.my_aspirations)
	plt.axis([0, IT, 0, 1])
	plt.title("Individual "+str(fi)+" aspirations")
	plt.xlabel("Iterations")
	plt.ylabel("Aspirations")
	plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/deterministic/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(fi)+"_l_"+str(int(l*10))+"_h_"+str(int(h*10))+"_asp.png")
	plt.close()
	fi += 1
	plt.figure(3)
	plt.plot(list(range(IT)), p.recipient.my_donations)
	plt.axis([0, IT, 0, 1])
	plt.title("Individual "+str(fi)+" donations")
	plt.xlabel("Iterations")
	plt.ylabel("Donations")
	plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/deterministic/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(fi)+"_l_"+str(int(l*10))+"_h_"+str(int(h*10))+"_don.png")
	plt.close()
	plt.figure(4)
	plt.plot(list(range(IT)), p.recipient.my_aspirations)
	plt.axis([0, IT, 0, 1])
	plt.title("Individual "+str(fi)+" aspirations")
	plt.xlabel("Iterations")
	plt.ylabel("Aspirations")
	plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/deterministic/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(fi)+"_l_"+str(int(l*10))+"_h_"+str(int(h*10))+"_asp.png")
	plt.close()
	fi += 1

'''
########################################################
######## Donation and aspiration mean evolution ########
########################################################


plt.figure(5)
plt.plot(list(range(IT)), deterministic_donations)
plt.axis([0, IT, 0, 1])
plt.title("Donations means")
plt.xlabel("Iterations")
plt.ylabel("Donations means")
plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/deterministic/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(N)+"_mean_don_l_"+str(int(l*10))+"_h_"+str(int(h*10))+".png")
plt.close()


plt.figure(6)
plt.plot(list(range(IT)), deterministic_aspirations)
plt.axis([0, IT, 0, 1])
plt.title("Aspirations means")
plt.xlabel("Iterations")
plt.ylabel("Aspirations means")
plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/deterministic/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(N)+"_mean_asp_l_"+str(int(l*10))+"_h_"+str(int(h*10))+".png")
plt.close()





#########################################################################
#########################################################################
#############               STOCHASTIC MODEL                #############
#########################################################################
#########################################################################


### Creating an environment with N pairs of individuals ###
M = 200	# number of iterations
IT = M
N = 502	# number of pairs
epsilon = 0.01
pairs = []
for i in range(N):
	pairs.append(PairEnvironment())
stochastic_donations = []	# List with all the donations for stochastic model
stochastic_aspirations = []	# List with all the aspirations for stochastic model
l = 0.2
h = 0.2

while( M > 0 ):
	don_mean = 0.0
	asp_mean = 0.0
	### STEP 1. Each pair make the donation ###
	#print("ITERATION ", M)
	for p in pairs:
		#print("*** State previous to the donation ***")
		don_d, asp_d, don_r, asp_r = p.get_state()
		p.dictator.my_donations.append(don_d)		# me interesa la evolución de cada individuo de cada pareja así que todo esto lo guardo
		p.dictator.my_aspirations.append(asp_d)		# idem
		p.recipient.my_donations.append(don_r)		# idem
		p.recipient.my_aspirations.append(asp_r)	# idem
		don_mean += don_r
		asp_mean += asp_r
		p.make_stoch_donation(l, h, epsilon)
		#print("Donation made")
		#print("*** State back to the donation ***")
		#p.get_state()
		#print("-------------------------------------")
	stochastic_donations.append(don_mean / N)		# todas las donaciones (en cada make_donation() sólo se actualiza la donación del recipient)
	stochastic_aspirations.append(asp_mean / N)		# todas las aspiraciones (en cada make_donation() sólo se actualiza la aspiración del recipient)

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
plt.plot(list(range(IT)), stochastic_donations)
plt.axis([0, IT, 0, 1])
plt.title("Donations means")
plt.xlabel("Iterations")
plt.ylabel("Donations means")
plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/stochastic/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(N)+"_mean_don_l_"+str(int(l*10))+"_h_"+str(int(h*10))+".png")
plt.close()


plt.figure(6)
plt.plot(list(range(IT)), stochastic_aspirations)
plt.axis([0, IT, 0, 1])
plt.title("Aspirations means")
plt.xlabel("Iterations")
plt.ylabel("Aspirations means")
plt.savefig("/Users/marina/Documents/UPF/Master/2/SDIC/RL/proyecto/stochastic/l_"+str(int(l*10))+"_h_"+str(int(h*10))+"/"+str(N)+"_mean_asp_l_"+str(int(l*10))+"_h_"+str(int(h*10))+".png")
plt.close()



