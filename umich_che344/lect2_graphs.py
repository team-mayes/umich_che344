# !/usr/bin/env python
# coding=utf-8
"""
Make a graph for lecture 2, hippo digestion
"""
from __future__ import print_function

import sys
import numpy as np
from scipy import interpolate
from common import make_fig, GOOD_RET

__author__ = 'hbmayes'


def graph_alg_eq():
    """
    Given a simple algebraic equation, makes a graph
    """
    fig_name = 'lect2_hippo'

    # x-axis
    x_start = 0.0  # initial conversion
    x_end = 0.999  # final conversion; didn't choose 1 to avoid divide by zero error
    num_steps = 2001  # for solving/graphing
    conversion_scale = np.linspace(x_start, x_end, num_steps)

    # y-axis
    design_eq = np.divide((1.00+16.5*(1.00-conversion_scale)), 1.75*(1-conversion_scale))

    make_fig(fig_name, conversion_scale, design_eq,
             x_label=r'conversion (X, unitless)', y_label=r'$\displaystyle\frac{C_{F0}}{-r_F}$ (hr)',
             x_lima=0.0, x_limb=1.0, y_lima=0.0, y_limb=24.0,
             )


def graph_points():
    """
    Given a few points, makes a smooth curve
    :return: saves a file with the graph
    """
    fig_name = 'lect2_num_solv'

    # given data
    x = np.array([0.0, 0.4, 0.6, 0.8])
    ra = np.array([0.01, 0.0080, 0.005, 0.002])
    design_eq =np.divide(2.0, ra)
    print("Generic example design equation points: {}".format(["{:0.1f}".format(x) for x in design_eq]))

    # cubic spline
    xnew = np.linspace(0.0, 0.8, 101)
    # alternately, from interpolation
    y_interp = interpolate.interp1d(x, design_eq, kind='quadratic')
    make_fig(fig_name, x, design_eq, ls1='o', x2_array=xnew, y2_array=y_interp(xnew),
             x_label=r'conversion (X, unitless)', y_label=r'$\displaystyle\frac{F_{A0}}{-r_A} \left(L\right)$',
             x_lima=0.0, x_limb=0.8, y_lima=0.0, y_limb=1000,
             fig_width=4, color2='green',
             )


def graph_smooth_from_pts():
    """
    Given a few points, interpolates a smooth curve
    :return: saves a file with the graph
    """
    fig_name = 'lect2_isom'

    # given data
    x = np.array([0.0, 0.2, 0.4, 0.6, 0.65])
    ra = np.array([39.0, 53.0, 59.0, 38.0, 25.0])
    design_eq =np.divide(50.0, ra)
    print("Isom example design equation points: {}".format(design_eq))

    # cubic spline
    tck = interpolate.splrep(x, design_eq, s=0)
    xnew = np.linspace(0.0, 0.7, 101)
    ynew = interpolate.splev(xnew, tck, der=0)
    # alternately, from interpolation
    cubic_interp = interpolate.interp1d(x, design_eq, kind='quadratic', fill_value="extrapolate")
    make_fig(fig_name, x, design_eq, ls1='o', x2_array=xnew, y2_array=ynew, x3_array=xnew, y3_array=cubic_interp(xnew),
             y1_label="data", y2_label="quadratic", y3_label="cubic",
             x_label=r'conversion (X, unitless)', y_label=r'$\displaystyle\frac{F_{A0}}{-r_A} \left(m^3\right)$',
             x_lima=0.0, x_limb=0.7, y_lima=0.0, y_limb=2.5,
             )


def main():
    """ Runs the main program.
    """
    graph_alg_eq()
    graph_points()
    graph_smooth_from_pts()

    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
