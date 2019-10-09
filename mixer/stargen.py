import math
import scipy

# All stars have mass and age as free parameters
# They also have metallicity as a free parameter, but that is likely out of scope
# Stars should have an age (in MY) greater than 0 and less than 13800
# Stars should have a mass (in MSun) between 0.01 and 395
# Lower mass objects are not stars; the upper limit is based on max est mass for R136a1
class Star:
    def __init__(self, mass, age):
        assert self.age >= 0 and self.age <= 13800, "Invalid stellar age."
        assert self.mass >= 0.01 and self.mass <= 395, "Invalid stellar mass."
        self.mass = mass
        self.age = age


# Protostars are young stars of any size
# Protostar objects should be created for stars between 0 and 0.5 MY old
# See: https://arxiv.org/pdf/1401.1809.pdf
# Protostars should not have planets, but may have accretion disks and envelopes
# See: https://astronomy.stackexchange.com/questions/764/timescale-of-ignition-of-a-protostar
class Protostar(Star):

    def __init__(self, mass, age):
        assert self.age >= 0 and self.age <= 0.5, "Incorrect age for a protostar."
        ## --==-- RADIUS --==-- ##
        # TODO: Check edge cases on math, esp. max age
        # Using the Jeans radius as initial radius at age = 0 MY
        inital_radius = jeans_radius(self.mass)
        # Final radius by main sequence continuity
        final_radius = 0 # FIXME: Should call actual radius function for BD/PMS/MS
        # Radius is based on collapse from Jeans radius to final radius
        # Collapse happens in freefall time
        # See: http://www.astro.uu.se/~hoefner/astro/teach/apd_files/apd_collapse.pdf
        density = jeans_density(self.mass)
        freefall_time = ((3*math.pi/(32*scipy.G*jeans_density))**(1/2)/3.154e13)
        # Note: The following is just a linear interpolation, not physically accurate
        self.radius = ((self.age * (final_radius-initial_radius)/freefall_time) + initial_radius)
        assert self.radius > 0, "Stellar radius less than zero!"
        ## --==-- TEMPERATURE --==-- ##
        initial_temp = 20
        # Continuity condition
        final_temp = 0 # FIXME: Should call actual temp function for BD/PMS/MS
        # Linear interpolation over freefall time (again, not realistic)
        self.temperature = ((self.age * (final_temp-initial_temp)/freefall_time) + initial_temp)
        assert self.temperature >= 20, "Protostar cooler than star forming medium!"
        ## --==-- LUMINOSITY --==-- ##
        # Function of temperature
        ## --==-- COLOR --==-- ##
        # Implement w/ colorpy

    def jeans_radius(mass):
        # Critical Jeans radius assumes T=20K, particle mass=3.9e-24
        return ((scipy.G*mass*3.9e-24*1.989e+30) / (scipy.k*20))

    def jeans_density(mass):
        return mass / ((4/3)*math.pi*jeans_radius(mass)**3)

# A pre-main-sequence star is older than a protostar, but still young (<~20 MY)
# These stars should have mass between 0.08 and 10 MSun
# More massive stars emerge directly onto the main sequence
class Pre_Main_Sequence(Star):
    pass


# The main section of stellar life
# See: http://personal.psu.edu/rbc3/A534/lec18.pdf
# See: http://hyperphysics.phy-astr.gsu.edu/hbase/Astro/startime.html
class Main_Sequence(Star):
    pass


# Brown dwarves form from protostars which accreted less than 0.08 MSun
# There is no upper limit on the age of a brown dwarf, but they cool steadily
# See: http://www2.ifa.hawaii.edu/CSPF/presentations/bdtutorial/bdtutorial.pdf
class BrownDwarf(Star):
    pass


# TODO: Prototype post-main-sequence stars and stellar remnants
# PMS star types: AG, RG, RSG, BSG, LBV, YHG, WR
# Remnant types: White_Dwarf, Neutron_Star (multiple types), Black_Hole
