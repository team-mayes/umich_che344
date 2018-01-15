# !/usr/bin/env python
# coding=utf-8
"""
Graphs for lecture 4, plot solution to an ODE
"""
from __future__ import print_function

import sys
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve
from common import make_fig, GOOD_RET

__author__ = 'hbmayes'


def ode(y, t, k, k_c, cao, nu_0):
    """
    :param y: independent variable
    :param t: dependent variable
    :param k: rate coefficient
    :param k_c: equilibrium coefficient
    :param cao: initial concentration
    :return: dy_dt
    """
    vol_change = 1-0.5*y
    # vol_change = 1
    return 2.0 * k / nu_0 * (cao * np.square((1.0-y)/vol_change) - y * 0.5 / k_c / vol_change)


def solve_ode():
    """
    Solve single ODE
    """
    fig_name = "lect5"

    k = 0.2  # L/mol s
    k_c = 20.0  # L/mol
    cao = 0.2  # mol/L
    x0 = 0.0  # initial conversion
    nu_0 = 1.0  # L / s

    v_start = 0.0
    v_end = 60.0
    volume = np.linspace(v_start, v_end, 1001)  # L
    conv = odeint(ode, x0, volume, args=(k, k_c, cao, nu_0))

    # here, need to add the additional argument of "t" because of how "ode" was set up for "odeint"
    x_eq = fsolve(ode, 0.5, args=(v_end, k, k_c, cao, nu_0))

    make_fig(fig_name + "_conversion", volume, conv,
             x_label=r'volume (L)', y_label=r'conversion (unitless)', y1_label=r'X(V)',
             x2_array=[v_start, v_end], y2_array=[x_eq, x_eq], y2_label=r'X$_{eq}$',
             x_lima=0.0, x_limb=v_end,
             y_lima=0.0, y_limb=1.0,
             fig_width=8, fig_height=4,
             )

    vol_change = 1.0 - 0.5 * conv
    # vol_change = 1
    c_a = cao * (1.0 - conv) / vol_change
    c_b = cao * conv * 0.5 / vol_change

    make_fig(fig_name + "_concentration", volume, c_a,
             y1_label="A", y2_array=c_b, y2_label="B", color2="red",
             x_label=r'volume (L)', y_label=r'concentration (mol/L)',
             x_lima=0.0, x_limb=v_end,
             y_lima=0.0, y_limb=cao,
             fig_width=8, fig_height=4,
             )

    conv_2 = odeint(ode, x0, volume, args=(k, k_c, cao, nu_0*0.5))
    conv_3 = odeint(ode, x0, volume, args=(k, k_c, cao, nu_0*2.0))
    make_fig(fig_name + "_clicker", volume, conv,
             x_label=r'volume (L)', y_label=r'conversion (unitless)', y1_label=r'A) No change',
             y2_array=conv * 2.0, y2_label=r'B) ', y3_array=conv * 0.5, y3_label=r'C) ',
             y4_array=conv_2, y4_label=r'D) ', y5_array=conv_3, y5_label=r'E) ',
             x_lima=0.0, x_limb=v_end,
             y_lima=0.0, y_limb=1.0,
             fig_width=8, fig_height=4,
             )

    eps = -0.5
    x_leven = np.linspace(0.0, 0.7, 1001)  # conversion, unitless
    y2 = 1.0 / ode(x_leven, 1.0, k, k_c, cao, nu_0)
    # y_leven = nu_0 * k_c/k * np.square(1 + eps * x_leven) / (2 * k_c * cao * np.square(1-x_leven) -
    #                                                          x_leven * (1 + eps * x_leven))
    make_fig(fig_name + "_levenspiel", x_leven, y2,
             x_label=r'conversion (unitless)', y_label=r'$\frac{-F_{A0}}{r_A}$ (L)',
             y_lima=0.0, y_limb=150,
             x_lima=0.0, x_limb=0.8,
             fig_width=8, fig_height=4,
             )


def main():
    """ Runs the main program.
    """
    solve_ode()

    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
