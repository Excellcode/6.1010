################################################################################
# CSE.C20
# Problem Set 1: lander
# Name: excell
# Collaborators: none

import math
import matplotlib.pyplot as plt
from IVPlib_pset1 import IVP
import IVPlib_pset1 as IVPlib


################################################################################
## Lander class definition (a subclass of IVP)
################################################################################


class LanderIVP(IVP):

    def evalf(self, u, t):
        """
        Calculates forcing for a Martian lander given the current state and time.

        Args:
            u (float list): current state
            t (float): current time

        Returns:
            f (float list): current forcing
        """
        #### BEGIN SOLUTION ####
        
        A_l = self.get_p("A_l")
        CD_l = self.get_p("CD_l")
        m_l = self.get_p("m_l")
       
        A_p = self.get_p("A_p")
        CD_p = self.get_p("CD_p")
        V_p = self.get_p("V_p")
        
        V =u[0]
        z = u[1]
        dict= self.atmosphere(z)
        g = dict['g']
        p_a = dict["rhoa"]
        f = []
        theta_e = self.get_p("theta_e")
        theta_p = self.get_p("theta_p")
        D_l = 0.5*p_a*V**2*A_l*CD_l
        D_p = 0.5*p_a*V**2*A_p*CD_p
        
        if V > V_p:
            D = D_l
            theta = theta_e
        else:
            D = D_l + D_p 
            theta = theta_p   
        theta = math.radians(theta)
        f.append(g*math.cos(theta) - D/m_l)
        f.append(-V*math.cos(theta))
        return f
        #### END SOLUTION ####

    def atmosphere(self, z):
        """
        Returns in a dictionary the properties of the Martian atmosphere at the
        altitude z (assumed in meters). Currently, the properties returned are:
            'Ta': temperature (K)
            'pa': pressure (kPa)
            'rhoa': density (kg/m^3)
            'g': gravity (m/s^2)

        Args:
            z (float): altitude in meters

        Returns:
            props (dictionary): property keys and values
        """
        if z > 7000:
            Ta = 235 - 0.00108*(z-7000) # K
        else:
            Ta = 235 - 0.00222*(z-7000) # K
        pa = 0.699*math.exp(-0.00009*z) # kPa
        rhoa = pa / (0.1921*Ta) # kg/m^3

        G = 6.674e-11 # gravitational constant (m^3/ kg/s^2)
        Mm = 6.41693e23 # mass of Mars (kg)
        Rm = 3389.5*1000 # radius of Mars (m)
        g = G*Mm / (Rm+z)**2 # m/s^2

        props = {}
        props['Ta'] = Ta
        props['pa'] = pa
        props['rhoa'] = rhoa
        props['g'] = g
        return props


################################################################################
## Functions to solve Martian lander trajectory IVP
################################################################################


def lander_Vzaplot(t, V, z, a, method='numerical'):
    """
    Produces a single figure with subplots of:
        * velocity vs. time
        * z vs. time
        * acceleration vs. time
    The figure will be labeled with the method name.

    Args:
        t (float list): time values t[n]
        V (float list): velocity values from numerical method, V[n] (in m/s)
        z (float list): z values from numerical method, z[n] (in km)
        a (float list): acceleration values from numerical method, a[n] (in m/s**2)
        method (string, optional): name of the numerical method used to generate results

    Returns:
        axs (array of Axes): handle to the Axes objects that comprise the figure's subplots
    """
    #### BEGIN SOLUTION ####
    fig, axs = plt.subplots(3,1)
    
    #first subplot
    axs[0].plot(t, V, 'bo', label = method)
    
    axs[0].set_ylabel("V (m/s)")
   
    axs[0].legend()
   

    #2nd subplot
    axs[1].plot(t, z, 'bo')
    axs[1].set_ylabel("z (km)")
    
    #3rd subplot
    axs[2].plot(t, a, 'bo')
    axs[2].set_ylabel("a (m/s^2)")
    axs[2].set_xlabel("t (sec)")
    
    return axs
    #### END SOLUTION ####


def lander_run_case(lander_IVP, dt, mlist):
    """
    Solves the Martian lander problem described in lander_IVP with a timestep dt for
    the methods in mlist. For each method in mlist, this function will:
        * plot the solution by calling lander_Vzaplot
        * print the time (in sec) and altitude (in km) at which the parachute deployed
        * print the altitude (in km) and velocity (in m/s) at the final time

    Args:
        lander_IVP (IVP object): describes IVP case to be simulated
        dt (float): timestep
        mlist (function list): list of numerical methods to run on case

    Returns:
        results (dictionary): maps each method name to a tuple of three elements:
            * the Axes objects in the figure corresponding to that method
            * the time of parachute deployment
            * the altitude (z) at which deployment occurred
    """
    #### BEGIN SOLUTION ####
    results = {}

    for method in mlist:
        t, u = IVPlib.solve(lander_IVP, dt, method)
        V = []
        z = []
        a = []
        time_p = -1
        for i in range(len(t)):
            V.append(u[i][0])
            z.append(u[i][1]/1000.0)
            a.append((lander_IVP.evalf(u[i], t[i]))[0])
            if V[i] <= lander_IVP.get_p("V_p"):
                if time_p == -1:
                    time_p = t[i]
                    z_p =z[i]
                
    
        

        mname = method.__name__
        print(f"Method: {mname}\n")
        print(f"parachute deployed at t, z: {time_p: .2e} s, {z_p: .2e} km \n")
        print(f"Final z, V: {z[-1]: .2e} km, {V[-1]: .2e} m/s")

    
        axs = lander_Vzaplot(t, V, z, a, mname)
        results[mname] = (axs, time_p, z_p)

    return results
    #### END SOLUTION ####


if __name__ == '__main__':
    uI = [5800.0, 125*1000.0] # Initial velocity (m/s) and altitude (m)
    tI = 0
    tF = 300.0 # s

    p = {}
   
    p['m_l'] = 3300.0 # kg
    p['V_p'] = 470.0 # parachute deploy velocity (m/s)
    p['A_l'] = 15.9 # m^2
    p['CD_l'] = 1.7
    p['A_p'] = 201.0 # m^2
    p['CD_p'] = 1.2
    p['theta_e'] = 83.0 # flight path angle during entry, in degrees
    p['theta_p'] = 70.0 # flight path angle during parachute, in degrees

    lander_IVP = LanderIVP(uI, tI, tF, p)

    # Set up which method(s) to run
    mlist = [IVPlib.step_RK4]

    # Simulate a single case to demonstrate basic behavior of methods with dt=0.1 s
    lander_run_case(lander_IVP, 0.1, mlist)

    plt.show()
