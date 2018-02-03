# !/usr/bin/env python
# coding=utf-8
"""
Graphs for lecture 4, plot solution to an ODE
"""
from __future__ import print_function

import sys
import numpy as np
from common import make_fig, GOOD_RET, temp_c_to_k, k_from_a_ea, R_KJ, AVO, R_KCAL, cal_to_j, temp_k_to_c

__author__ = 'hbmayes'


# noinspection PyUnusedLocal
def ode(y, t, k, k_c, cao, nu_0, gas=True):
    """
    :param gas: flag to account for volume change
    :param y: independent variable
    :param t: dependent variable
    :param k: rate coefficient
    :param k_c: equilibrium coefficient
    :param cao: initial concentration
    :param nu_0: initial volumetric flow rate
    :return: dy_dt
    """
    if gas:
        vol_change = 1-0.5*y
    else:
        vol_change = 1
    return 2.0 * k / nu_0 * (cao * np.square((1.0-y)/vol_change) - y * 0.5 / k_c / vol_change)


# noinspection PyTypeChecker
def solve_ode():
    """
    Solve single ODE
    """
    fig_name = "lect06"

    k = 0.2  # L/mol s
    k_c = 20.0  # L/mol
    cao = 0.2  # mol/L
    # x0 = 0.0  # initial conversion
    nu_0 = 1.0  # L / s

    # v_start = 0.0
    # v_end = 60.0
    # volume = np.linspace(v_start, v_end, 1001)  # L
    # conv = odeint(ode, x0, volume, args=(k, k_c, cao, nu_0))
    # conv_liq = odeint(ode, x0, volume, args=(k, k_c, cao, nu_0, False))

    # # here, need to add the additional argument of "t" because of how "ode" was set up for "odeint"
    # x_eq = fsolve(ode, 0.5, args=(v_end, k, k_c, cao, nu_0))
    # x_eq_liq = fsolve(ode, 0.5, args=(v_end, k, k_c, cao, nu_0, False))
    #
    # make_fig(fig_name + "_conversion", volume, conv,
    #          x_label=r'volume (L)', y_label=r'conversion (unitless)', y1_label=r'X(V)',
    #          x2_array=[v_start, v_end], y2_array=[x_eq, x_eq], y2_label=r'X$_{eq}$',
    #          x_lima=0.0, x_limb=v_end,
    #          y_lima=0.0, y_limb=1.0,
    #          fig_width=8, fig_height=4,
    #          )
    # make_fig(fig_name + "_conversion_liq", volume, conv_liq,
    #          x_label=r'volume (L)', y_label=r'conversion (unitless)', y1_label=r'X(V)',
    #          x2_array=[v_start, v_end], y2_array=[x_eq_liq, x_eq_liq], y2_label=r'X$_{eq}$',
    #          x_lima=0.0, x_limb=v_end,
    #          y_lima=0.0, y_limb=1.0,
    #          fig_width=8, fig_height=4,
    #          )
    #
    # vol_change = 1.0 - 0.5 * conv
    # c_a_no_vol = cao * (1.0 - conv_liq)
    # c_b_no_vol = cao * conv_liq * 0.5
    # c_a = cao * (1.0 - conv) / vol_change
    # c_b = cao * conv * 0.5 / vol_change
    #
    # make_fig(fig_name + "_concentration", volume, c_a,
    #          y1_label="A", y2_array=c_b, y2_label="B", color2="red",
    #          x_label=r'volume (L)', y_label=r'concentration (mol/L)',
    #          x_lima=0.0, x_limb=v_end,
    #          y_lima=0.0, y_limb=cao,
    #          fig_width=8, fig_height=4,
    #          )
    #
    # make_fig(fig_name + "_concentration_liq", volume, c_a_no_vol,
    #          y1_label="A", y2_array=c_b_no_vol, y2_label="B", color2="red",
    #          x_label=r'volume (L)', y_label=r'concentration (mol/L)',
    #          x_lima=0.0, x_limb=v_end,
    #          y_lima=0.0, y_limb=cao,
    #          fig_width=8, fig_height=4,
    #          )
    #
    # conv_2 = odeint(ode, x0, volume, args=(k, k_c, cao, nu_0*0.5))
    # conv_3 = odeint(ode, x0, volume, args=(k, k_c, cao, nu_0*2.0))
    # make_fig(fig_name + "_clicker", volume, conv,
    #          x_label=r'volume (L)', y_label=r'conversion (unitless)', y1_label=r'A) No change',
    #          y2_array=conv * 2.0, y2_label=r'B) ', y3_array=conv * 0.5, y3_label=r'C) ',
    #          y4_array=conv_2, y4_label=r'D) ', y5_array=conv_3, y5_label=r'E) ',
    #          x_lima=0.0, x_limb=v_end,
    #          y_lima=0.0, y_limb=1.0,
    #          fig_width=8, fig_height=4,
    #          )

    x_leven = np.linspace(0.0, 0.7, 1001)  # conversion, unitless
    # y_changing_density = 1.0 / ode(x_leven, 1.0, k, k_c, cao, nu_0)
    # # eps = -0.5
    # # y_leven = nu_0 * k_c/k * np.square(1 + eps * x_leven) / (2 * k_c * cao * np.square(1-x_leven) -
    # #                                                          x_leven * (1 + eps * x_leven))
    # make_fig(fig_name + "_levenspiel", x_leven, y_changing_density,
    #          x_label=r'conversion (unitless)', y_label=r'$\frac{-F_{A0}}{r_A}$ (L)',
    #          y_lima=0.0, y_limb=150,
    #          x_lima=0.0, x_limb=0.8,
    #          fig_width=8, fig_height=4,
    #          )
    y_constant_density = 1.0 / ode(x_leven, 1.0, k, k_c, cao, nu_0, False)
    # eps = -0.5
    # y_leven = nu_0 * k_c/k * np.square(1 + eps * x_leven) / (2 * k_c * cao * np.square(1-x_leven) -
    #                                                          x_leven * (1 + eps * x_leven))
    make_fig(fig_name + "_levenspiel", x_leven, y_constant_density,
             x_label=r'conversion (unitless)', y_label=r'$\frac{-F_{A0}}{r_A}$ (L)',
             y_lima=0.0, y_limb=150,
             x_lima=0.0, x_limb=0.7,
             fig_width=6, fig_height=4,
             )
    make_fig(fig_name + "_levenspiel_mult", x_leven, y_constant_density, y2_array=y_constant_density*2.0,
             y3_array=y_constant_density*0.5, color2="red",
             x_label=r'conversion (unitless)', y_label=r'$\frac{-F_{A0}}{r_A}$ (L)',
             y_lima=0.0, y_limb=150,
             x_lima=0.0, x_limb=0.7,
             fig_width=8, fig_height=4,
             )


