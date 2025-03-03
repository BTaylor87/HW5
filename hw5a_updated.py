# region imports
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# endregion

# region functions
def ff(Re: float, rr: float, CBEQN: bool = False) -> float:
    """
    Calculates the Darcy-Weisbach friction factor (f) based on flow regime.

    Parameters:
        Re (float): Reynolds number.
        rr (float): Relative roughness (ε/D).
        CBEQN (bool): True to use Colebrook equation, False for laminar flow.

    Returns:
        float: Friction factor (f) as a scalar.
    """
    if CBEQN:
        # Define Colebrook equation for turbulent flow
        colebrook_eq = lambda f: 1 / np.sqrt(f) + 2.0 * np.log10((rr / 3.7) + 2.51 / (Re * np.sqrt(f)))
        # Solve for f using fsolve (returns a 1-element ndarray)
        result = fsolve(colebrook_eq, 0.02)  # Initial guess: 0.02
        # Explicitly convert ndarray element to Python float
        return float(result[0])
    else:
        # Laminar flow formula (returns a float for scalar Re)
        return 64.0 / Re


def plotMoody(plotPoint: bool = False, pt: tuple = (0.0, 0.0)) -> None:
    """
    Generates the Moody diagram with laminar, transition, and turbulent flow regimes.
    """
    # Generate Reynolds number ranges
    ReValsCB = np.logspace(np.log10(4000), np.log10(1e8), 200)  # Turbulent
    ReValsL = np.logspace(np.log10(600.0), np.log10(2000.0), 20)  # Laminar
    ReValsTrans = np.logspace(np.log10(2000), np.log10(4000), 20)  # Transition

    # Relative roughness values (ε/D)
    rrVals = np.array([0, 1E-6, 5E-6, 1E-5, 5E-5, 1E-4, 2E-4, 4E-4, 6E-4, 8E-4,
                       1E-3, 2E-3, 4E-3, 6E-3, 8E-8, 1.5E-2, 2E-2, 3E-2, 4E-2, 5E-2])

    # Calculate friction factors
    ffLam = np.array([ff(Re, 0.0) for Re in ReValsL])  # Laminar
    ffTrans = np.array([ff(Re, 0.0) for Re in ReValsTrans])  # Transition (dummy values)
    ffCB = np.array([[ff(Re, rr, True) for Re in ReValsCB] for rr in rrVals])  # Turbulent

    # Plotting (unchanged)
    plt.loglog(ReValsL, ffLam, 'k-', label='Laminar')
    plt.loglog(ReValsTrans, ffTrans, 'k--', label='Transition')
    for idx, rr in enumerate(rrVals):
        plt.loglog(ReValsCB, ffCB[idx], color='k')
        plt.annotate(f"{rr:.1e}", xy=(ReValsCB[-1], ffCB[idx][-1]), ha='left', va='center')

    plt.xlim(600, 1e8)
    plt.ylim(0.008, 0.10)
    plt.xlabel(r"Reynolds Number ($Re$)")
    plt.ylabel(r"Friction Factor ($f$)")
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.show()


def main() -> None:
    """Entry point to generate the Moody diagram."""
    plotMoody()


# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion

#HELPED WITH CHATGPT AND DEEPSEEK