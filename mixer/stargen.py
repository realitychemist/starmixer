import math
import numpy as np
import csv
# import scipy as sci

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
        self.mass = mass
        assert self.mass >= 0.01 and self.mass <= 150, "Stellar mass outside calibrated range!"
        # TODO: calibrated mass range should be read from massfunction.py, not hardcoded
        self.age = age
        assert self.age >= 0, "Pre-ZAMS object, use PreStar class"
        self.metallicity = metallicity
        assert self.metallicity > 0 and self.metallicity < 1, "Nonsensical metallicity!"
        self.relativeMetallicity = math.log(self.metallicity/0.02, 10)
        self.logMetallicity = math.log(self.metallicity, 10)
        self.raisedMetallicity = self.relativeMetallicity + 1
        self.metalConstants = self.setMetalConstants()
        print(self.metalConstants) # THIS IS FOR TESTING, REMOVE IT WHEN DONE

    # Set the lifepath metallicity constants
    def setMetalConstants(self):
        metalConstants = {} # Dictionary of metallicity constants
        with open('Coefficients.csv', newline='') as coFile:
            reader = csv.DictReader(coFile, fieldnames=['name','mu','eta','gamma','beta','alpha'])
            # Most constants are just the output of simple polynomials...
            for r in reader:
                coList = [float(i) for i in [r['mu'],r['eta'],r['gamma'],r['beta'],r['alpha']]]
                polyValue = np.polyval(coList, self.relativeMetallicity)
                metalConstants.update({r['name'] : polyValue})

            # But some of these need to be transoformed or just set differently:
            metalConstants.update({"a11" : metalConstants["a'11"] * metalConstants["a14"]})
            metalConstants.update({"a12" : metalConstants["a'12"] * metalConstants["a14"]})
            metalConstants.update({"a17" : 10**(max(0.097 - 0.1072*(self.logMetallicity + 3), max(0.097, min(0.1461, 0.1461 + 0.1237*(self.logMetallicity + 2)))))})
            metalConstants.update({"a18" : metalConstants["a'18"] * metalConstants["a20"]})
            metalConstants.update({"a19" : metalConstants["a'19"] * metalConstants["a20"]})
            metalConstants.update({"a11" : metalConstants["a'11"] * metalConstants["a14"]})
            metalConstants.update({"a29" : metalConstants["a'29"] ** metalConstants["a32"]})
            # a33 gets updated twice in sequence
            metalConstants.update({"a33" : min(1.4, 1.5135 + 0.3769*self.relativeMetallicity)})
            metalConstants.update({"a33" : max(0.6355 - 0.4192*self.relativeMetallicity, max(1.25, metalConstants["a33"]))})
            metalConstants.update({"a42" : min(1.25, max(1.1, metalConstants["a42"]))})
            metalConstants.update({"a44" : min(1.3, max(0.45, metalConstants["a44"]))})
            metalConstants.update({"a49" : max(metalConstants["a49"], 0.145)})
            metalConstants.update({"a50" : min(metalConstants["a50"], 0.306 + 0.053*self.relativeMetallicity)})
            metalConstants.update({"a51" : min(metalConstants["a51"], 0.3625 + 0.062*self.relativeMetallicity)})
            # Both a52 and a53 get updated twice in sequence (depending on metallicity)
            metalConstants.update({"a52" : max(metalConstants["a52"], 0.9)})
            if(self.metallicity > 0.01):
                metalConstants.update({"a52" : min(metalConstants["a52"], 1.0)})
            metalConstants.update({"a53" : max(metalConstants["a53"], 1.0)})
            if(self.metallicity > 0.01):
                metalConstants.update({"a53" : min(metalConstants["a53"], 1.1)})
            # a57 gets updated twice in sequence
            metalConstants.update({"a57" : min(1.4, 1.5135 + 0.3769*self.relativeMetallicity)})
            metalConstants.update({"a57" : max(0.6355 - 0.4192*self.relativeMetallicity, max(1.25, metalConstants["a57"]))})
            metalConstants.update({"a62" : max(metalConstants["a62"], 0.065)})
            # The update for 163 is strictly conditional
            if(self.metallicity < 0.004):
                metalConstants.update({"a63" : min(metalConstants["a63"], 0.055)})
            metalConstants.update({"a64" : max(0.091, min(0.121, metalConstants["a64"]))})
            # a66 gets updated twice sequentially
            metalConstants.update({"a66" : max(metalConstants["a66"], min(1.6, -0.308 - 1.046*self.relativeMetallicity))})
            metalConstants.update({"a66" : max(0.8, min(0.8 - 2.0*self.relativeMetallicity, metalConstants["a66"]))})
            metalConstants.update({"a68" : max(0.9, min(metalConstants["a68"], 1.0))})
            # Another update of a64 may be reuqired at this point
            # TODO: come back and add this update once radius alpha coefficient is written
            metalConstants.update({"a68" : min(metalConstants["a68"], metalConstants["a66"])})
            if(self.metallicity > 0.01):
                metalConstants.update({"a72" : max(metalConstants["a72"], 0.95)})
            metalConstants.update({"a74" : min(metalConstants["a74"], 1.6)})
            # a75 gets updated twice sequentially
            metalConstants.update({"a75" : max(1.0, min(metalConstants["a75"], 1.27))})
            metalConstants.update({"a75" : max(metalConstants["a75"], 0.6355 - 0.4192*self.relativeMetallicity)})
            metalConstants.update({"a76" : max(metalConstants["a76"], np.polyval([-0.05182516, -0.2161264, -0.1015564], self.relativeMetallicity))})
            metalConstants.update({"a77" : max(min(0.0, metalConstants["a77"]), np.polyval([-0.1463472, -0.5457078, -0.3868776], self.relativeMetallicity))})
            metalConstants.update({"a78" : max(0.0, min(metalConstants["a78"], 7.454 + 9.046*self.relativeMetallicity))})
            metalConstants.update({"a79" : min(metalConstants["a79"], max(2.0, -13.3 - 18.6*self.relativeMetallicity))})
            metalConstants.update({"a80" : max(0.0585542, metalConstants["a80"])})
            metalConstants.update({"a81" : min(1.5, max(0.4, metalConstants["a81"]))})
            metalConstants.update({"b1" : min(0.54, metalConstants["b1"])})
            # b2 gets updated twice sequentially
            metalConstants.update({"b2" : 10**(-4.6739-0.9394*self.logMetallicity)})
            metalConstants.update({"b2" : min(max(metalConstants["b2"], -0.04167 + 55.67*self.metallicity), 0.4771 - 9329.21*self.metallicity**2.94)})
            # b'3 is a preliminary for b3
            metalConstants.update({"b'3" : max(-0.1451, np.polyval([-0.254, -1.5175, -2.2794], self.logMetallicity))})
            # b3 gets updated twice sequentially (depending on metallicity)
            metalConstants.update({"b3" : 10**metalConstants["b'3"]})
            if(self.metallicity > 0.004):
                metalConstants.update({"b3" : max(metalConstants["b3"], 0.7307 + 14265.1*self.metallicity**3.395)})
            metalConstants.update({"b4" : metalConstants["b4"] + 0.1231572*self.relativeMetallicity**5})
            metalConstants.update({"b6" : metalConstants["b6"] + 0.01640687*self.metallicity**5})
            metalConstants.update({"b11" : metalConstants["b'11"]**2})
            metalConstants.update({"b13" : metalConstants["b'13"]**2})
            metalConstants.update({"b14" : metalConstants["b'14"]**metalConstants["b15"]})
            metalConstants.update({"b16" : metalConstants["b'16"]**metalConstants["b15"]})
            if(self.relativeMetallicity > -1.0):
                metalConstants.update({"b17" : 1.0})
            else:
                metalConstants.update({"b17" : 1.0 - 0.3880523*(self.relativeMetallicity + 1.0)**2.862149})
            metalConstants.update({"b24" : metalConstants["b'24"]**metalConstants["b28"]})
            metalConstants.update({"b26" : 5.0 - 0.09138012*self.metallicity**-0.3671407})
            metalConstants.update({"b27" : metalConstants["b'27"]**(2*metalConstants["b28"])})
            metalConstants.update({"b31" : metalConstants["b'31"]**metalConstants["b33"]})
            metalConstants.update({"b34" : metalConstants["b'34"]**metalConstants["b33"]})
            metalConstants.update({"b36" : metalConstants["b'36"]**4})
            metalConstants.update({"b37" : 4.0*metalConstants["b'37"]})
            metalConstants.update({"b38" : metalConstants["b'38"]**4})
            metalConstants.update({"b40" : max(metalConstants["b40"], 1.0)})
            metalConstants.update({"b41" : metalConstants["b'41"]**metalConstants["b42"]})
            metalConstants.update({"b44" : metalConstants["b'44"]**5})
            if(self.raisedMetallicity <= 0.0):
                metalConstants.update({"b45" : 1.0})
            else:
                metalConstants.update({"b45" : np.polyval([3.247361, -5.401682, 2.47162, 1.0], self.raisedMetallicity)})
            # TODO: come back and do this once M_HeF and M_FGB are written
            # metalConstants.update({"b46" : -1.0*metalConstants["b46"]*math.log()})
            metalConstants.update({"b47" : np.polyval([-0.3793726, 0.2344416, 1.127733, 0], self.raisedMetallicity)})
            metalConstants.update({"b51" : metalConstants["b'51"] - 0.1343798*self.relativeMetallicity**5})
            metalConstants.update({"b53" : metalConstants["b'53"] - 0.4426929*self.relativeMetallicity**5})
            metalConstants.update({"b55" : min(0.99164 - 743.123*self.metallicity**2.83, metalConstants["b55"])})
            metalConstants.update({"b56" : metalConstants["b'56"] - 0.1140142*self.relativeMetallicity**5})
            metalConstants.update({"b57" : metalConstants["b'57"] - 0.01308728*self.relativeMetallicity**5})

        return metalConstants

# A class for stars with an age less than 0 (pre-ZAMS)
class PreStar(Star):
    pass
