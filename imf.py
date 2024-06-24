"""All masses in m_sol."""

import numpy as np
from scipy.integrate import quad
from itertools import pairwise
from typing import Sequence


class BrokenPowerLaw:
    def __init__(self, gammas: Sequence[float], bounds: Sequence[float]) -> None:
        """A generic broken powerlaw, normalized over the range [bounds[0]:bounds[-1]] to form a valid PDF.

        :param gammas: A sequence of gammas for each section of the power law, in order from low to high inputs.
        :param bounds: A sequence of bounds and breaks: bounds[0] and bounds[-1] are the limits of integration
            for notmalizing the function as a PDF, while all other entries denote the locations of the breaks.
            Should have length len(gammas)+1 and be mSequenceonoSizedtonically increasing.
        """
        if not len(gammas) == len(bounds) - 1:
            raise ValueError(f"len(gammas) must be equal to len(bounds)-1, not len(gammas)={len(gammas)}"
                             f" and len(bounds)={len(bounds)}")
        for first, second in pairwise(bounds):  # Check that bounds are monotonically increasing.
            if first >= second:
                raise ValueError(f"Bounds must be monotonically increasing, not {bounds}")

        self.gammas = gammas
        self.bounds = bounds

        # TODO: This does not currently enforce continuity!  Make that happen...

        integrated = 0
        for g, (l, u) in zip(self.gammas, pairwise(self.bounds)):
            integrated += quad(lambda x: x**g, a=l, b=u)[0]
        self.k = 1/integrated

    def __call__(self, m: float) -> float:
        if m < self.bounds[0] or m > self.bounds[-1]:
            raise ValueError(f"m must be in the range [{self.bounds[0]}:{self.bounds[-1]}]")
        gamma_idx = next(i for i, x in enumerate(self.bounds) if x >= m) - 1
        return m**self.gammas[gamma_idx] * self.k


class Powerlaw(BrokenPowerLaw):
    def __init__(self, gamma: float, a: float, b: float) -> None:
        """A generic powerlaw of the form k*x**gamma, normalized by k over the range [a:b] to form a valid PDF.

        :param gamma: The power-law exponent; usually negative in this context.
        :param a: The minimum of the range over which to normalize (a > 0).
        :param b: The maximum of the range over which to normalize (a < b).
        """
        if a <= 0 or b < a:
            raise ValueError("Invalid bounds of integration.")
        super().__init__(gammas=[gamma], bounds=[a, b])


class SalpeterIMF(Powerlaw):
    def __init__(self, a, b) -> None:
        """A power-law IMF with a single exponent of -2.35.  Fits well for high-mass stars, but overestimates number
        of low-mass stars in a population.

        :param a: The minimum of the range over which to normalize (a > 0).
        :param b: The maximum of the range over which to normalize (a < b < inf).
        """
        super().__init__(gamma=-2.35, a=a, b=b)


class KroupaIMF(BrokenPowerLaw):
    def __init__(self,
                 gammas: Sequence[float] = (-0.3, -1.3, -2.3, -2.3),
                 ub: float = np.inf) -> None:
        """Piecewise power-law IMF as defined in Kroupa 2001.
        :param gammas: The Kroupa IMF is a piecewise combination of four power-laws, with boundaries at 0.01 (minimum
            valid mass), 0.08, 0.5, and 1 m_sol. Kroupa 2001 estimates the gamma values for each piece to be
            (respectively) -0.3, -1.3, -2.3, and -2.3, but there is an uncertainty associated with each estimate.
            This parameter lets you manually set the gamma values for each piece, by passing a sequence of floats.
            The default behavior is to use the mean values from Kroupa 2001.
        :param ub: Kroupa 2001 does not specify an explicit upper bound on mass, so the default behavior is to use an
            infinite upper bound.  However this parameter can be used to explicitly specify a finite upper bound.
        """
        if not len(gammas) == 4:
            raise ValueError(f"KroupaIMF requires exactly 4 gammas, not {len(gammas)}.")
        bounds = [0.01, 0.08, 0.5, 1, ub]
        super().__init__(gammas=gammas, bounds=bounds)


class ChabrierIMF:
    def __init__(self) -> None:
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
    imf = KroupaIMF(ub=150)
    masses = np.geomspace(0.01, 150, 1000)
    ps = [imf(m) for m in masses]

    # noinspection PyTypeChecker
    assert np.isclose(quad(imf, 0.01, 150, limit=200)[0], 1)

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
    plt.title("Power-Law IMF (Kroupa)")
    plt.xlabel("Mass :: m_sol")
    plt.ylabel("Probability Density")
    plt.show()
