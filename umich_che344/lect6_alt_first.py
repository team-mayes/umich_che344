# !/usr/bin/env python
# coding=utf-8
"""
Calcs for HW3
"""
from __future__ import print_function

import sys

import numpy as np

from common import GOOD_RET, make_fig

__author__ = 'hbmayes'


def pfr_design_eq(x_out, x_in, vol, nuo, k):
    """
    PFR design eq for HW3 problem 1, set up for f(Xi) = 0 for fsolve function
    :param x_in: initial conversion (unitless)
    :param x_out: final conversion (unitless)
    :param vol: PFR volume in L
    :param nuo: volumetric flow in L/min
    :param k: rate coefficient in 1/min
    :return: function residual (want close to zero)
    """
    return vol - nuo / k * (4.0 * np.log(1 / (1 - x_out)) - 3.0 * x_out - 4.0 * np.log(1 / (1 - x_in)) + 3.0 * x_in)


def cstr_design_eq(x_out, x_in, vol, nuo, k):
    """
    PFR design eq for HW3 problem 1, set up for f(Xi) = 0 for fsolve function
    :param x_in: initial conversion (unitless)
    :param x_out: final conversion (unitless)
    :param vol: PFR volume in L
    :param nuo: volumetric flow in L/min
    :param k: rate coefficient in 1/min
    :return: function residual (want close to zero)
    """
    return vol - nuo / k * (x_out - x_in) * (1 + 3 * x_out) / (1 - x_out)


def r_dis_a(k, cao, x):
    """
    rate of consumption (disappearance) of species A for HW3 prob 1
    :param k: rate coefficient at temp of interest (1/min)
    :param cao: initial concentration of A in mol/L
    :param x: conversion of A
    :return: rate in mol/L-mib
    """
    return k * cao * (1 - x)


def pfr_design(k, cao, x, k_equil, nuo):
    """
    rate of consumption (disappearance) of species A for HW3 prob 1
    :param k: rate coefficient at temp of interest (1/min)
    :param cao: initial concentration of A in mol/L
    :param x: conversion of A
    :return: rate in mol/L-mib
    """
    return nuo / (2.0 * k * (cao * np.square(1 - x) - x / (2 * k_equil)))


# noinspection PyTypeChecker
def prob1a():
    """
    Given a few points, makes a line
    :return: nothing--saves a file with the graph
    """

    cao = 1.0  # mol / L
    nuo = 100.0  # L / s
    k = 0.2  # L / mol s
    fao = cao * nuo

    vol = 750.0  # L
    tau = vol / nuo  # s

    # x_in = 0.0
    # x_out = 0.65
    x_in = np.zeros(6)
    x_out = np.zeros(6)
    cstr_x = np.zeros(6)

    print("conversion", (tau * k) / (1 + tau * k))

    for id in [1, 2, 3, 4]:
        x_in[id+1] = x_out[id]
        cstr_x = (tau*k)/(1+tau*k)
    print(x_in)
    #
    # x_cstr = np.array([x_in, x_out])
    # x_pfr = np.linspace(x_in, x_out, 10001)
    # neg_ra = r_dis_a(k, cao, x_pfr)
    # leven_pfr  []
    #
    # fig_name = 'lect06_alt'
    # volume_limit = 2000
    # make_fig(fig_name, x_pfr, leven_pfr,
    #          x_label=r'conversion (X, unitless)', y_label=r'$\displaystyle\frac{F_{A0}}{-r_A} \left(L\right)$',
    #          x_lima=0.0, x_limb=0.65,
    #          y_lima=0.0, y_limb=volume_limit,
    #          color1="black",
    #          x_fill=x_cstr,
    #          y_fill=leven_cstr,
    #          x2_fill=x_pfr, y2_fill=leven_pfr,
    #          # fill1_label="CSTR", fill2_label="PFR",
    #          )
    # print("yo")


def main():
    """ Runs the main program.
    """
    prob1a()

    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
