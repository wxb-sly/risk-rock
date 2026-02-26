import numpy as np

import matplotlib.pyplot as plt

fa_samples= np.random.normal(loc=35, scale=5, size=5000)

arr = fa_samples[fa_samples<25]

#print(fa_samples)
#print(arr.mean())

#using mean on a boolean array gives probability
pro = (fa_samples<25).mean()
print(pro)
