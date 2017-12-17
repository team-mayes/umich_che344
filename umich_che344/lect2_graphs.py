# !/usr/bin/env python
# coding=utf-8
"""
Make a graph for lecture 2, hippo digestion
"""
from __future__ import print_function

import sys
import numpy as np
from common import make_fig, GOOD_RET

__author__ = 'hbmayes'


def graph_alg_eq():
    """

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


def main():
    """ Runs the main program.
    """
    graph_alg_eq()

    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
