from os import path
from pandas import DataFrame, read_csv
from bisect import bisect_left

with open(path.relpath("blackbody_teff_hex.csv")) as infile:
    _blackbody_color_lookup = read_csv(infile, names=["effective_temp", "color_hex"])


def color_match(T_eff):
    """Uses a lookup table to find the closest matching hex color for a given effective temperature.

    Parameters
    ----------
    T_eff : float
        The effective temperature, in solar units

    Returns
    -------
    string
        A string containing an rgb color in standard hexadecminal notation
    """
    _T_sol = 5772  # Kelvin
    temp = T_eff * _T_sol

    idx = bisect_left(_blackbody_color_lookup["effective_temp"], temp)  # Relies on effective_temp being sorted!
    return _blackbody_color_lookup.iloc[idx]["color_hex"]