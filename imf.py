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
            Should have length len(gammas)+1 and be monotonically increasing.
        """
        if not len(gammas) == len(bounds) - 1:
            raise ValueError(f"len(gammas) must be equal to len(bounds)-1, not len(gammas)={len(gammas)}"
                             f" and len(bounds)={len(bounds)}")
        for first, second in pairwise(bounds):  # Check that bounds are monotonically increasing.
            if first >= second:
                raise ValueError(f"Bounds must be monotonically increasing, not {bounds}")

        self.gammas = gammas
        self.bounds = bounds

        # Enforce continuity
        self.cs = [1]
        for i, bound in enumerate(self.bounds[1:-1]):
            left = self.cs[i]*bound**self.gammas[i]
            right = bound**self.gammas[i+1]
            self.cs.append(left/right)

        integrated = 0
        for g, (l, u), c in zip(self.gammas, pairwise(self.bounds), self.cs):
            integrated += quad(lambda x: c*x**g, a=l, b=u)[0]
        self.k = 1/integrated

    def __call__(self, m: float) -> float:
        if m < self.bounds[0] or m > self.bounds[-1]:
            raise ValueError(f"m must be in the range [{self.bounds[0]}:{self.bounds[-1]}]")
        coeff_idx = next(i for i, x in enumerate(self.bounds) if x >= m) - 1
        return self.cs[coeff_idx]*m**self.gammas[coeff_idx] * self.k


class PowerLaw(BrokenPowerLaw):
    def __init__(self, gamma: float, a: float, b: float) -> None:
        """A generic powerlaw of the form k*x**gamma, normalized by k over the range [a:b] to form a valid PDF.

        :param gamma: The power-law exponent; usually negative in this context.
        :param a: The minimum of the range over which to normalize (a > 0).
        :param b: The maximum of the range over which to normalize (a < b).
        """
        if a <= 0 or b < a:
            raise ValueError("Invalid bounds of integration.")
        BrokenPowerLaw.__init__(self, gammas=[gamma], bounds=[a, b])


class LogNormal:
    def __init__(self, pf: float, u: float, v: float, a: float, b: float) -> None:
        """A generic log-normal of the form k*pf/m*exp(-1*((log(m)-log(u))**2/(2*v**2)), normalized by k over the
        range [a:b] to form a valid PDF.

        :param pf: Log-normal prefactor.
        :param u: Interior log coefficient.
        :param v: Interior divisor coefficient.
        :param a: The minimum of the range over which to normalize (a > 0).
        :param b: The maximum of the range over which to normalize (a < b).
        """
        self.pf, self.u, self.v, self.a, self.b = pf, u, v, a, b

        integrated = quad(lambda x: (1/x)*self.pf * np.exp(-1*(np.log(x)-np.log(self.u))**2/(2*self.v**2)),
                          a=self.a, b=self.b)[0]
        self.k = 1 / integrated

    def __call__(self, m: float) -> float:
        if m < self.a or m > self.b:
            raise ValueError(f"m must be in the range [{self.a}:{self.b}]")
        return self.k*self.pf*(1/m) * np.exp(-1*(np.log(m)-np.log(self.u))**2/(2*self.v**2))


class SalpeterIMF(PowerLaw):
    def __init__(self, a, b) -> None:
        """A power-law IMF with a single exponent of -2.35.  Fits well for high-mass stars, but overestimates number
        of low-mass stars in a population.

        :param a: The minimum of the range over which to normalize (a > 0).
        :param b: The maximum of the range over which to normalize (a < b < inf).
        """
        PowerLaw.__init__(self, gamma=-2.35, a=a, b=b)


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
        BrokenPowerLaw.__init__(self, gammas=gammas, bounds=bounds)


class ChabrierIMF:
    def __init__(self, pf: float = 0.158/np.log(10),
                 u: float = 0.079,
                 v: float = 1,
                 ub: float = np.inf) -> None:
        """Log-normal below m = 1 Msol, and power-law (Salpeter) above. Compared to KroupaIMF, this gives fewer
        extremely low mass stars.

        :param pf: Prefactor for the log-normal part. Chabrier gives 0.158/ln(10) with some uncertainty.
        :param u: Interior log coefficient for the log-normal part. Chabrier gives 0.079 with some uncertainty.
        :param v: Interior divisor coefficient for the log-normal part. Chabrier gives 0.69 with some uncertainty.
        :param ub: Kroupa 2001 does not specify an explicit upper bound on mass, so the default behavior is to use an
            infinite upper bound.  However this parameter can be used to explicitly specify a finite upper bound.
        """
        self.pf, self.u, self.v, self.ub = pf, u, v, ub
        self.lognorm_part = LogNormal(self.pf, self.u, self.v, 0.01, 1)
        self.powerlaw_part = SalpeterIMF(1, ub)

        integrated = quad(lambda x: self.lognorm_part(x), a=0.01, b=1)[0]
        left = self.lognorm_part(1)
        right = self.powerlaw_part(1)
        self.c = left/right
        integrated += quad(lambda x: self.c*self.powerlaw_part(x), a=1, b=self.ub)[0]
        self.k = 1/integrated

    def __call__(self, m: float) -> float:
        if m < 0.01 or m > self.ub:
            raise ValueError(f"m must be in the range [0.01:{self.ub}]")
        elif m <= 1:
            return self.k*self.lognorm_part(m)
        elif m >= 1:
            return self.k*self.c*self.powerlaw_part(m)



if __name__ == "__main__":
    # Lowest-mass brown dwarfs are ~ 0.01 m_sol == 13 m_jptr
    # Highest-mass star currently known is ~ 250 m_sol, but max expected at time of formation was ~ 150 m_sol

    imf = ChabrierIMF(ub=150)
    masses = np.geomspace(0.01, 150, 1000)
    ps = [imf(m) for m in masses]

    # noinspection PyTypeChecker
    assert np.isclose(quad(imf, 0.01, 150, limit=200)[0], 1)

    bounds_check_passed = False
    try:
        _ = imf(151)
    except ValueError:
        bounds_check_passed = True
    assert bounds_check_passed

    import matplotlib.pyplot as plt  # Inspect plot for reasonableness
    plt.style.use("dark_background")
    plt.plot(masses, ps, "w")
    plt.yscale("log")
    plt.xscale("log")
    plt.title("IMF (Chabrier 2003)")
    plt.xlabel("Mass :: m_sol")
    plt.ylabel("Probability Density")
    plt.show()
