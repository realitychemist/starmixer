import math
import numpy as np
import csv

# All stars have three free parameters:
#       * Mass (in Msun, solar mass units)
#       * Age (in Myr, millions of years)
#       * Metallicity (in Z, mass fraction of elements other than H or He)
# Stars should have an age (in Myr) less than 13800 *unless* they are meant to be
#  hypothetical future stars.  An age of 0 represents emergence onto the main
#  sequence (ZAMS), while negative ages represent PMS stars, protostars, etc...
# Stars should have a mass (in MSun) between 0.01 and 150.  Other ranges require
#  renormalization of the massfunction.
# Stars must, by definition, have a metallicity in the range [0,1], although the
#  values 0 and 1 themselves make the math weird, so I've restricted this range to (0,1)
#
# This approach is due to the paper "Comprehensive analytic formulae for stellar
#  evolution as a function of mass and metallicity" by Hurley, Pols, and Tout (2000).
#  See https://arxiv.org/abs/astro-ph/0001295

class Star:
    def __init__(self, mass, age, metal):

        # Lots of math goes on here, but we end up with the following in each object
        #  instance once __init__ goes out of scope.  All other variables are temporary:

        ## INSTANCE VARIABLES ##
        # mass    : Mass of star (in Msun)
        # age     : Age of star beyond ZAMS (in Myr)
        # metal   : Metallicity of star (as non-H/He fraction)

        self.mass = mass
        assert self.mass >= 0.01 and self.mass <= 150, "Stellar mass outside calibrated range!"
        # TODO: calibrated mass range should be read from massfunction.py, not hardcoded
        self.age = age
        assert self.age >= 0, "Pre-ZAMS object!"
        self.metal = metal
        assert self.metal > 0 and self.metal < 1, "Nonsensical metallicity!"

        metal_relative = math.log(self.metal/0.02, 10)
        metal_const = self.setMetalConstants(metal_relative)

        # "Signpost" mass values
        mass_hook = np.polyval([0.0892, 0.16015, 1.0185], metal_relative)
        mass_HeF = np.polyval([0.087, 0.25, 1.995], metal_relative)
        mass_FGB = (13.048*(self.metal/0.02)**0.06)/(1 + 0.0012*(0.02/self.metal)**1.27)

        # Main sequence / HG time constants
        time_BGB = ((metal_const["a1"] + metal_const["a2"]*self.mass**4
                    + metal_const["a3"]*self.mass**5.5 + self.mass**7)
                    /(metal_const["a4"]*self.mass**2 + metal_const["a5"]*self.mass**7))
        t_x = max(0.95, min(0.95 - 0.03*(metal_relative + 0.30103), 0.99))
        t_mu = max(0.5, 1.0 - 0.01*max(metal_const["a6"] / self.mass**metal_const["a7"],
                                        metal_const["a8"] + metal_const["a9"] / self.mass**metal_const["a10"]))
        time_hook = t_mu * time_BGB
        time_MS = max(time_hook, t_x*time_BGB)

        # TODO: find a better place for this comment
        # ZAMS radius and luminosity are due to "Zero-age main-sequence radii and luminosities
        #  as analytic functions of mass and metallicity" by Tout, Eggleton, and Han (1996)
        # See: https://academic.oup.com/mnras/article/281/1/257/1066409


    # Set the lifepath metallicity constants
    # TODO: Come back and finish these!
    def setMetalConstants(self, metal_relative):
        # We need these special forms for a few adjustments below
        metal_logarithmic = math.log(self.metal, 10)
        metal_rel_raised = metal_relative + 1

        metal_const = {} # Dictionary of metallicity constants
        with open("Coefficients.csv", newline="") as coFile:
            reader = csv.DictReader(coFile, fieldnames=["name","4","3","2","1","0"])
            # Most constants are just the output of simple polynomials...
            for r in reader:
                coList = [float(i) for i in [r["4"],r["3"],r["2"],r["1"],r["0"]]]
                polyValue = np.polyval(coList, metal_relative)
                metal_const.update({r["name"] : polyValue})

            # But some of these need to be transoformed or just set differently:
            metal_const.update({"a11" : metal_const["a'11"] * metal_const["a14"]})
            metal_const.update({"a12" : metal_const["a'12"] * metal_const["a14"]})
            metal_const.update({"a17" : 10**(max(0.097 - 0.1072*(metal_logarithmic + 3),
                                                max(0.097, min(0.1461, 0.1461 + 0.1237*(metal_logarithmic + 2)))))})
            metal_const.update({"a18" : metal_const["a'18"] * metal_const["a20"]})
            metal_const.update({"a19" : metal_const["a'19"] * metal_const["a20"]})
            metal_const.update({"a11" : metal_const["a'11"] * metal_const["a14"]})
            metal_const.update({"a29" : metal_const["a'29"] ** metal_const["a32"]})
            # a33 gets updated twice in sequence
            metal_const.update({"a33" : min(1.4, 1.5135 + 0.3769*metal_relative)})
            metal_const.update({"a33" : max(0.6355 - 0.4192*metal_relative, max(1.25, metal_const["a33"]))})
            metal_const.update({"a42" : min(1.25, max(1.1, metal_const["a42"]))})
            metal_const.update({"a44" : min(1.3, max(0.45, metal_const["a44"]))})
            metal_const.update({"a49" : max(metal_const["a49"], 0.145)})
            metal_const.update({"a50" : min(metal_const["a50"], 0.306 + 0.053*metal_relative)})
            metal_const.update({"a51" : min(metal_const["a51"], 0.3625 + 0.062*metal_relative)})
            # Both a52 and a53 get updated twice in sequence (depending on metallicity)
            metal_const.update({"a52" : max(metal_const["a52"], 0.9)})
            if(self.metal > 0.01):
                metal_const.update({"a52" : min(metal_const["a52"], 1.0)})
            metal_const.update({"a53" : max(metal_const["a53"], 1.0)})
            if(self.metal > 0.01):
                metal_const.update({"a53" : min(metal_const["a53"], 1.1)})
            # a57 gets updated twice in sequence
            metal_const.update({"a57" : min(1.4, 1.5135 + 0.3769*metal_relative)})
            metal_const.update({"a57" : max(0.6355 - 0.4192*metal_relative, max(1.25, metal_const["a57"]))})
            metal_const.update({"a62" : max(metal_const["a62"], 0.065)})
            # The update for 163 is strictly conditional
            if(self.metal < 0.004):
                metal_const.update({"a63" : min(metal_const["a63"], 0.055)})
            metal_const.update({"a64" : max(0.091, min(0.121, metal_const["a64"]))})
            # a66 gets updated twice sequentially
            metal_const.update({"a66" : max(metal_const["a66"], min(1.6, -0.308 - 1.046*metal_relative))})
            metal_const.update({"a66" : max(0.8, min(0.8 - 2.0*metal_relative, metal_const["a66"]))})
            metal_const.update({"a68" : max(0.9, min(metal_const["a68"], 1.0))})
            # Another update of a64 may be reuqired at this point
            # TODO: come back and add this update once radius alpha coefficient is written
            metal_const.update({"a68" : min(metal_const["a68"], metal_const["a66"])})
            if(self.metal > 0.01):
                metal_const.update({"a72" : max(metal_const["a72"], 0.95)})
            metal_const.update({"a74" : min(metal_const["a74"], 1.6)})
            # a75 gets updated twice sequentially
            metal_const.update({"a75" : max(1.0, min(metal_const["a75"], 1.27))})
            metal_const.update({"a75" : max(metal_const["a75"], 0.6355 - 0.4192*metal_relative)})
            metal_const.update({"a76" : max(metal_const["a76"],
                                            np.polyval([-0.05182516, -0.2161264, -0.1015564], metal_relative))})
            metal_const.update({"a77" : max(min(0.0, metal_const["a77"]),
                                            np.polyval([-0.1463472, -0.5457078, -0.3868776], metal_relative))})
            metal_const.update({"a78" : max(0.0, min(metal_const["a78"], 7.454 + 9.046*metal_relative))})
            metal_const.update({"a79" : min(metal_const["a79"], max(2.0, -13.3 - 18.6*metal_relative))})
            metal_const.update({"a80" : max(0.0585542, metal_const["a80"])})
            metal_const.update({"a81" : min(1.5, max(0.4, metal_const["a81"]))})
            metal_const.update({"b1" : min(0.54, metal_const["b1"])})
            # b2 gets updated twice sequentially
            metal_const.update({"b2" : 10**(-4.6739-0.9394*metal_logarithmic)})
            metal_const.update({"b2" : min(max(metal_const["b2"], -0.04167 + 55.67*self.metal),
                                            0.4771 - 9329.21*self.metal**2.94)})
            # b'3 is a preliminary for b3
            metal_const.update({"b'3" : max(-0.1451, np.polyval([-0.254, -1.5175, -2.2794], metal_logarithmic))})
            # b3 gets updated twice sequentially (depending on metallicity)
            metal_const.update({"b3" : 10**metal_const["b'3"]})
            if(self.metal > 0.004):
                metal_const.update({"b3" : max(metal_const["b3"], 0.7307 + 14265.1*self.metal**3.395)})
            metal_const.update({"b4" : metal_const["b4"] + 0.1231572*metal_relative**5})
            metal_const.update({"b6" : metal_const["b6"] + 0.01640687*self.metal**5})
            metal_const.update({"b11" : metal_const["b'11"]**2})
            metal_const.update({"b13" : metal_const["b'13"]**2})
            metal_const.update({"b14" : metal_const["b'14"]**metal_const["b15"]})
            metal_const.update({"b16" : metal_const["b'16"]**metal_const["b15"]})
            if(metal_relative > -1.0):
                metal_const.update({"b17" : 1.0})
            else:
                metal_const.update({"b17" : 1.0 - 0.3880523*(metal_relative + 1.0)**2.862149})
            metal_const.update({"b24" : metal_const["b'24"]**metal_const["b28"]})
            metal_const.update({"b26" : 5.0 - 0.09138012*self.metal**-0.3671407})
            metal_const.update({"b27" : metal_const["b'27"]**(2*metal_const["b28"])})
            metal_const.update({"b31" : metal_const["b'31"]**metal_const["b33"]})
            metal_const.update({"b34" : metal_const["b'34"]**metal_const["b33"]})
            metal_const.update({"b36" : metal_const["b'36"]**4})
            metal_const.update({"b37" : 4.0*metal_const["b'37"]})
            metal_const.update({"b38" : metal_const["b'38"]**4})
            metal_const.update({"b40" : max(metal_const["b40"], 1.0)})
            metal_const.update({"b41" : metal_const["b'41"]**metal_const["b42"]})
            metal_const.update({"b44" : metal_const["b'44"]**5})
            if(metal_rel_raised <= 0.0):
                metal_const.update({"b45" : 1.0})
            else:
                metal_const.update({"b45" : np.polyval([3.247361, -5.401682, 2.47162, 1.0], metal_rel_raised)})
            # TODO: come back and do this once M_HeF and M_FGB are written
            # metal_const.update({"b46" : -1.0*metal_const["b46"]*math.log()})
            metal_const.update({"b47" : np.polyval([-0.3793726, 0.2344416, 1.127733, 0], metal_rel_raised)})
            metal_const.update({"b51" : metal_const["b'51"] - 0.1343798*metal_relative**5})
            metal_const.update({"b53" : metal_const["b'53"] - 0.4426929*metal_relative**5})
            metal_const.update({"b55" : min(0.99164 - 743.123*self.metal**2.83, metal_const["b55"])})
            metal_const.update({"b56" : metal_const["b'56"] - 0.1140142*metal_relative**5})
            metal_const.update({"b57" : metal_const["b'57"] - 0.01308728*metal_relative**5})

        return metal_const
