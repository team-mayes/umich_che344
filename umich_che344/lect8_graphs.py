# !/usr/bin/env python
# coding=utf-8
"""
Graphs for lecture 3, from Maxwell-Boltzmann Distribution
"""
from __future__ import print_function

import sys

import numpy as np

from common import make_fig, GOOD_RET

__author__ = 'hbmayes'


def neg_ra(k, cao, x):
    return k * cao * (1-x)


def get_volume(cao, nu, k, x_range):
    return (cao * nu) / neg_ra(k, cao, x_range)


def graph_alg_eq():
    """
    Given a simple algebraic equation, makes a graph
    """
    fig_name = 'lect8_cstrs_series'

    # x-axis
    x_start = 0.00  # initial conversion
    x_end = 0.8  # final conversion
    num_steps = 2001  # for solving/graphing
    x_range = np.linspace(x_start, x_end, num_steps)
    vol = 50.0  # L
    nu = 4.0  # L/s
    tau = vol / nu  # s
    k = 0.0281  # min^-1
    cao = 1.0  # mol/L

    volume = get_volume(cao, nu, k, x_range)

    x = {}
    for reactor in range(0, 5):
        x[reactor] = 1 - 1.0 / np.power(1. + tau * k, reactor)
        print("After reactor {}, the conversion is {:.2f}".format(reactor, x[reactor]))

    x_fill = {}
    y_fill = {}
    for reactor in range(1, 5):
        x_fill[reactor] = [x[reactor-1], x[reactor]]
        vol = get_volume(cao, nu, k, x[reactor])
        y_fill[reactor] = [vol, vol]

    make_fig(fig_name, x_range, volume,
             # x_range, volume,
             x_label=r'conversion (X, unitless)', y_label=r'$\frac{F_{A0}}{-r_A}$ (L)',
             x_lima=0.0, x_limb=0.5,
             y_lima=0.0, y_limb=600.0,
             fig_width=6, fig_height=4,
             x_fill=x_fill[1], y_fill=y_fill[1],
             x2_fill=x_fill[2], y2_fill=y_fill[2],
             )
    fao = cao * nu
    fa1 = cao * (1-x[1]) * nu
    print(fao, fa1, (fao - fa1)/fao)

    make_fig(fig_name + "1", x_range, volume,
             # x_range, volume,
             x_label=r'conversion (X, unitless)', y_label=r'$\frac{F_{A0}}{-r_A}$ (L)',
             x_lima=0.0, x_limb=0.5,
             y_lima=0.0, y_limb=600.0,
             fig_width=6, fig_height=4,
             x_fill=x_fill[1], y_fill=y_fill[1],
             # x2_fill=x_fill[2], y2_fill=y_fill[2],
             )

    ca1 = cao * (1-x[1])
    volume = get_volume(ca1, nu, k, x_range)
    reactor = 1
    print(x[reactor])
    x_fill[reactor] = [x[reactor-1], x[reactor]]
    vol = get_volume(ca1, nu, k, x[reactor])
    y_fill[reactor] = [vol, vol]

    make_fig(fig_name + "2", x_range, volume,
             # x_range, volume,
             x_label=r'conversion (X, unitless)', y_label=r'$\frac{F_{A1}}{-r_A}$ (L)',
             x_lima=0.0, x_limb=0.5,
             y_lima=0.0, y_limb=600.0,
             fig_width=6, fig_height=4,
             # x_fill=x_fill[1], y_fill=y_fill[1],
             x2_fill=x_fill[1], y2_fill=y_fill[1],
             )

    # x_fill = np.linspace(4.0, 60.0)
    # y_fill = eq_3_20(x_fill, 600.0)
    # y2_fill = eq_3_20(x_fill, 1000.0)
    # make_fig(fig_name + "fill", x_range, frac_e[2], y1_label=str(temps[2]), color1="green",
    #          y2_array=frac_e[4], y2_label=str(temps[4]), color2="purple",
    #          x_label=r'energy (kcal/mol)', y_label='fraction with E at temp in K',
    #          x_lima=x_start, x_limb=X_end,
    #          y_lima=0.0, y_limb=0.5,
    #          fig_width=8, fig_height=4,
    #          x_fill=x_fill, y_fill=y_fill, x2_fill=x_fill, y2_fill=y2_fill,
    #          )



def main():
    """ Runs the main program.
    """
    graph_alg_eq()
    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
