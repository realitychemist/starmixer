import blackbody
from numpy import log10

"""Most units are relative solar units (mass, radius, angular velocity, luminosity, etc...).  The exceptions are
time which uses log(Myr) units -- 0 is 1 Myr, 1 is 10 Myr, 2 is 100 Myr, etc -- and metallicity, which uses Z 
units (mass fraction of elements hevier than helium). Color uses hex-RGB encoding."""


class CelestialBody:
    # Any object in space is a celestial body
    def __init__(self, mass, age, angular):
        self.mass = mass  # m_sol
        self.age = age  # log(Myr)
        if 10**self.age > 13800:  # Max age sanity check
            raise ValueError(f"Object age {10**self.age} Myr greater than age of universe 13800 Myr.")
        self.angular = angular  # l_sol (not to be confused with luminosity)


# %% -=- Stellar Objects -=- %% #
class Star(CelestialBody):
    # A star is any fusing body sitting near the center of mass of a system
    def __init__(self, mass, age, angular, metallicity):
        super(Star, self).__init__(mass, age, angular)
        self.metallicity = metallicity  # Z


class MainSequence(Star):
    # Most stars are main sequence stars (this class includes red dwarfs)
    def __init__(self, mass, age, angular, metallicity):
        super(MainSequence, self).__init__(mass, age, angular, metallicity)
        self.lifetime = log10(self.mass**-2.5 * 10**4)  # log(Myr)
        if self.age > self.lifetime:  # Star should no longer be on the main sequence; pass out an error
            raise ValueError(f"Star age {10**self.age} Myr greater than"
                             f"main sequence lifetime {10**self.lifetime} Myr")
        self.temperature = (mass**2.5)**-4  # T_sol
        self.color = blackbody.visible_color(self.temperature)  # RGB hexadecimal
        self.spectrum = blackbody.spectrum(self.temperature)
        self.radius = mass**0.5  # r_sol
        self.luminosity = mass**3.5  # lum_sol (not to be confused with angular momentum)
        self.rotation = self.angular/(self.mass * self.radius**2)  # tau_sol; 2/5 inertial factor cancels


class Giant(Star):
    # A star past the main sequence part of its life (or that skipped it)
    raise NotImplementedError


class WolfRayet(Giant):
    # A peculiar type of giant characterized by extremely high temperature and strong stellar wind
    raise NotImplementedError


# %% -=- Stellar Remnants -=- %% #
class Remnant(CelestialBody):
    # The remains of a body that was once a star
    raise NotImplementedError


class WhiteDwarf(Remnant):
    # A relatively cool stellar remnant, usually of fairly low mass
    raise NotImplementedError


class Neutron(Remnant):
    # The remnants of a massive star that has undergone a supernova
    raise NotImplementedError


class Pulsar(WhiteDwarf, Neutron):
    # A neutron star (sometimes a white dwarf) that projects energetic beams from its poles
    raise NotImplementedError


class Magnetar(Neutron):
    # A type of nuetron star with a strong magnetic field that periodically bursts with radiation
    raise NotImplementedError


class BlackHole(Remnant):
    # The remnant of a massize star (usually), from which no light can escape
    raise NotImplementedError


# %% -=- Non-Stellar Objects -=- %% #
class Protostar(CelestialBody):
    # A protostar is an mass of gas and space dust in the process of collapsing
    raise NotImplementedError


class PreMainSequence(CelestialBody):
    # A coalesced body older than a protostar, but which has not yet reached ZAMS
    raise NotImplementedError


class BrownDwarf(CelestialBody):
    # A small body which is almost -- but not quite -- massive enough to undergo fusion
    raise NotImplementedError


class Satellite(CelestialBody):
    # Any body in orbit around another body
    raise NotImplementedError


class AccretionDisk(Satellite):
    # A disk of debris remaing from stellar formation in the process of forming a planet
    raise NotImplementedError


class Planet(Satellite):
    # A rocky or gasseous body in orbit around a star-like object
    raise NotImplementedError


class Moon(Satellite):
    # A rocky stellite of a planet
    raise NotImplementedError


class Asteroid(Satellite):
    # Small rocky or icy bodies in orbit around a star-like object (or captured in a L point)
    raise NotImplementedError


class Comet(Satellite):
    # Icy body that trails a tail when passing near a star; orbit is usually highly eliptical
    raise NotImplementedError


# %% -=- Constructs (Low Priority) -=- %% #
class Construct(Satellite):
    # Any non-naturally occuring celestial body in orbit around a star or remnant
    raise NotImplementedError


class DysonSwarm(Construct):
    # Many small satellites around a star, intended to harvest energy
    raise NotImplementedError


class DysonSphere(Construct):
    # A shell constructed around a star intended to harvest energy
    raise NotImplementedError


class Topopolis(Construct):
    # A massive (stellar-scale) habitat construct, like many O'Neil cylinders joined together
    raise NotImplementedError


class NivenRing(Construct):
    # A stellar scale rotating torroidal habitat
    raise NotImplementedError


class BishopRing(Construct):
    # A planetary scale rotating rorroidal habitat in orbit around a star or remnant
    raise NotImplementedError


class ShellWorld(Construct):
    # Any of several types of hollow, planet or asteroid scale habitats orbiting a star or remnant
    raise NotImplementedError


class OrbitalRing(Construct):
    # A torroidal habitat encircling (or partly encircling) a planet or moon
    raise NotImplementedError


class ONeillCylinder(Construct):
    # An orbital scale habitat formed from a rotating cylinder
    raise NotImplementedError


class SpaceStation(Construct):
    # Any small-scale habitat in orbit around a planet, moon, asteroid, star, etc...
    raise NotImplementedError


# %% -=- Compositions -=- %% #
class StellarBinary:
    # A class to contain binary star systems, which have many special properties
    raise NotImplementedError


class System:
    # A generic class for any grouping of objects that together form a stellar system
    raise NotImplementedError
