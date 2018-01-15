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


def sys_odes(y_vector, w, ka, keq, kc, alpha, cto, fto):
    # put here any equations you need to calculate the differential equations (R.H.S.s of dy/dW)
    fa, fb, fc, p = y_vector
    ft = fa + fb + fc
    ca = cto * fa / ft
    cb = cto * fb / ft
    cc = cto * fc / ft
    r1 = ka*(ca - cb**3.0 * cc / keq)
    rb = kc*cb
    # below are the differential equations for dFa/dW, dFb/dW, dFc/dW, and dp/dW (in that order)
    dy_dw = [-r1,
             3.0*r1 - rb,
             r1,
             -alpha*ft/(2.0*fto*p)]
    return dy_dw


def solve_ode_sys():
    # initial values
    fa0 = 5.0
    fb0 = 0.0
    c0 = 0.0
    p0 = 1.0
    # "y" is our system of equations (a vector). "y0" are the initial values. I'm listing "X" first and "p" second
    y0 = [fa0, fb0, c0, p0]

    ka = 2.0
    keq = 0.004
    kc = 8.0
    cto = 0.2
    fto = 5.0
    alpha = 0.015

    # Give an initial weight through a final weight. We don't know the final weight needed yet; if we guess
    # too small and we don't get the conversion we want, we can always increase it and run the program again
    x_min = 0
    x_max = 30.0
    w_cat = np.linspace(x_min, x_max, 1001)

    sol = odeint(sys_odes, y0, w_cat, args=(ka, keq, kc, alpha, cto, fto))
    a_w = sol[:, 0]
    b_w = sol[:, 1]
    c_w = sol[:, 2]
    p_w = sol[:, 3]

    name = 'lecture_9'
    make_fig(name+"flows", w_cat, a_w, y1_label="$F_A$(W)", y2_array=b_w, y2_label="$F_B$(W)",
             y3_array=c_w, y3_label="$F_C$(W)", x_label="catalyst mass (kg)",
             y_label="molar flow rates (mol/s)", x_lima=x_min, x_limb=x_max, y_lima=None, y_limb=None, loc=7)

    make_fig(name+"p", w_cat, p_w, x_label="catalyst mass (kg)",
             y_label="pressure ratio, p (unitless)", x_lima=x_min, x_limb=x_max, y_lima=0.0, y_limb=1.0, loc=7)


def main():
    """ Runs the main program.
    """
    solve_ode_sys()

    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
