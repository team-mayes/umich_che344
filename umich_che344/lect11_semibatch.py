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

A = '_a'
B = '_b'
C = '_c'


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


# noinspection PyTypeChecker
def solve_original_semibatch():
    # initial values
    xb_parts = []
    name = 'lect_11_semibatch'

    # Give an initial independent variable through a final one. We don't know the final needed yet; if we guess
    # too small and we don't get the conversion we want, we can always increase it and run the program again
    t_min = 0
    t_max = 400.0
    time = np.linspace(t_min, t_max, 1001)
    for part_id, part in enumerate([A, B, C]):
        if part == A:
            vol_0 = 5.  # L
            cb_0 = 0.05  # mol/L
            ca_0 = 0.0
            ca_in = 0.025  # mol/L
            nu_in = 0.05  # L/s
        elif part == B:
            vol_0 = 15.  # vol in L
            na_0 = 0.25  # mol
            nb_0 = 0.25  # mol
            ca_0 = na_0 / vol_0
            cb_0 = nb_0 / vol_0
            nu_in = 0.0
            ca_in = 0.0
        else:
            vol_0 = 10.  # L
            cb_0 = 0.025  # mol/L
            ca_0 = 0.0
            ca_in = 0.05  # mol/L
            nu_in = 0.05  # L/s

        if part == A:
            # show that both methods yield the same solution
            c_initial_all = [ca_0, cb_0, 0., 0.]

            # def sys_odes_ca(y_vector, time, vol_0, nu_in, ca_in):
            sol = odeint(sys_odes_ca, c_initial_all, time, args=(vol_0, nu_in, ca_in))
            ca = sol[:, 0]
            cb = sol[:, 1]
            cc = sol[:, 2]
            cd = sol[:, 3]

            make_fig(name+"_ca"+part, time, ca, y1_label="$C_A$", y2_array=cb, y2_label="$C_B$",
                     y3_array=cc, y3_label="$C_C$", y4_array=cd, y4_label="$C_D$", x_label="time (s)",
                     y_label="concentration (mol/L)",
                     x_lima=t_min, x_limb=t_max, y_lima=0.0, y_limb=1.0,
                     )

        # def sys_odes_na(y_vector, time, vol_0, nu_in, ca_in):
        na_0 = ca_0 * vol_0
        nb_0 = cb_0 * vol_0
        na_initial_all = [na_0, nb_0, 0., 0.]
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

        make_fig(name+"_na"+part, time, ca, y1_label="$C_A$", y2_array=cb, y2_label="$C_B$",
                 y3_array=cc, y3_label="$C_C$", y4_array=cd, y4_label="$C_D$", x_label="time (s)",
                 y_label="concentration (mol/L)",
                 x_lima=t_min, x_limb=t_max, y_lima=0.0, y_limb=1.00
                 )

        print("Part {}, na_in = {:.2f} moles, nb_in = {:.2f}".format(part, na_0, nb_0))
        xb_parts.append((nb_0 - nb) / nb_0)
        vol_15_index = np.nonzero(np.abs(vol-15.0)<0.000001)
        print("   time at s the conversion of B at V = 15 L, which corresponds to time = {} s, "
              "and X_B = {:.2f}".format(time[vol_15_index], xb_parts[part_id][500]))

    make_fig(name+"_x", time, xb_parts[0], y1_label="$X_B$ original semibatch, $C_{B0} > C_{A_{in}}$",
             y2_array=xb_parts[1], y2_label="$X_B$ batch", color2="red",
             y3_array=xb_parts[2], y3_label="$X_B$ semibatch, $C_{B0} < C_{A_{in}}$", x_label="time (s)",
             y_label="conversion of B (unitless)",
             x_lima=t_min, x_limb=t_max, y_lima=0.0, y_limb=1.00,
             )


# def solve_batch():
#     # initial values
#     vol_0 = 15.  # L
#     initial_moles = 0.25  # moles
#     cb_0 = initial_moles / vol_0  # mol/L
#     c_initial_all = [cb_0, cb_0, 0., 0.]
#
#     part = "_part_b"
#
#     ca_in = 0.025  # mol/L
#     nu_in = 0.00  # L/s
#
#     # Give an initial independent variable through a final one. We don't know the final needed yet; if we guess
#     # too small and we don't get the conversion we want, we can always increase it and run the program again
#     t_min = 0
#     t_max = 400.0
#     time = np.linspace(t_min, t_max, 1001)
#
#     # def sys_odes_ca(y_vector, time, vol_0, nu_in, ca_in):
#     sol = odeint(sys_odes_ca, c_initial_all, time, args=(vol_0, nu_in, ca_in))
#     ca = sol[:, 0]
#     cb = sol[:, 1]
#     cc = sol[:, 2]
#     cd = sol[:, 3]
#
#     name = 'lect_11_semibatch'
#     make_fig(name+"_ca"+part, time, ca, y1_label="$C_A$", y2_array=cb, y2_label="$C_B$",
#              y3_array=cc, y3_label="$C_C$", y4_array=cd, y4_label="$C_D$", x_label="time (s)",
#              y_label="concentration (mol/L)",
#              x_lima=t_min, x_limb=t_max, y_lima=-0.01, y_limb=0.05
#              )
#
#     # def sys_odes_na(y_vector, time, vol_0, nu_in, ca_in):
#     na_initial_all = [0, cb_0 * vol_0, 0., 0.]
#     sol = odeint(sys_odes_na, na_initial_all, time, args=(vol_0, nu_in, ca_in))
#     na = sol[:, 0]
#     nb = sol[:, 1]
#     nc = sol[:, 2]
#     nd = sol[:, 3]
#
#     vol = vol_0 + nu_in * time
#     ca = na / vol
#     cb = nb / vol
#     cc = nc / vol
#     cd = nd / vol
#
#     make_fig(name+"_na"+part, time, ca, y1_label="$C_A$", y2_array=cb, y2_label="$C_B$",
#              y3_array=cc, y3_label="$C_C$", y4_array=cd, y4_label="$C_D$", x_label="time (s)",
#              y_label="concentration (mol/L)",
#              x_lima=t_min, x_limb=t_max, y_lima=-0.01, y_limb=0.05
#              )
#
#     nb_in = cb_0 * vol_0
#     xb = (nb_in - nb) / nb_in
#     make_fig(name+"_x", time, xb, y1_label="$X_B$", x_label="time (s)",
#              y_label="conversion of B (unitless)",
#              x_lima=t_min, x_limb=t_max, y_lima=0.0, y_limb=1.0,
#              )
#     print("This problem wants the conversion of B at V = 15 L, which corresponds to time = {} s, "
#           "and X_B = {:.2f}".format(time[500], xb[500]))


def main():
    """ Runs the main program.
    """
    solve_original_semibatch()

    # solve_batch()

    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
