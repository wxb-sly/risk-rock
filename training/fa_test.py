import numpy as np

import matplotlib.pyplot as plt

fa_samples= np.random.normal(loc=35, scale=5, size=5000)

ucs_samples=np.random.normal(loc=50, scale=10, size=5000)

rqd_samples = np.random.normal(loc=70, scale=15, size=5000)

probab_weak = ((ucs_samples<30) & (rqd_samples<50)).mean()
#in numpy neeed to use bitwise and

arr = fa_samples[fa_samples<25]

#print(fa_samples)
#print(arr.mean())

#using mean on a boolean array gives probability
pro = (fa_samples<25).mean()
print(probab_weak)
