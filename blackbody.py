from os import path
import numpy as np
import pandas as pd
from bisect import bisect_left
from constants import t_sol
from matplotlib.patches import Patch
import matplotlib
import matplotlib.pyplot as plt
from scipy.constants import c, h, k
# Constant units are: c :: m/s
#                     h :: J/Hz
#                     k :: J/K


def visible_color(t_eff: float) -> str:
    """Get visible color for a blackbody of the given effective temperature.

    :param t_eff: The effective temperature, in solar units (i.e. 1 = 5772 K).
    :return: The visible color, in standard hex-rgb notation (i.e. #rrggbb).
    """
    temp = t_eff * t_sol  # Kelvin

    with open(path.relpath("blackbody_teff_hex.csv")) as infile:
        blackbody_color_lookup = pd.read_csv(infile, names=["Effective Temperature", "Color"])

    idx = bisect_left(blackbody_color_lookup["Effective Temperature"], temp)  # Relies on effective_temp being sorted
    return blackbody_color_lookup.iloc[idx]["Color"]


def spectrum(t_eff: float,
             maxwav: float or None = None) -> pd.DataFrame:
    """Get the irradiance spectrum for a blackbody of given effective temperature.

    :param t_eff: The effective temperature, in solar units (i.e. 1 = 5772 K).
    :param maxwav: Maximum wavelength (nanometers) to be returned in the spectrum. If None (default), the maximum
    wavelength is determined automatically.
    :return: A DataFrame containing the irradiance at each wavelength sampled, and the corresponding wavelengths.
    """
    temp = t_eff * t_sol  # Kelvin

    if maxwav is not None:
        autoscale = False
    else:
        autoscale = True
        maxwav = 10000  # Conservative deafult

    wavs_nm = np.linspace(10, maxwav, 10000)
    wavs_m = [w*1e-9 for w in wavs_nm]  # m

    def irradiance_at_wavelength(w, t):
        return 2*h*(c**2)*(w**-5) * (np.exp((h*c)/(w*k*t))-1)**-1 * 1e-9  # W/(m^2 nm sr)
    irradiances = [irradiance_at_wavelength(w, temp) for w in wavs_m]

    df = pd.DataFrame(data={"Irradiance": irradiances, "Wavelength": wavs_nm})

    if autoscale:
        peak_idx = df["Irradiance"].idxmax()
        peak = df.iloc[peak_idx]["Irradiance"]
        irradiance_thresh = peak/30  # Just hard-coding a value that usually looks nice
        # We generally only want to crop off the long right-hand-side tail, so first split at the peak
        df_left = df.iloc[:peak_idx+1]
        df_right = df.iloc[peak_idx:]
        df_right = df_right[df_right["Irradiance"] >= irradiance_thresh]
        df = pd.concat([df_left, df_right])

    return df


def spectrum_plot(t_eff: float, maxwav: float or None = None) -> plt.figure:
    """Automatic pretty-plotting for the spectrum of a blackbody. Visible range is color-coded (with alpha-falloff
    outside visible range), the peak wavelength is labeled, and a patch shows the overall color of the blackbody.

    :param t_eff: The effective temperature of the blackbody, in solar units (i.e. 1 = 5772 K).
    :param maxwav: Maximum wavelength (nanometers) to be returned in the spectrum. If None (default), the maximum
        wavelength is determined automatically.
    :return: The figure containing the spectrum plot. Some aspects (e.g. figure title) are not set, and expect you
        to set them yourself before showing or saving.
    """
    spect = spectrum(t_eff, maxwav)
    overall_color = visible_color(t_eff)

    def wavelength_to_rgba(w: float) -> tuple[float, float, float]:
        """Convert wavelength (in nm) to an RGBA color. Wavelengths outside the visible spectrum keep the color of
        that end (so either red or violet), but fall off toward an alpha of 0 over 50 nm.

        :param w: The wavelength, in nanometers.
        :return: The RGB color, as a tuple (values for each component range from 0 to 1).
        """
        if 380 <= w <= 440:  # Indigos / violets
            x = 0.3 + 0.7*(w-380) / (440-380)
            r = ((-(w-440) / (440-380)) * x)**0.8
            g = 0
            b = x**0.8
        elif 440 <= w <= 490:  # Blues
            r = 0
            g = ((w-440) / (490-440))**0.8
            b = 1
        elif 490 <= w <= 510:  # Greens
            r = 0
            g = 1
            b = (-(w-510)/(510-490))**0.8
        elif 510 <= w <= 580:  # Yellows
            r = ((w-510) / (580-510))**0.8
            g = 1
            b = 0
        elif 580 <= w <= 645:  # Oranges
            r = 1
            g = (-(w-645) / (645-580))**0.8
            b = 0
        elif 645 <= w <= 750:  # Reds
            x = 0.3 + 0.7*(750-w) / (750-645)
            r = x**0.8
            g = 0
            b = 0
        else:  # Error state, defualt black
            r, g, b = 0, 0, 0

        return r, g, b

    with plt.style.context("dark_background"):
        norm = plt.Normalize(380, 750, clip=False)
        wls = np.arange(380, 751, 2)
        colors = list(zip(norm(wls), [wavelength_to_rgba(w) for w in wls]))
        spectral_map = matplotlib.colors.LinearSegmentedColormap.from_list("spectral_map", colors)
        spectral_map.set_extremes(under=(0.3**0.8, 0, 0.3**0.8, 0.33), over=(0.3**0.8, 0, 0, 0.33))

        ymax = np.max(spect["Irradiance"]) * 1.1
        ys = np.linspace(0, ymax, 10)
        extent = (np.min(spect["Wavelength"]), np.max(spect["Wavelength"]),
                  np.min(spect["Irradiance"]), ymax)

        fig, ax = plt.subplots()
        ax.imshow(np.array(spect["Wavelength"]).reshape(1, len(spect["Wavelength"])),
                  clim=(380, 750), extent=extent, cmap=spectral_map, aspect="auto", alpha=None)
        ax.set_ylim(0, ymax)
        ax.plot("Wavelength", "Irradiance", data=spect, linewidth=2, color="white")
        ax.fill_between(spect["Wavelength"], spect["Irradiance"], ymax, color="black")

        ax.legend(handles=[Patch(facecolor=overall_color, edgecolor=overall_color,
                                 label=f"Approximate visible color: {overall_color}")],
                  loc="upper right", markerfirst=False, frameon=False, handlelength=2, handleheight=1.236)
        ax.set_xlabel("Wavelength :: nm")
        ax.set_ylabel("Irradiance :: W/(m^2 nm sr)")
    return fig


if __name__ == "__main__":  # Quick and dirty tests
    assert visible_color(1) == "#fdfbff"
    solspec = spectrum(1)
    assert np.isclose(solspec.iloc[solspec["Irradiance"].idxmax()]["Wavelength"], 502, atol=1)

    # Check plot for reasonableness
    fig = spectrum_plot(1)
    fig.canvas.draw()
    fig.suptitle("Blackbody Approximation to Sol's Spectrum", c="w")
    plt.show()
