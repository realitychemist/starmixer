"""All masses in m_sol."""

import numpy as np
from scipy.integrate import quad


class GenericPowerlaw:
    def __init__(self, gamma: float, a: float, b: float):
        """A generic powerlaw of the form k*x**gamma, normalized by k over the range [a:b] to form a valid PDF.

        :param gamma: The power-law exponent; usually negative in this context.
        :param a: The minimum of the range over which to normalize (a > 0).
        :param b: The maximum of the range over which to normalize (a < b < inf).
        """
        if a <= 0 or b < a or b == np.inf:
            raise ValueError("Invalid bounds of integration.")
        self.gamma = gamma
        self.a = a
        self.b = b
        integrated = quad(lambda x: x**self.gamma, a=self.a, b=self.b)[0]
        self.k = 1/integrated

    def __call__(self, m: float) -> float:
        """Evaluate the power-law IMF for a given input mass.

        :param m: The value at wihch to evaluate the power-law IMF. Must be in the range [a:b] used when constructing.
        :return: The probability of a particular star being of mass m in this power-law distribution.
        """
        if m < self.a or m > self.b:
            raise ValueError(f"m must be in the range [{self.a}:{self.b}].")
        return m**self.gamma * self.k


class SalpeterIMF:
    def __init__(self, a, b):
        """A power-law IMF with a single exponent of -2.35.  Fits well for high-mass stars, but overestimates number
        of low-mass stars in a population.

        :param a: The minimum of the range over which to normalize (a > 0).
        :param b: The maximum of the range over which to normalize (a < b < inf).
        """
        self.gamma = -2.35
        self.a = a
        self.b = b
        self.k = quad(lambda x: x**self.gamma, a=self.a, b=self.b)[0]**-1

    def __call__(self, m: float) -> float:
        """Evaluate the Salpeter IMF for a given input mass.

        :param m: The value at which to evaluate the Salpeter IMF.  Must be in the range [a:b] used when constructing.
        :return: The probability of a particular star being of mass in a Salpeter-distributed population.
        """
        if m < self.a or m > self.b:
            raise ValueError(f"m must be in the range [{self.a}:{self.b}].")
        return m**self.gamma * self.k


class KroupaIMF:
    def __init__(self,
                 gammas: tuple = (-0.3, -1.3, -2.3, -2.3),
                 b: float = np.inf):
        """Piecewise power-law IMF as defined in Kroupa 2001.
        :param gammas: The Kroupa IMF is a piecewise combination of four power-laws, with boundaries at 0.01 (minimum
            valid mass), 0.08, 0.5, and 1 m_sol. Kroupa 2001 estimates the gamma values for each piece to be
            (respectively) -0.3, -1.3, -2.3, and -2.3, but there is an uncertainty associated with each estimate.
            This parameter lets you manually set the gamma values for each piece, by passing a 4-tuple of floats.
            The default behavior is to use the mean values from Kroupa 2001.
        :param b: Kroupa 2001 does not specify an explicit upper bound on mass, so the default behavior is to use an
            infinite upper bound.  However this parameter can be used to explicitly specify a finite upper bound.
        """
        cutoffs = (0.01, 0.08, 0.5, 1)
        self.gammas = gammas
        self.b = b
        # TODO: https://gist.github.com/cgobat/12595d4e242576d4d84b1b682476317d


class ChabrierIMF:
    def __init__(self):
        """IMF based on Chabrier 2003, made up of piecewise power-law and log-normal sections.  Compared with
        KroupaIMF, this gives fewer extremely low- and extremely high-mass bodier.
        """
        cutoffs = (1, )
        # TODO


# def ChabrierIMF(m):
#     """From Chabrier 2003.
#
#     Somewhat more complex than the Kroupa IMF, made up of both power lawn and log normal pieces
#     (gives fewer extremely low / extremely high mass bodies than Kroupa).
#     """
#     cond1 = m <= 1
#     cond2 = (m > 1) & (np.log(m) <= 0.54)
#     cond3 = (np.log(m) > 0.54) & (np.log(m) <= 1.26)
#     cond4 = np.log(m) > 1.26  # Technically only defined up to log(m) <= 1.8, but we'll extrapolate
#
#     imf = np.ones(m.shape)
#     imf[cond1] *= 0.158*np.exp(-(np.log(m[cond1]) - np.log(0.079))**2/(2*0.69**2))
#     # The amplitudes here have been rescaled from the ones presented in Chabrier 2003 in order to
#     #  give a continuous IMF; the values presented in the paper give large discontinuties
#     imf[cond2] *= 0.000181982*m[cond2]**-1.3
#     imf[cond3] *= 0.000606745*m[cond3]**-3.53
#     imf[cond4] *= 0.000101383*m[cond4]**-2.11
#     # Normalize the function across the mass range given
#     imf[:] /= sum(imf)
#     return imf


if __name__ == "__main__":
    # Lowest-mass brown dwarfs are ~ 0.01 m_sol == 13 m_jptr
    # Highest-mass star currently known is ~ 250 m_sol, but max expected at time of formation was ~ 150 m_sol
    imf = SalpeterIMF(0.01, 150)
    masses = np.geomspace(0.01, 150, 1000)
    ps = [imf(m) for m in masses]

    # noinspection PyTypeChecker
    assert np.isclose(quad(imf, 0.01, 150)[0], 1)

    bounds_check_passed = False
    try:
        _ = imf(151)
    except ValueError:
        bounds_check_passed = True
    assert bounds_check_passed is True

    import matplotlib.pyplot as plt  # Inspect plot for reasonableness
    plt.style.use("dark_background")
    plt.plot(masses, ps, "w")
    plt.yscale("log")
    plt.xscale("log")
    plt.title("Power-Law IMF (γ=-2.35, a.k.a. Salpeter)")
    plt.xlabel("Mass :: m_sol")
    plt.ylabel("Probability Density")
    plt.show()