def main():
    """ Runs the main program.
    """
    solve_ode()

    # in class demo of range
    t1_c = 625  # degrees Celsius
    t2_c = 725  # degrees Celsius
    e_a = 29.25  # kJ/mol
    a = 7.27e-11  # cm^3/molecules-s
    a_moles = a * AVO * 0.001 * 60.0  # L /mol-min
    temp1 = temp_c_to_k(t1_c)
    temp2 = temp_c_to_k(t2_c)
    k1 = k_from_a_ea(a_moles, e_a, temp1, R_KJ)
    k2 = k_from_a_ea(a_moles, e_a, temp2, R_KJ)
    print("Given A = {} cm^3/molecules-s, E_A = {} kJ/mol: ".format(a, e_a))
    print("              at {} C ({} K), k = {:.2e} L/mol-min".format(t1_c, temp1, k1))
    print("              at {} C ({} K), k = {:.2e} L/mol-min".format(t2_c, temp2, k2))

    e_a_cal = 13.0  # kcal/mol
    e_a = cal_to_j(e_a_cal)  # kJ/mol
    temp3 = 333.0  # k
    temp4 = temp3 + 100.0
    t3_c = temp_k_to_c(temp3)
    t4_c = temp_k_to_c(temp4)
    r = 1.69 * 1e-6 / 1000.0 * 60.0

    a = r/k_from_a_ea(1, e_a, temp3, R_KCAL)
    k3 = k_from_a_ea(a, e_a, temp3, R_KCAL)
    k4 = k_from_a_ea(a, e_a, temp4, R_KCAL)

    print("\nGiven E_A = {:.1f} kcal/mol ({:.1f} kJ/mol):".format(e_a_cal, e_a))
    print("       Given: at  {:.0f} C ({} K), k = {:.2e} L/mol-min".format(t3_c, temp3, k3))
    print("  Calculated: at {:.0f} C ({} K), k = {:.2e} L/mol-min".format(t4_c, temp4, k4))

    k = 1.95e-4  # L/mol-s
    tau = 1.0 / 3e-3  # s
    print("tau: {:.2f}".format(tau))
    cao = 1.0  # mol/L
    print("term: {:.2f}".format(1.0/(k*tau*cao) + 56.0))

    # CA PE exam question
    x1 = 0.55
    kc = 5.8
    x2 = (1.0-np.square(1.-(1.+1./kc)*x1))/(1.+1./kc)
    print("P5-17: X2 = {:.3f}".format(x2))

    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
