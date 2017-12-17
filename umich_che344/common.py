# !/usr/bin/env python
# coding=utf-8
"""
Common functions for multiple scripts used
"""
from __future__ import print_function
import os
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

__author__ = 'hbmayes'

"""
Exit Codes:
0 = Success
"""
# The good status code
GOOD_RET = 0

# for figures
DEF_FIG_WIDTH = 10
DEF_FIG_HEIGHT = 6
DEF_AXIS_SIZE = 20
DEF_TICK_SIZE = 15
DEF_FIG_DIR = './figs/'


def save_figure(name, save_fig=True, fig_dir=DEF_FIG_DIR):
    """
    Specifies where and if to save a created figure
    :param name: Name for the file
    :param save_fig: boolean as to whether to save fig; defaults to true (specify False if not desired)
    :param fig_dir: location to save; defaults to a "figs" subfolder; can specify a directory such as
                    './' (current directory)
    :return: n/a
    """
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)
    if save_fig:
        plt.savefig(fig_dir + name, bbox_inches='tight')


def make_fig(name, x_array, y1_array, y1_label="", y2_array=None, y2_label="",
             y3_array=None, y3_label="", y4_array=None, y4_label="",
             y5_array=None, y5_label="", x_label="",
             y_label="", x_lima=None, x_limb=None, y_lima=None, y_limb=None, loc=2,
             fig_width=DEF_FIG_WIDTH, fig_height=DEF_FIG_HEIGHT, axis_font_size=DEF_AXIS_SIZE,
             tick_font_size=DEF_TICK_SIZE):
    rc('text', usetex=True)
    # a general purpose plotting routine; can plot between 1 and 5 curves
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.plot(x_array, y1_array, label=y1_label, linewidth=2, color='blue')
    if y2_array is not None:
        ax.plot(x_array, y2_array, label=y2_label, ls='--', linewidth=2, color='orange')
    if y3_array is not None:
        ax.plot(x_array, y3_array, label=y3_label, ls=':', linewidth=3, color='green')
    if y4_array is not None:
        ax.plot(x_array, y4_array, label=y4_label, ls='-.', linewidth=3, color='red')
    if y5_array is not None:
        ax.plot(x_array, y5_array, label=y5_label, ls='-', linewidth=3, color='yellow')
    ax.set_xlabel(x_label, fontsize=axis_font_size)
    ax.set_ylabel(y_label, fontsize=axis_font_size)
    if x_limb is not None:
        if x_lima is None:
            x_lima = 0.0
        ax.set_xlim([x_lima, x_limb])

    if y_limb is not None:
        if y_lima is None:
            y_lima = 0.0
        ax.set_ylim([y_lima, y_limb])

    ax.tick_params(labelsize=tick_font_size)
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    if y2_array is not None:
        ax.legend(loc=loc, fontsize=tick_font_size, )
    ax.xaxis.grid(True, 'minor')
    ax.yaxis.grid(True, 'minor')
    ax.xaxis.grid(True, 'major', linewidth=1)
    ax.yaxis.grid(True, 'major', linewidth=1)
    save_figure(name)
