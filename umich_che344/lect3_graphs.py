# !/usr/bin/env python
# coding=utf-8
"""
Graphs for lecture 3, from Maxwell-Boltzmann Distribution
"""
from __future__ import print_function

import sys
import numpy as np
from common import make_fig, GOOD_RET, eq_3_20, eq_3_23, eq_3_20integrated

__author__ = 'hbmayes'


def graph_alg_eq():
    """
    Given a simple algebraic equation, makes a graph
    """
    fig_name = 'lect3_frac_energy'

    # x-axis
    e_start = 0.00  # initial energy
    e_end = 10.0  # final energy
    num_steps = 2001  # for solving/graphing
    energy_range = np.linspace(e_start, e_end, num_steps)

    temps = [300.0, 450.0, 600.0, 750.0, 1000.0]

    # y-axis
    frac_e = []
    for temp in temps:
        frac_e.append(eq_3_20(energy_range, temp))

    make_fig(fig_name, energy_range, frac_e[0], y1_label=str(temps[0]),
             y2_array=frac_e[1], y2_label=str(temps[1]),
             y3_array=frac_e[2], y3_label=str(temps[2]),
             y4_array=frac_e[3], y4_label=str(temps[3]),
             y5_array=frac_e[4], y5_label=str(temps[4]),
             x_label=r'energy (kcal/mol)', y_label='fraction with E at temp in K',
             x_lima=0.0, x_limb=e_end,
             y_lima=0.0, y_limb=1.0,
             fig_width=8, fig_height=4,
             )


    x_fill = np.linspace(4.0, 60.0)
    y_fill = eq_3_20(x_fill, 600.0)
    y2_fill = eq_3_20(x_fill, 1000.0)
    make_fig(fig_name + "fill", energy_range, frac_e[2], y1_label=str(temps[2]), color1="green",
             y2_array=frac_e[4], y2_label=str(temps[4]), color2="purple",
             x_label=r'energy (kcal/mol)', y_label='fraction with E at temp in K',
             x_lima=e_start, x_limb=e_end,
             y_lima=0.0, y_limb=0.5,
             fig_width=8, fig_height=4,
             x_fill=x_fill, y_fill=y_fill, x2_fill=x_fill, y2_fill=y2_fill,
             )


def graph_int():
    """
    Given a simple algebraic equation, makes a graph
    """
    fig_name = 'lect3_frac_energy_at_least'
    # x-axis
    temp_start = 0.001  # initial temp in K
    temp_end = 1200.0  # final temp in K
    num_steps = 2001  # for solving/graphing
    temp_range = np.linspace(temp_start, temp_end, num_steps)

    # y-axis
    ea = 4.0
    frac_e_approx = eq_3_23(temp_range, ea)
    frac_e_anal = eq_3_20integrated(temp_range, ea)

    make_fig(fig_name, temp_range, frac_e_anal, y1_label="analytical",
             y2_array=frac_e_approx, y2_label="approximate", color2="red",
             x_label=r'temperature (K)', y_label=r'fraction with E $>$ E$_A = 4.0$',
             x_lima=0.0, x_limb=temp_end,
             y_lima=0.0, y_limb=1.0,
             fig_width=8, fig_height=4,
             )
    #
    # ea = 12.0
    # frac_e_approx = eq_3_23(temp_range, ea)
    # frac_e_anal = eq_3_20integrated(temp_range, ea)
    #
    # make_fig(fig_name + "25", temp_range, frac_e_anal, y1_label="analytical",
    #          y2_array=frac_e_approx, y2_label="approximate", color2="red",
    #          x_label=r'temperature (K)', y_label=r'fraction with E $>$ E$_A = 12.0$',
    #          x_lima=0.0, x_limb=temp_end,
    #          y_lima=0.0, y_limb=0.2,
    #          fig_width=8, fig_height=4,
    #          )


def main():
    """ Runs the main program.
    """
    graph_alg_eq()
    graph_int()

    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
