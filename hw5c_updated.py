# region imports
import numpy as np
from scipy.integrate import solve_ivp
from scipy.integrate._ivp.ivp import OdeResult  # Import OdeResult for type hinting
import matplotlib.pyplot as plt


# endregion

# region functions
def ode_system(t: float, X: np.ndarray, *params: tuple) -> list:
    """
    Defines the ODE system for the hydraulic valve dynamics.

    Parameters:
        t (float): Current time (required by solve_ivp but unused in equations).
        X (np.ndarray): State variables [x (position), xdot (velocity), p1, p2].
        params (tuple): Physical constants (A, Cd, ps, pa, V, β, ρ, Kvalve, m, y).

    Returns:
        list: Derivatives [dx/dt, d²x/dt², dp1/dt, dp2/dt].
    """
    # Unpack parameters
    A, Cd, ps, pa, V, beta, rho, Kvalve, m, y = params

    # Unpack state variables
    x, xdot, p1, p2 = X

    # Calculate derivatives (t is unused but required by solve_ivp)
    xddot = (p1 - p2) * A / m
    p1dot = (y * Kvalve * (ps - p1) - rho * A * xdot) * beta / (V * rho)
    p2dot = (-y * Kvalve * (p2 - pa) + rho * A * xdot) * beta / (V * rho)

    return [xdot, xddot, p1dot, p2dot]


def main() -> None:
    """Solves the ODE system and plots results as per HW5_SP25.docx."""
    # Time span and evaluation points
    t_span = (0.0, 0.02)
    t_eval = np.linspace(t_span[0], t_span[1], 200)

    # System parameters (A, Cd, ps, pa, V, beta, rho, Kvalve, m, y)
    myargs = (
        4.909e-4, 0.6, 1.4e7, 1.0e5, 1.473e-4,
        2.0e9, 850.0, 2.0e-5, 30.0, 0.002
    )

    # Initial conditions: [x=0, xdot=0, p1=pa, p2=pa]
    pa = myargs[3]
    ic = [0.0, 0.0, pa, pa]

    # Solve the ODE system (explicitly type-hinted as OdeResult)
    sln: OdeResult = solve_ivp(fun=ode_system, t_span=t_span,y0=ic,args=myargs,t_eval=t_eval, method='RK45' )

    # Plot 1: xdot (velocity) vs. time
    plt.figure(1)
    plt.plot(sln.t, sln.y[1], 'b-', label=r'$\dot{x}$ (Velocity)')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Piston Velocity vs Time')
    plt.grid(True)
    plt.legend()

    # Plot 2: p1 and p2 (pressures) vs. time
    plt.figure(2)
    plt.plot(sln.t, sln.y[2] / 1e5, 'b-', label='$P_1$ (bar)')
    plt.plot(sln.t, sln.y[3] / 1e5, 'r-', label='$P_2$ (bar)')
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (bar)')
    plt.title('Pressure vs Time')
    plt.legend()
    plt.grid(True)
    plt.show()

# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion

#HELPED WITH CHATGPT AND DEEPSEEK