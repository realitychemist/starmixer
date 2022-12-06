import blackbody

class CelestialBody():
    # Any object in space is a celestial body
    def __init__(self, mass, age, angular):
        self.mass = mass  # m_sol
        self.age = age  # log(MYR)
        self.angular = angular  # L_sol (not to be confused with luminosity)

# %% -=- Stellar Objects -=- %% #
class Star(CelestialBody):
    # A star is any fusing body sitting near the center of mass of a system
    def __init__(self, mass, age, angular, metallicity):
        self.metallicity = metallicity  # Z
        super(Star, self).__init__(mass, age, angular)

class MainSequence(Star):
    # Most stars are main sequence stars (this class includes red dwarfs)
    def __init__(self, mass, age, angular, metallicity):
        super(MainSequence, self).__init__(mass, age, angular, metallicity)
        temperature = (mass**2.5)**-4  # T_sol
        color = blackbody.color_match(temperature)  # RGB hexadecimal
        radius = mass**0.5  # r_sol
        luminosity = mass**3.5  # L_sol (not to be confused with angular momentum)
        rotation = None  # Function of angular/mass/radius

class Giant(Star):
    # A star past the main sequence part of its life (or that skipped it)
    pass

class WolfRayet(Giant):
    # A peculiar type of giant characterized by extremely high temperature and strong stellar wind
    pass

# %% -=- Stellar Remnants -=- %% #
class Remnant(CelestialBody):
    # The remains of a body that was once a star
    pass

class WhiteDwarf(Remnant):
    # A relatively cool stellar remnant, usually of fairly low mass
    pass

class Neutron(Remnant):
    # The remnants of a massive star that has undergone a supernova
    pass

class Pulsar(WhiteDwarf, Neutron):
    # A neutron star (sometimes a white dwarf) that projects energetic beams from its poles
    pass

class Magnetar(Neutron):
    # A type of nuetron star with a strong magnetic field that periodically bursts with radiation
    pass

class BlackHole(Remnant):
    # The remnant of a massize star (usually), from which no light can escape
    pass

# %% -=- Non-Stellar Objects -=- %% #
class Protostar(CelestialBody):
    # A protostar is an mass of gas and space dust in the process of collapsing
    pass

class PreMainSequence(CelestialBody):
    # A coalesced body older than a protostar, but which has not yet reached ZAMS
    pass

class BrownDwarf(CelestialBody):
    # A small body which is almost -- but not quite -- massive enough to undergo fusion
    pass

class Satellite(CelestialBody):
    # Any body in orbit around another body
    pass

class AccretionDisk(Satellite):
    # A disk of debris remaing from stellar formation in the process of forming a planet
    pass

class Planet(Satellite):
    # A rocky or gasseous body in orbit around a star-like object
    pass

class Moon(Satellite):
    # A rocky stellite of a planet
    pass

class Asteroid(Satellite):
    # Small rocky or icy bodies in orbit around a star-like object (or captured in a L point)
    pass

class Comet(Satellite):
    # Icy body that trails a tail when passing near a star; orbit is usually highly eliptical
    pass

# %% -=- Constructs (Low Priority) -=- %% #
class Construct(Satellite):
    # Any non-naturally occuring celestial body in orbit around a star or remnant
    pass

class DysonSwarm(Construct):
    # Many small satellites around a star, intended to harvest energy
    pass

class DysonSphere(Construct):
    # A shell constructed around a star intended to harvest energy
    pass

class Topopolis(Construct):
    # A massive (stellar-scale) habitat construct, like many O'Neil cylinders joined together
    pass

class NivenRing(Construct):
    # A stellar scale rotating torroidal habitat
    pass

class BishopRing(Construct):
    # A planetary scale rotating rorroidal habitat in orbit around a star or remnant
    pass

class ShellWorld(Construct):
    # Any of several types of hollow, planet or asteroid scale habitats orbiting a star or remnant
    pass

class OrbitalRing(Construct):
    # A torroidal habitat encircling (or partly encircling) a planet or moon
    pass

class ONeillCylinder(Construct):
    # An orbital scale habitat formed from a rotating cylinder
    pass

class SpaceStation(Construct):
    # Any small-scale habitat in orbit around a planet, moon, asteroid, star, etc...
    pass

# %% -=- Compositions -=- %% #
class StellarBinary():
    # A class to contain binary star systems, which have many special properties
    pass

class System():
    # A generic class for any grouping of objects that together form a stellar system
    pass
