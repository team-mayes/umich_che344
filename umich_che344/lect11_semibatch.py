# !/usr/bin/env python
# coding=utf-8
"""
Demo to integrate an ODE for ChE 344; A <--> 3B + C, membrane reactor with pressure drop, B diffusing out the membrane
references:
     https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html
     https://scipy.github.io/old-wiki/pages/Cookbook/CoupledSpringMassSystem.html
"""
from __future__ import print_function
import sys
import numpy as np
from scipy.integrate import odeint
from common import make_fig, GOOD_RET


__author__ = 'hbmayes'


def sys_odes_ca(y_vector, time, vol_0, nu_in, ca_in):
    # put here any equations you need to calculate the differential equations (R.H.S.s of dy/dW)
    ca, cb, cc, cd = y_vector

    vol = vol_0 + nu_in * time
    r = 2.2 * ca * cb
    dca_dt = nu_in * (ca_in - ca) / vol - r
    dcb_dt = - nu_in * cb / vol - r
    dcc_dt = - nu_in * cc / vol + r
    dcd_dt = - nu_in * cd / vol + r

    return [dca_dt, dcb_dt, dcc_dt, dcd_dt]


def sys_odes_na(y_vector, time, vol_0, nu_in, ca_in):
    # put here any equations you need to calculate the differential equations (R.H.S.s of dy/dW)
    na, nb, nc, nd = y_vector

    vol = vol_0 + nu_in * time
    ca = na/vol
    cb = nb/vol
    r = 2.2 * ca * cb
    fa_in = ca_in * nu_in  # mol/L * L/s = mol/s, good!
    dna_dt = fa_in - r * vol
    dnb_dt = -r * vol
    dnc_dt = r * vol
    dnd_dt = r * vol

    return [dna_dt, dnb_dt, dnc_dt, dnd_dt]


def solve_ode_sys():
    # initial values
    vol_0 = 5.  # L
    cb_0 = 0.05  # mol/L
    c_initial_all = [0., cb_0, 0., 0.]

    ca_in = 0.025  # mol/L
    nu_in = 0.05  # L/s

    # Give an initial independent variable through a final one. We don't know the final needed yet; if we guess
    # too small and we don't get the conversion we want, we can always increase it and run the program again
    t_min = 0
    t_max = 400.0
    time = np.linspace(t_min, t_max, 1001)

    # def sys_odes_ca(y_vector, time, vol_0, nu_in, ca_in):
    sol = odeint(sys_odes_ca, c_initial_all, time, args=(vol_0, nu_in, ca_in))
    ca = sol[:, 0]
    cb = sol[:, 1]
    cc = sol[:, 2]
    cd = sol[:, 3]

    name = 'lect_11_semibatch'
    make_fig(name+"_ca", time, ca, y1_label="$C_A$", y2_array=cb, y2_label="$C_B$",
             y3_array=cc, y3_label="$C_C$", y4_array=cd, y4_label="$C_D$", x_label="time (s)",
             y_label="concentration (mol/L)",
             x_lima=t_min, x_limb=t_max, y_lima=-0.01, y_limb=0.05
             )

    # def sys_odes_na(y_vector, time, vol_0, nu_in, ca_in):
    na_initial_all = [0, cb_0 * vol_0, 0., 0.]
    sol = odeint(sys_odes_na, na_initial_all, time, args=(vol_0, nu_in, ca_in))
    na = sol[:, 0]
    nb = sol[:, 1]
    nc = sol[:, 2]
    nd = sol[:, 3]

    vol = vol_0 + nu_in * time
    ca = na / vol
    cb = nb / vol
    cc = nc / vol
    cd = nd / vol

    make_fig(name+"_na", time, ca, y1_label="$C_A$", y2_array=cb, y2_label="$C_B$",
             y3_array=cc, y3_label="$C_C$", y4_array=cd, y4_label="$C_D$", x_label="time (s)",
             y_label="concentration (mol/L)",
             x_lima=t_min, x_limb=t_max, y_lima=-0.01, y_limb=0.05
             )


def main():
    """ Runs the main program.
    """
    solve_ode_sys()

    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
