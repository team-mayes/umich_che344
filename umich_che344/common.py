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
from matplotlib.patches import Rectangle
import csv
import errno
import numpy as np
from scipy import special
import six
import sys
from contextlib import contextmanager


__author__ = 'hbmayes'

"""
Exit Codes:
0 = Success
"""
# The good status code
GOOD_RET = 0
INPUT_ERROR = 1

# physical constants
J_IN_CAL = 4.184  # conversion factor J/cal = kJ/kcal
R_J = 8.314472  # J / K mol
R_KJ = 0.001 * R_J  # kJ / K mol
R_CAL = R_J / J_IN_CAL
R_KCAL = R_CAL * 0.001
R_BAR = R_J * 0.001 # bar-L / mol-K
R_ATM = 0.082057338  # atm-L / mol-K
K_0C = 273.15  # Temp in Kelvin at 0 degrees C
AVO = 6.022140857e23 # avogadro's number, mol-1, from NIST on 2018-01-15

# for figures
DEF_FIG_WIDTH = 10
DEF_FIG_HEIGHT = 6
DEF_AXIS_SIZE = 20
DEF_TICK_SIZE = 15
DEF_FIG_DIR = './figs/'


class InvalidDataError(Exception):
    pass


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


# For tests

# From http://schinckel.net/2013/04/15/capture-and-test-sys.stdout-sys.stderr-in-unittest.testcase/
@contextmanager
def capture_stdout(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    out, sys.stdout = sys.stdout, six.StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out


@contextmanager
def capture_stderr(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    err, sys.stderr = sys.stderr, six.StringIO()
    command(*args, **kwargs)
    sys.stderr.seek(0)
    yield sys.stderr.read()
    sys.stderr = err


def silent_remove(filename, disable=False):
    """
    Removes the target file name, catching and ignoring errors that indicate that the
    file does not exist.

    @param filename: The file to remove.
    @param disable: boolean to flag if want to disable removal
    """
    if not disable:
        try:
            os.remove(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise


# Conversions

def temp_c_to_k(temp_in_c):
    """
    simple conversion
    :param temp_in_c: temp in Celsius
    :return: temp in K
    """
    return temp_in_c + K_0C


def temp_k_to_c(temp_in_k):
    """
    simple conversion
    :param temp_in_k: temp in Kelvin
    :return: temp in Celsius
    """
    return temp_in_k - K_0C


def j_to_cal(energy_joules):
    """
    simple conversion
    :param energy_joules: energy in joules
    :return: energy in calories
    """
    return energy_joules / J_IN_CAL


def cal_to_j(energy_cal):
    """
    simple conversion
    :param energy_cal: energy in calories
    :return: energy in Joules
    """
    return energy_cal * J_IN_CAL


# Kinetics equations

def k_at_new_temp(k_ref, e_a, r_gas, t_ref, t_new):
    """
    convert using "alternate" form of Arrhenius eq
    :param k_ref: reference rate coefficient at temp t_ref
    :param e_a: activation energy with units consistent with given r_gas
    :param r_gas: universal gas constant in units consistent with e_a and temps
    :param t_ref: reference temp in K
    :param t_new: new temp in K
    :return: k at the "new' temperature, t_ref, in the same units as the given k_ref
    """
    return k_ref * np.exp((-e_a/r_gas)*(1/t_new - 1/t_ref))


def k_from_a_ea(a, e_a, temp, r_gas):
    """
    convert using "alternate" form of Arrhenius eq
    :param a: pre-exponential factor
    :param e_a: activation energy with units consistent with given r_gas
    :param temp: temperature in K
    :param r_gas: universal gas constant in units consistent with e_a and temps
    """
    return a * np.exp(-e_a/(r_gas*temp))


def eq_3_20(energy, temp, gas_const=R_KCAL):
    """
    fraction of moles with energy specified at temperature specified
    :param energy: energy in kcal/mol unless other gas constant used
    :param temp: temperature in K
    :param gas_const: universal gas contanst in correct units (default is Kcal/mol)
    :return fraction
    """
    return 2.0 * np.pi * np.power(1 / (np.pi * gas_const * temp), 1.5) * np.sqrt(energy) * np.exp(
        -energy / (gas_const * temp))


def eq_3_23(temp, ea, gas_const=R_KCAL):
    """
    fraction of moles with energy specified at temperature specified
    :param temp: temperature in K
    :param ea: activation energy in kcal/mol unless other gas constant used
    :param gas_const: universal gas constant in correct units (default is Kcal/mol)
    :return fraction
    """
    return np.sqrt(4.0 * ea / (np.pi * gas_const * temp)) * np.exp(-ea / (gas_const * temp))


def eq_3_20integrated(temp, ea, gas_const=R_KCAL):
    """
    fraction of moles with energy specified at temperature specified
    :param temp: temperature in K
    :param ea: activation energy in kcal/mol unless other gas constant used
    :param gas_const: universal gas constant in correct units (default is Kcal/mol)
    :return fraction
    """
    gamma = ea / (gas_const * temp)
    return np.sqrt(4.0 * gamma / np.pi) * np.exp(-gamma) + special.erfc(np.sqrt(gamma))


# LOGIC

def create_out_fname(src_file, prefix='', suffix='', remove_prefix=None, base_dir=None, ext=None):
    """Creates an outfile name for the given source file.

    @param remove_prefix: string to remove at the beginning of file name
    @param src_file: The file to process.
    @param prefix: The file prefix to add, if specified.
    @param suffix: The file suffix to append, if specified.
    @param base_dir: The base directory to use; defaults to `src_file`'s directory.
    @param ext: The extension to use instead of the source file's extension;
        defaults to the `scr_file`'s extension.
    @return: The output file name.
    """

    if base_dir is None:
        base_dir = os.path.dirname(src_file)

    file_name = os.path.basename(src_file)
    if remove_prefix is not None and file_name.startswith(remove_prefix):
        base_name = file_name[len(remove_prefix):]
    else:
        base_name = os.path.splitext(file_name)[0]

    if ext is None:
        ext = os.path.splitext(file_name)[1]

    return os.path.abspath(os.path.join(base_dir, prefix + base_name + suffix + ext))


def convert_dict_line(all_conv, data_conv, line):
    s_dict = {}
    for s_key, s_val in line.items():
        if data_conv and s_key in data_conv:
            try:
                s_dict[s_key] = data_conv[s_key](s_val)
            except ValueError as e:
                warning("Could not convert value '{}' from column '{}': '{}'.  Leaving as str".format(s_val, s_key, e))
                s_dict[s_key] = s_val
        elif all_conv:
            try:
                s_dict[s_key] = all_conv(s_val)
            except ValueError as e:
                warning("Could not convert value '{}' from column '{}': '{}'.  Leaving as str".format(s_val, s_key, e))
                s_dict[s_key] = s_val
        else:
            s_dict[s_key] = s_val
    return s_dict


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


# CSV #

def read_csv_header(src_file):
    """Returns a list containing the values from the first row of the given CSV
    file or None if the file is empty.

    @param src_file: The CSV file to read.
    @return: The first row or None if empty.
    """
    with open(src_file) as csv_file:
        for row in csv.reader(csv_file):
            return list(row)


def read_csv(src_file, data_conv=None, all_conv=None, quote_style=csv.QUOTE_MINIMAL):
    """
    Reads the given CSV (comma-separated with a first-line header row) and returns a list of
    dicts where each dict contains a row's data keyed by the header row.

    @param src_file: The CSV to read.
    @param data_conv: A map of header keys to conversion functions.  Note that values
        that throw a TypeError from an attempted conversion are left as strings in the result.
    @param all_conv: A function to apply to all values in the CSV.  A specified data_conv value
        takes precedence.
    @param quote_style: how to read the dictionary
    @return: A list of dicts containing the file's data.
    """
    result = []
    # file_reader = csv.reader(open(src_file), delimiter=',')
    with open(src_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, quoting=quote_style)
        for line in csv_reader:
            result.append(convert_dict_line(all_conv, data_conv, line))
    return result


def write_csv(data, out_fname, fieldnames, extrasaction="raise", mode='w', quote_style=csv.QUOTE_NONNUMERIC,
              print_message=True, round_digits=False):
    """
    Writes the given data to the given file location.

    @param round_digits: if desired, provide decimal number for rounding
    @param data: The data to write (list of dicts).
    @param out_fname: The name of the file to write to.
    @param fieldnames: The sequence of field names to use for the header.
    @param extrasaction: What to do when there are extra keys.  Acceptable
        values are "raise" or "ignore".
    @param mode: default mode is to overwrite file
    @param print_message: boolean to flag whether to note that file written or appended
    @param quote_style: dictates csv output style
    """
    with open(out_fname, mode) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames, extrasaction=extrasaction, quoting=quote_style)
        if mode == 'w':
            writer.writeheader()
        if round_digits:
            for row_id in range(len(data)):
                new_dict = {}
                for key, val in data[row_id].items():
                    if isinstance(val, float):
                        new_dict[key] = round(val, round_digits)
                    else:
                        new_dict[key] = val
                data[row_id] = new_dict
        writer.writerows(data)
    if print_message:
        if mode == 'a':
            print("  Appended: {}".format(out_fname))
        elif mode == 'w':
            print("Wrote file: {}".format(out_fname))


# FIGURES

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


def make_fig(name, x_array, y1_array, y1_label="", ls1="-", color1="blue",
             x2_array=None, y2_array=None, y2_label="", ls2='--', color2='orange',
             x3_array=None, y3_array=None, y3_label="", ls3=':',
             x4_array=None, y4_array=None, y4_label="", ls4='-.',
             x5_array=None, y5_array=None, y5_label="", ls5='-', color4='red',
             x_fill=None, y_fill=None, x2_fill=None, y2_fill=None,
             fill1_label=None, fill2_label=None,
             fill_color_1="green", fill_color_2="blue",
             x_label="", y_label="", x_lima=None, x_limb=None, y_lima=None, y_limb=None, loc=0,
             fig_width=DEF_FIG_WIDTH, fig_height=DEF_FIG_HEIGHT, axis_font_size=DEF_AXIS_SIZE,
             tick_font_size=DEF_TICK_SIZE):
    """
    Many defaults to it is easy to adjust
    """
    rc('text', usetex=True)
    # a general purpose plotting routine; can plot between 1 and 5 curves
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.plot(x_array, y1_array, ls1, label=y1_label, linewidth=2, color=color1)
    if y2_array is not None:
        if x2_array is None:
            x2_array = x_array
        ax.plot(x2_array, y2_array, label=y2_label, ls=ls2, linewidth=2, color=color2)
    if y3_array is not None:
        if x3_array is None:
            x3_array = x_array
        ax.plot(x3_array, y3_array, label=y3_label, ls=ls3, linewidth=3, color='green')
    if y4_array is not None:
        if x4_array is None:
            x4_array = x_array
        ax.plot(x4_array, y4_array, label=y4_label, ls=ls4, linewidth=3, color=color4)
    if y5_array is not None:
        if x5_array is None:
            x5_array = x_array
        ax.plot(x5_array, y5_array, label=y5_label, ls=ls5, linewidth=3, color='purple')
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

    if x_fill is not None:
        plt.fill_between(x_fill, y_fill, 0, color=fill_color_1, alpha='0.75')

    if x2_fill is not None:
        plt.fill_between(x2_fill, y2_fill, 0, color=fill_color_2, alpha='0.5')

    ax.tick_params(labelsize=tick_font_size)
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    if len(y1_label) > 0:
        ax.legend(loc=loc, fontsize=tick_font_size, )
    if fill1_label and fill2_label:
        p1 = Rectangle((0, 0), 1, 1, fc=fill_color_1, alpha=0.75)
        p2 = Rectangle((0, 0), 1, 1, fc=fill_color_2, alpha=0.5)
        ax.legend([p1, p2], [fill1_label, fill2_label], loc=loc, fontsize=tick_font_size, )
    ax.xaxis.grid(True, 'minor')
    ax.yaxis.grid(True, 'minor')
    ax.xaxis.grid(True, 'major', linewidth=1)
    ax.yaxis.grid(True, 'major', linewidth=1)
    save_figure(name)
