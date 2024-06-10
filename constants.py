"""Conversion factors to/from nominal solar units, plus some other useful constants and conversion factors."""
from numpy import pi

m_sol = 1.988e30  # Nominal solar mass, kilograms
r_sol = 6.957e8  # Nominal solar radius, meters
lum_sol = 3.828e26  # Nominal solar luminosity, watts
t_sol = 5772  # Nominal solar effective temperature, kelvin
tau_sol = 2*pi/24.47  # Mean solar sidereal period, rad/day
l_sol = (2/5) * m_sol * r_sol**2  # Solar moment of intertia (solid sphere approximation), kilogram meters-squared
grav = 6.674e-11  # Gravitational constant, newton meters-squared per kilogram-squared
