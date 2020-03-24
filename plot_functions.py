import matplotlib.pyplot as plt


def means_evolution(nfig, l, h, learn, habit, sp, M, deterministic_donations, deterministic_aspirations, model, epsilon=0.0, envious_prob=0.0, fr=0):
	plt.figure(nfig, figsize=[15,10])
	plt.subplot(len(l), len(h), sp)
	plt.plot(list(range(M)), deterministic_donations, label='donations')
	plt.plot(list(range(M)), deterministic_aspirations, label='aspirations')
	plt.axis([0, M, 0, 1])
	plt.xticks(fontsize='small')
	plt.yticks(fontsize='small')
	if(habit == h[0]): plt.ylabel('l = '+str(learn), family='monospace')
	if(learn == l[0]): plt.title('h = '+str(habit), family='monospace')
	plt.legend(['donations', 'aspirations'], loc="best")
	if( model == 'deterministic' ):
		plt.suptitle("Deterministic model \nDonations and aspirations mean evolution for different values of learning rate and habituation parameter")
	else:
		if( model == 'stochastic' ):
			plt.suptitle("Stochastic model: \u03B5= "+str(epsilon)+"\nDonations and aspirations mean evolution for different values of learning rate and habituation parameter")
		else:
			plt.suptitle("Model extensions: probability of being envious = "+str(envious_prob)+" and "+str(fr)+" free-rider\nDonations and aspirations mean evolution for different values of learning rate and habituation parameter")


def individual_evolution(pairs, nfig, l, h, learn, habit, spi, M, model, epsilon=0.0, envious_prob=0.0, fr=0):
	for p in pairs:
		if(p.is_random_ind()): 
			random_pair = p
	donationsd = random_pair.dictator.my_donations
	aspirationsd = random_pair.dictator.my_aspirations
	plt.figure(nfig, figsize=[15,10])
	plt.subplot(len(l), len(h), spi)
	plt.plot(list(range(M)), donationsd)
	plt.plot(list(range(M)), aspirationsd)
	if(habit == h[0]): plt.ylabel('l = '+str(learn), family='monospace')
	if(learn == l[0]): plt.title('h = '+str(habit), family='monospace')
	plt.axis([0, M, 0, 1])
	plt.legend(['donations', 'aspirations'], loc="best")
	if( model == 'deterministic' ):
		plt.suptitle("Deterministic model \nEvolution of donation and aspiration values for a random individual for different values of learning rate and habituation parameter")
	else:
		if( model == 'stochastic' ):
			plt.suptitle("Stochastic model: \u03B5= "+str(epsilon)+"\nEvolution of donation and aspiration values for a random individual for different values of learning rate and habituation parameter")
		else:
			plt.suptitle("Model extensions: probability of being envious = "+str(envious_prob)+" and "+str(fr)+" free-rider\nEvolution of donation and aspiration values for a random individual for different values of learning rate and habituation parameter")




