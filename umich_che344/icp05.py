# !/usr/bin/env python
# coding=utf-8
"""
Calcs for HW2
"""
from __future__ import print_function

import sys
from umich_che344.common import GOOD_RET, R_KCAL, temp_c_to_k, k_at_new_temp

__author__ = 'hbmayes'


def main():
    """ Runs the main program.
    """
    k_ref = 0.07  # mol/L/min
    t_ref = temp_c_to_k(300.0)
    e_a = 20.0  # kcal/mol
    c_initial = 1.0  # M
    x = 0.9  # req conversion
    common_constant = c_initial**2 * (1-x)  # M^2

    # temp in C, vol in L
    for temp, vol in zip([500.0, 200.0, 350.0, 200.0, 100.0], [100.0, 250.0, 500.0, 5000.0, 10000.0]):
        temp_k = temp_c_to_k(temp)
        k = k_at_new_temp(k_ref, e_a, R_KCAL, t_ref, temp_k)
        print("At {}C ({}K), k = {:0.2E}".format(temp, temp_k, k))
        intermed = k*vol
        print("  kV = {:0.2E} L/mol/min*{:0.0f} L = {:0.3f} L^2/mol/min".format(k, vol, intermed))
        print("  max F_A0 = {:0.1f} L^2/mol/min * {:0.2f} mol^2/L^2 = {:0.2f} mol/min".format(intermed, common_constant,
                                                                                          intermed * common_constant))
    return GOOD_RET  # success


if __name__ == '__main__':
    status = main()
    sys.exit(status)
