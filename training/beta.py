import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

rqd_low = np.random.beta(a=6, b=4, size =1000)

#topercent
rqd_low =rqd_low * 100

plt.hist(rqd_low, bins=50, density=True, alpha=0.5, label="1m Drill Run")

plt.savefig('lowe.png')
print("done")

rqd_high_evidence = np.random.beta(a=600, b=400, size=10000) * 100

plt.hist(rqd_high_evidence, bins=50, density=True, alpha=0.5, label="100m Drill Run")
plt.axvline(60, color='k', linestyle='dashed', label="Mean (60%)")
plt.title("Beta Distribution: RQD Uncertainty")
plt.legend()
plt.savefig('high.png')
print("done2")

