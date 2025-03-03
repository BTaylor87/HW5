# region imports
import hw5a_updated as pta
import random as rnd
from matplotlib import pyplot as plt
# endregion

# region functions
def ffPoint(Re, rr):
    """
    This function takes Re and rr as parameters and outputs a friction factor according to the following:
    1.  if Re>4000 use Colebrook Equation
    2.  if Re<2000 use f=64/Re
    3.  else calculate a probabilistic friction factor where the distribution has a mean midway between the prediction
        of the f=64/Re and Colebrook Equations and a standard deviation of 20% of this mean
    :param Re:  the Reynolds number
    :param rr:  the relative roughness
    :return:  the friction factor
    """
    if Re >= 4000:
        return pta.ff(Re, rr, CBEQN=True)
    if Re <= 2000:
        return pta.ff(Re, rr)
    CBff = pta.ff(4000, rr, CBEQN=True)
    Lamff = 64 / 2000
    mean = Lamff + (CBff - Lamff) * (Re - 2000) / 2000
    sig = 0.2 * mean
    return rnd.normalvariate(mean, sig)

def PlotPoint(Re, f):
    pta.plotMoody(plotPoint=True, pt=(Re, f))

def main():
    while True:
        Re = float(input("Enter the Reynolds number: "))
        rr = float(input("Enter the relative roughness: "))
        f = ffPoint(Re, rr)
        PlotPoint(Re, f)
        if input("Enter another set? (y/n): ").lower() != 'y':
            break
# endregion


# region function calls
if __name__ == "__main__":
    main()
# endregion

#HELPED WITH CHATGPT AND DEEPSEEK