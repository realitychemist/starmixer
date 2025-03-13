import celestial_classes as cc
import imf
import random


def build_star() -> cc.Star:
    startypelist = [cc.MainSequence]
    startype = random.choice(startypelist)
    # mass, age, angular, metallicity
    mass = imf.ChabrierIMF

    pass