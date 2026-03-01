import numpy as np
import matplotlib.pyplot as plt

#lamda = expected rate

rpk = np.random.poisson(lam=2, size = 1000)
#rockburst per km

bins = np.arange(0, rpk.max() + 1.5) - 0.5
plt.hist(rpk, bins=bins, density=True, alpha=0.7, color='r', edgecolor='black')
plt.title("Poisson Distribution: Rockbursts per km ($lambda=2$)")
plt.xlabel("Number of Rockbursts")
plt.ylabel("Probability")
plt.xticks(range(0, rpk.max() + 1))
plt.savefig("poisson")

