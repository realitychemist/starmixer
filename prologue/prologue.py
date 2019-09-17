# This file is for "scratch work" like figuring out probability functions
# Nothing from here should ever be called in the rest of the project

import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

### !!~~!! STELLAR MASS DISTRIBUTION !!~~!! ###

# Constants
ALPHA_LOW = -0.3
ALPHA_MID = -1.3
ALPHA_HIGH = -2.3

## --==-- KROUPA IMF SEGMENTS --==-- ##
kroupaLow = lambda m: m**ALPHA_LOW
kroupaMid = lambda m: m**ALPHA_MID
kroupaHigh = lambda m: m**ALPHA_HIGH

## --==-- MASS CDF (NON-NORMALIZED) --==-- ##
def underMassFrac(m):
    ## --==-- CATCH EXTREMES --==-- ##
    # Should not ever be called if other functions are working properly
    if m < 0.01: # No known stars smaller than this mass, fraction is zero
        print("WARNING: Mass lower than any known star")
        return 0
    if m > 375: # No known stars larger than this mass, fraction is one
        print("WARNING: Mass higher than any known star")
        return 1

    # Accumulator for returns of Kroupa IMF: N(m)dm = m**-a, where a varies by mass range
    count = 0.0

    ## --==-- LOW MASS STARS --==-- ##
    if m <= 0.08: # Count low mass stars up to m if m is a low mass star
        count += float(integrate.quad(kroupaLow, 0.01, m)[0])
    else: # Count all low mass stars if m is larger than all low mass stars
        count += float(integrate.quad(kroupaLow, 0.01, 0.08)[0])

    ## --==-- MID MASS STARS --==-- ##
    if m <= 0.5 and m > 0.08: # Count mid mass stars up to m if m is a mid mass star
        count += float(integrate.quad(kroupaMid, 0.08, m)[0])
    elif m > 0.5: # Count all mid mass stars if m is larger than all mid mass stars
        count += float(integrate.quad(kroupaMid, 0.08, 0.5)[0])

    ## --==-- HIGH MASS STARS --==-- ##
    if m > 0.5: # Count high mass stars up to m if m is a high mass star
        count += float(integrate.quad(kroupaHigh, 0.5, m)[0])

    # Divide accumulated values by total of summing all stars from mass 0.01 to 375 to get fraction under m, and return
    denom = float(integrate.quad(kroupaLow, 0.01, 0.08)[0]) +\
            float(integrate.quad(kroupaMid, 0.08, 0.5)[0]) +\
            float(integrate.quad(kroupaHigh, 0.5, 375)[0])
    return count/denom


# Range of stellar masses, in 0.01 stellar mass increments
masses = np.arange(0.01, 375, 0.01)

# Domain: fraction of stars under mass m (this will be a CDF if plotted on [0,1] x-axis)
mass_cdf = []
for m in masses:
    mass_cdf.append(underMassFrac(m))

# Use min-max normalization to rescale x-axis (should work well due to even point distribution)
masses_renorm = []
for m in masses:
    renorm = (m - 0.01)/(375 - 0.01)
    masses_renorm.append(renorm)

plt.yscale("log")
plt.xscale("log")
plt.plot(masses_renorm, mass_cdf, 'o', color="black")
plt.savefig("cdf_test.png")
plt.close()

# This is our mass CDF (numerical)
# We would prefer to have a PDF, which could then be passed to random.choices
# See: https://stackoverflow.com/questions/4265988/generate-random-numbers-with-a-given-numerical-distribution

# See: https://arxiv.org/pdf/1212.0939.pdf
# This source shows several IMFs as PDFs (normalized so full integral is 1)
# Their L3 IMF looks very promising and much more computationally tractable
# pl3(m) = A(m/mu)^-alpha * (1+(m/mu)^(1-alpha))^-beta
# alpha = 2.3, beta = 1.4, mu = 0.2, A depends on integration limits
