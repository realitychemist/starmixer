class CelestialBody():
    # Any object in space is a celestial body
    def __init__(self, mass, age):
        self.mass = mass
        self.age = age

# %% -=- Stellar Objects -=- %% #
class Star(CelestialBody):
    # A star is any fusing body sitting near the center of mass of a system
    pass

class MainSequence(Star):
    # Most stars are main sequence stars (this class includes red dwarfs)
    pass

class Subgiant(Star):
    # A star
    pass

class Giant(Star):
    pass

# %% -=- Stellar Remnants -=- %% #
class Remnant(CelestialBody):
    pass

class WhiteDwarf(Remnant):
    pass

class Neutron(Remnant):
    pass

class NovaRemnant(Remnant):
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
    # 
    pass

# %% -=- Constructs (Low Priority) -=- %% #
class Construct(Satellite):
    pass

class DysonSwarm(Construct):
    pass

class DysonSphere(Construct):
    pass

class Topopolis(Construct):
    pass

class Ringworld(Construct):
    pass

class BishopRing(Construct):
    pass

class OrbitalRing(Construct):
    pass

class ONeillCylinder(Construct):
    pass

class SpaceStation(Construct):
    pass

# %% -=- Compositions -=- %% #
class StellarBinary():
    pass

class System():
    pass
