import math
import scipy

# All stars have mass and age as free parameters
# Stars should have an age (in MY) greater than 0 and less than 13800
# Stars should have a mass (in MSun) between 0.01 and 395
# Lower mass objects are not stars; the upper limit is based on max est mass for R136a1
# Consider adding population class for stars (1, 2, or 3) based on metallicity (epoch)
class Star:
    def __init__(self, mass, age):
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
        # Critical Jeans radius assumes T=20K, particle mass=3.9e-24
        # Using the Jeans radius as initial radius at age = 0 MY
        jeans_radius = ((scipy.G*self.mass*3.9e-24*1.989e+30) / (scipy.k*20))
        # Final radius is equal to BD/PMS/MMS radius (continuity)
        if self.mass < 0.08: # Brown dwarf continuity condition
            final_radius = 0 # FIXME: Needs actual BD radius eqn
        elif self.mass < 1: # Lower mass main sequence continuity
            final_radius = slef.mass**0.8
        else: # Higher mass main sequence continuity;
            final_radius = self.mass**0.57
        # Radius is based on collapse from Jeans radius to final radius
        # Collapse happens in freefall time
        # See: http://www.astro.uu.se/~hoefner/astro/teach/apd_files/apd_collapse.pdf
        jeans_density = self.mass / ((4/3)*math.pi*jeans_radius**3)
        freefall_time = ((3*math.pi/(32*scipy.G*jeans_density))**(1/2)/3.154e13)
        # Note: The following is just a linear interpolation, not physically accurate
        self.radius = ((self.age * (final_radius-jeans_radius)/freefall_time) + jeans_radius)
        assert self.radius > 0, "Stellar radius less than zero!"

        ## --==-- TEMPERATURE --==-- ##
        initial_temp = 20
        # Continuity condition
        if self.mass < 0.08: # Brown dwarf continuity
            final_temp = 0 # FIXME: Needs actual BD temp eqn
        elif self.mass < 1: # Lower mass MS continuity
            final_temp = 0 # FIXME: Needs actual LMS temp eqn
        else: # Higher mass MS continuity
            final_temp = 0 # FIXME: Needs actual HMS temp eqn

        # Linear interpolation over freefall time
        self.temperature = ((self.age * (final_temp-initial_temp)/freefall_time) + initial_temp)
        assert self.temperature >= 20, "Protostar cooler than star forming medium!"

        ## --==-- COLOR --==-- ##
        # Implement w/ colorpy

        ## --==-- LUMINOSITY --==-- ##
        # Function of temperature


# A pre-main-sequence star is older than a protostar, but still young (<20 MY)
# These stars should have mass between 0.08 and 10 MSun
class Pre_Main_Sequence(Star):
    pass

# Brown dwarves form from protostars which accreted less than 0.08 MSun
# There is no upper limit on the age of a brown dwarf, but they cool steadily
# See: http://www2.ifa.hawaii.edu/CSPF/presentations/bdtutorial/bdtutorial.pdf
class BrownDwarf(Star):
    pass


# Masses between 0.08 MSun and 0.6 MSun
# No upper limit on age, should be at least 20 MY old
# See: http://personal.psu.edu/rbc3/A534/lec18.pdf
class Low_Mass_Main_Sequence(Star):
    pass


# Masses between 0.6 and 10 MSun
# Age between 20 MY and 10000 MY (lifetime depends on mass)
# See: http://hyperphysics.phy-astr.gsu.edu/hbase/Astro/startime.html
class Midsize_Main_Sequence(Star):
    pass


# Masses above 10 MSun
# Age between 0.1 MY and 32 MY (lifetime depends on mass)
# See: http://hyperphysics.phy-astr.gsu.edu/hbase/Astro/startime.html
class Massive_Main_Sequence(Star):
    pass


# TODO: Prototype post-main-sequence stars and stellar remnants
# PMS star types: AG, RG, RSG, BSG, LBV, YHG, WR
# Remnant types: White_Dwarf, Neutron_Star (multiple types), Black_Hole
