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


def ode(y, t, k, k_c, cao):
    """
    :param y: independent variable
    :param t: dependent variable
    :param k: rate coefficient
    :param k_c: equilibrium coefficient
    :param cao: initial concentration
    :return: dy_dt
    """
    return 2.0 * k * (cao * np.square(1.0-y) - y * 0.5 / k_c)


def solve_ode():
    """
    Solve single ODE
    """
    fig_name = "lect4"

    k = 0.2  # L/mol s
    k_c = 20.0  # L/mol
    cao = 0.2  # mol/L
    x0 = 0.0  # initial conversion

    t_start = 0.0
    t_end = 60.0
    time = np.linspace(t_start, t_end, 1001)  # seconds
    conv = odeint(ode, x0, time, args=(k, k_c, cao))

    # here, need to add the additional argument of "t" because of how "ode" was set up for "odeint"
    x_eq = fsolve(ode, 0.5, args=(t_end, k, k_c, cao))

    make_fig(fig_name + "_conversion", time, conv,
             x_label=r'time (s)', y_label=r'conversion (unitless)', y1_label=r'X(t)',
             x2_array=[t_start, t_end], y2_array=[x_eq, x_eq], y2_label=r'X$_{eq}$',
             x_lima=0.0, x_limb=t_end,
             y_lima=0.0, y_limb=1.0,
             fig_width=8, fig_height=4,
             )

    c_a = cao * (1.0 - conv)
    c_b = cao * conv * 0.5

    make_fig(fig_name + "_concentration", time, c_a,
             y1_label="A", y2_array=c_b, y2_label="B", color2="red",
             x_label=r'time (s)', y_label=r'concentration (mol/L)',
             x_lima=0.0, x_limb=t_end,
             y_lima=0.0, y_limb=cao,
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
