import math
import scipy

# All stars have three free parameters:
#       * Mass (in Msun, solar mass units)
#       * Age (in Myr, millions of years)
#       * Metallicity (in Z, mass fraction of elements other than H or He)
# Stars should have an age (in Myr) less than 13800 *unless* they are meant to be
#  hypothetical future stars.  An age of 0 represents emergence onto the main
#  sequence, while negative ages represent PMS stars, protostars, and unstable dust clouds.
# Stars should have a mass (in MSun) between 0.01 and 150.  Other ranges require
#  renormalization of the L3 massfunction.
# Stars must, by definition, have a metallicity in the range [0,1]
#
# This new approach is due to the paper "Comprehensive analytic formulae for stellar
#  evolution as a function of mass and metallicity" by Hurley, Pols, and Tout (2000).
#  See https://arxiv.org/abs/astro-ph/0001295

class Star:
    def __init__(self, mass, age, metallicity):
        assert self.age >= 0, "Pre-ZAMS object, use PreStar class"
        assert self.mass >= 0.01 and self.mass <= 150, "Stellar mass outside callibrated range!"
        assert self.metallicity >= 0 and self.metallicity <= 1, "Nonsensical metallicity!"
        self.mass = mass
        self.age = age
        self.metallicity = metallicity

    # Set the time-invariant constants needed to follow the star through its evolution
    def setConstants(self):
        # Logarithmic metallicity relative to Sol, analogous to [Fe/H]
        log_metallicity = math.log((self.metallicity / 0.02), 10)
        # Mass above which a main sequence hook appears
        mass_hook = 1.0185 + 0.16015*log_metallicity + 0.0892*log_metallicity**2
        # Maximum mass for which a helium flash occurs
        mass_HeF = 1.995 + 0.25*log_metallicity + 0.087*log_metallicity**2
        # Maximum mass for which helium ignites on the first giant branch
        mass_FGB = (13.048*(log_metallicity/0.02)**0.06)/(1 + 0.0012*(0.02/log_metallicity)**1.27)
        

# A class for stars with an age less than 0 (pre-ZAMS)
class PreStar(Star):
    pass
