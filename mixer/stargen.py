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
# Protostars should not have planets, but should have accretion disks and dust/gas envelopes
class Protostar(Star):
    pass

# A pre-main-sequence star is older than a protostar, but still young (<20 MY)
# These stars should have mass between 0.08 and 8 MSun
class Pre_Main_Sequence(Star):
    pass

# A class for massive young stars (>8 MSun, <0.1 MY)
# See: https://astronomy.stackexchange.com/questions/156/how-long-does-it-take-to-produce-a-star-why-does-it-take-that-long
class Pre_Massive(Star):
    pass

# Brown dwarves form from protostars which accreted less than 0.08 MSun
# There is no upper limit on the age of a brown dwarf, but they cool steadily
# See: http://www2.ifa.hawaii.edu/CSPF/presentations/bdtutorial/bdtutorial.pdf
class BrownDwarf(Star):
    pass

# Masses between 0.08 MSun and 0.6 MSun
# No upper limit on age, should be at least 20 MY old
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
