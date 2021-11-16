"""All masses in M_S.

Use with random.choices.  Minimal working example would be something lile:
    from random import choices
    population = np.geomspace(lower, upper, num=1000)
    weights = KroupaIMF(population)
    single_value = choices(population, weights)
    k_values = choices(population, weights, k=100)
"""

import numpy as np


def KroupaIMF(m):
    """From Kroupa 2001.

    A relatively simple IMF, built up of piecewise power laws.
    """
    cond1 = m < 0.08
    cond2 = (m >= 0.08) & (m < 0.5)
    cond3 = (m >= 0.5) & (m < 1)
    cond4 = m >= 1

    # Amplitude coefficients below are used to ensure continuity
    imf = np.ones(m.shape)
    imf[cond1] *= m[cond1]**-0.3
    imf[cond2] *= 0.0226274*m[cond2]**-1.8
    imf[cond3] *= 0.0121257*m[cond3]**-2.7
    imf[cond4] *= 0.0121257*m[cond4]**-2.3
    # Normalize the function across the mass range given
    imf[:] /= sum(imf)
    return imf


def ChabrierIMF(m):
    """From Chabrier 2003.

    Somewhat more complex than the Kroupa IMF, made up of both power lawn and log normal pieces
    (gives fewer extremely low / extremely high mass bodies than Kroupa).
    """
    cond1 = m <= 1
    cond2 = (m > 1) & (np.log(m) <= 0.54)
    cond3 = (np.log(m) > 0.54) & (np.log(m) <= 1.26)
    cond4 = np.log(m) > 1.26  # Technically only defined up to log(m) <= 1.8, but we'll extrapolate

    imf = np.ones(m.shape)
    imf[cond1] *= 0.158*np.exp(-(np.log(m[cond1]) - np.log(0.079))**2/(2*0.69**2))
    # The amplitudes here have been rescaled from the ones presented in Chabrier 2003 in order to
    #  give a continuous IMF; the values presented in the paper give large discontinuties
    imf[cond2] *= 0.000181982*m[cond2]**-1.3
    imf[cond3] *= 0.000606745*m[cond3]**-3.53
    imf[cond4] *= 0.000101383*m[cond4]**-2.11
    # Normalize the function across the mass range given
    imf[:] /= sum(imf)
    return imf


# %% TEST
# The lowest mass brown dwarfs are about 0.01 solar masses (13 M_J)
# The highest mass star currently known is about 250 M_S, although during formation the upper limit
#  should be approx. 120 M_S (more massive stars need to gain mass later in life, e.g. through
#  accretion in a binary).  I'll test out to 250 M_S just to see what I get

# def test(lower=0.01, upper=250):
#     import matplotlib.pyplot as plt
#     masses = np.geomspace(lower, upper, num=1000)
#     y_kr = KroupaIMF(masses)
#     y_ch = ChabrierIMF(masses)

#     plt.plot(masses, y_kr, "r-", label="Kroupa")
#     plt.plot(masses, y_ch, "b-", label="Chabrier")
#     plt.yscale("log")
#     plt.xscale("log")
#     plt.legend()


# test()
