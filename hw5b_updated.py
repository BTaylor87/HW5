# region imports
import hw5a_updated as pta
import random as rnd
from matplotlib import pyplot as plt
import math


# endregion

# region functions
def transition_f(Re, rr):
    """
    Returns a friction factor in the transition region (2000 < Re < 4000)
    by linearly interpolating between laminar and turbulent (Colebrook)
    friction factors, then sampling from a normal distribution centered
    at that interpolation with 20% standard deviation.
    """
    # Friction factor using Colebrook:
    f_cb = pta.ff(Re, rr, CBEQN=True)

    # Friction factor using laminar equation (f=64/Re in pta.ff):
    f_lam = pta.ff(Re, rr, CBEQN=False)

    # Linear interpolation in [2000, 4000]
    # fraction = how far Re is between 2000 and 4000
    fraction = (Re - 2000) / 2000

    # Mean friction factor in transition
    mean_f = f_lam + (f_cb - f_lam) * fraction

    # Standard deviation
    sigma_f = 0.2 * mean_f

    # Sample from normal distribution
    return rnd.normalvariate(mean_f, sigma_f)


def ffPoint(Re, rr):
    """
    Overall friction factor function:
      - If Re >= 4000: use Colebrook
      - If Re <= 2000: use laminar
      - Otherwise: interpolate + randomness (transition_f).
    """
    if Re >= 4000:
        return pta.ff(Re, rr, CBEQN=True)
    elif Re <= 2000:
        return pta.ff(Re, rr)  # laminar
    else:
        return transition_f(Re, rr)


def PlotPoint(Re, f, transition=False):
    """
    Plots a point on the Moody chart.
    Uses an upward triangle if transition=True, else a circle.
    """
    marker = "^" if transition else "o"
    pta.plotMoody(plotPoint=True, pt=(Re, f), marker=marker)


def moody_app():
    """
    Main application loop:
    1. Prompts the user for diameter, roughness, flow rate (gpm)
    2. Computes friction factor and head loss per foot
    3. Plots each point on the Moody diagram
    4. Continues until user enters 'q'.
    """

    while True:
        # Gather inputs
        d_in_str = input("Enter pipe diameter [inches] or 'q' to quit: ")
        if d_in_str.lower() == 'q':
            print("Exiting application.")
            break

        epsilon_mic_str = input("Enter pipe roughness epsilon [micro-inches] or 'q' to quit: ")
        if epsilon_mic_str.lower() == 'q':
            print("Exiting application.")
            break

        Q_gpm_str = input("Enter flow rate [gal/min] or 'q' to quit: ")
        if Q_gpm_str.lower() == 'q':
            print("Exiting application.")
            break

        # Convert user inputs into floats
        try:
            d_in = float(d_in_str)
            epsilon_mic = float(epsilon_mic_str)
            Q_gpm = float(Q_gpm_str)
        except ValueError:
            print("Invalid numeric input; please try again.\n")
            continue

        # Convert diameter from inches to feet
        d_ft = d_in / 12.0

        # Convert roughness from micro-inches to feet
        epsilon_in = epsilon_mic * 1e-6  # convert micro-inches to inches
        epsilon_ft = epsilon_in / 12.0  # convert inches to feet

        # Flow area in ft²
        area = math.pi * (d_ft ** 2) / 4.0

        # Convert GPM (gal/min) to ft³/s
        # 1 gallon = 0.133681 ft³, 1 min = 60 s
        Q_cfs = Q_gpm * 0.133681 / 60.0

        # Velocity in ft/s
        if area == 0:
            print("Invalid diameter (zero). Please try again.\n")
            continue
        v = Q_cfs / area

        # Kinematic viscosity (water ~60°F) in ft²/s (approx)
        nu = 1.217e-5

        # Reynolds number
        Re = v * d_ft / nu

        # Relative roughness
        rr = epsilon_ft / d_ft

        # Friction factor
        f = ffPoint(Re, rr)

        # Check for transition flow
        in_transition = (2000 < Re < 4000)

        # Darcy-Weisbach head loss per foot (hf/L)
        #   hf = f * (L/d) * (v² / (2g))
        #   => hf/L = f * (v²/(2g)) * (1/d)
        g = 32.174  # ft/s²
        hf_per_L = f * (v ** 2 / (2.0 * g)) * (1.0 / d_ft)

        # Display the results
        print("=============================================")
        print(f"Diameter [in]:            {d_in:.4g}")
        print(f"Roughness [micro-inches]: {epsilon_mic:.4g}")
        print(f"Flow rate [gpm]:          {Q_gpm:.4g}")
        print(f"Reynolds number:          {Re:.5g}")
        print(f"Relative roughness:       {rr:.6g}")
        print(f"Friction factor (f):      {f:.5g}")
        print(f"hf/L [ft/ft]:             {hf_per_L:.6g}")
        print("=============================================\n")

        # Plot this data point on the Moody diagram
        PlotPoint(Re, f, transition=in_transition)


# endregion

# region function calls
if __name__ == "__main__":
    moody_app()
# endregion

#HELPED WITH CHATGPT AND DEEPSEEK