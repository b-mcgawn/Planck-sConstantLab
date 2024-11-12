#Imports
import numpy as np, matplotlib.pyplot as plt, pandas as pd

#Constants
e_charge = 1.602e-19 #Couloumbs
c = 3.00e8 #m/s
size = 1000


#Import data
data = pd.read_csv('./DataLab4/Sheet3.csv')

V = data['V'][0:4]
V = np.array(V)

dV = data['dV'][0:4]
dV = np.array(dV)

# find energies
# might be this times 1,000- if it was in millivolts, which i dont think it was
E = V*e_charge
stdE = dV*e_charge


# find wavelengths
max_wave = np.array(data['Peak wavelength'][0:4]) #nm!!
std_wave = np.array(data['sigma'][0:4]) #nm!!


# find frequencies
def frequency(wave):
    return c*1E9/wave #gets it back into seconds

wave_hists = np.ones([len(max_wave),size])
f_hists = np.ones([len(max_wave),size])
for i in range(len(max_wave)):
    wave_hists[i] = np.random.normal(max_wave[i],std_wave[i],size)
    f_hists = frequency(wave_hists)

fmax = np.ones(len(max_wave))
fstd = np.ones(len(max_wave))

h_hist = np.ones([len(max_wave),size])
h_means = np.ones(len(max_wave))
hstd = np.ones(len(max_wave))

# find h
def hCalc(E,f):
    return E/f

for i in range(len(max_wave)):
    fmax[i] = np.mean(f_hists[i])
    fstd[i] = np.std(f_hists[i])

    E_hist = np.random.normal(E[i],stdE[i],size)
    
    # E = hf
    # h = E/f
    h_hist[i] = hCalc(E_hist,f_hists[i])
    h_means[i] = np.mean(h_hist[i])
    hstd[i] = np.std(h_hist[i])

h_weights = hstd**-2
w_sum = np.sum(h_weights)

h_mean = np.average(h_means,weights = h_weights)
h_std = np.sqrt(1/w_sum)
'''
wrong! 
h_var = w_sum*np.sum((h_means-h_mean)**2)/(w_sum**2 - np.sum(h_weights**2))
h_std = np.sqrt(h_var)
'''
h_line = np.poly1d((h_mean,0))
h_accepted = np.poly1d((6.626e-34,0))
h_eval = np.linspace(np.min(fmax)-np.max(fstd),np.max(fmax)+np.max(fstd),size)
h_plot = h_line(h_eval)
h_real = h_accepted(h_eval)

# Plotting
plt.ion()
plt.figure(20)
plt.clf()

plt.plot(h_eval,h_plot,"-r",label = "Measured value of h")
plt.plot(h_eval,h_real,"-b",label = "Accepted value of h")

plt.errorbar(x = fmax, y = E, yerr = stdE, xerr = fstd, color = "k",fmt = "o")

plt.title("Determining Planck's Constant")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Band Gap Energy (J)")
plt.legend()

print("Measured value of h: " + str(h_mean))
print("std: " + str(h_std))
