#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Felipe Santana Rojas
# Date: 2023-06-07
# Filename: utilities.py
# License: MIT License
import heapq
import logging
import logging.handlers
import os
import platform
import re
import subprocess
import time
import urllib.request

import numpy as np
import yaml
from tqdm import tqdm


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def load_configuration(config_file, config_mode):
    """
    Load configuration from a YAML file based on the specified mode.

    Args:
        config_file (str): The path to the configuration file.
        config_mode (str): The mode to select from the configuration file.

    Returns:
        dict or None: The configuration dictionary for the given mode, or None if an error occurs.
    """
    try:
        with open(config_file, 'r') as f:
            config_dict = yaml.safe_load(f)[config_mode]
        return config_dict
    except KeyError:
        print(f"Error: '{config_mode}' key not found in the configuration file '{config_file}'.")
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
    except IsADirectoryError:
        print(f"Error: '{config_file}' is a directory, not a file.")
    except PermissionError:
        print(f"Error: Permission denied while accessing the configuration file '{config_file}'.")
    except Exception as e:
        print(f"Error: An unexpected error occurred while loading the configuration file: {e}")

    return None


def get_input_params(function_params, function_values, config_file, config_mode):
    """
    Gets the input parameters to be used for a given function.

    It used the parameters explicitly defined when calling the function and if not it uses
    the ones present in a configuration file, but all the parameters of the function signature
    have to be present in one of those two.
    """
    function_params_config = ['config_file', 'config_mode']

    # Here I convert main_params into a dictionary and remove the configuration related
    # parameters because they have already been used and they have to be defined in the
    # main function
    function_params = {k: v for k, v in function_params.items() if k not in function_params_config}

    config_dict = load_configuration(config_file, config_mode)
    if not config_dict:
        raise FileNotFoundError(f'Configuration File: {config_file} was not found')

    # First we check if there are invalid keys in the configuration file
    wrong_config_keys = [key for key in config_dict if key not in function_params]
    for key in wrong_config_keys:
        print(f"Ignoring invalid configuration parameter '{key}'")

    input_values = {}
    for param in function_params:
        if param in function_values:  # If it is explicitly set on main use that value
            input_values[param] = function_values[param]
        else:  # If not use the value defined in config (if it is not there through an error)
            assert param in config_dict, (f'{param} not defined in config'
                                          f'file nor in main arguments')
            input_values[param] = config_dict[param]
    return input_values


def run_command(command):
    """
    Run a command in the shell and capture the output.

    Args:
        command (str): The command to run.

    Returns:
        CompletedProcess: The result of running the command.
    """
    return subprocess.run(command, shell=True, capture_output=True, text=True)


def print_message(message, new_line=True):
    """ Print a message in green color."""
    if new_line:
        print(bcolors.OKGREEN + message + bcolors.ENDC)
    else:
        print(bcolors.OKGREEN + message + bcolors.ENDC, end='')


def print_error(message, new_line=True):
    """ Print an error message in red color."""
    if new_line:
        print(bcolors.FAIL + message + bcolors.ENDC)
    else:
        print(bcolors.FAIL + message + bcolors.ENDC, end='')


def print_warning(message):
    """ Print a warning message in yellow color."""
    print(bcolors.WARNING + message + bcolors.ENDC)


def print_and_log_result(result, message_passed, message_failed, logger):
    """
    Performs the common practice that based on the result of a check we print a message if result
    is True, or an error if result is False, and then log the corresponding message as info.
    """
    if result:
        print_message(message_passed)
        logger.info(message_passed)
    else:
        print_error(message_failed)
        logger.info(message_failed)


def get_home_folder_info():
    """
    Get information about the home folder.

    Returns:
        tuple: A tuple containing the home folder usage (in MB) and sizes of subfolders.
    """
    home = os.path.expanduser("~")
    home_usage = get_folder_size(home)
    subfolders = [os.path.join(home, folder) for folder in os.listdir(home)
                  if os.path.isdir(os.path.join(home, folder))]
    subfolders_sizes = {folder: get_folder_size(folder) for folder in subfolders}

    return home_usage, subfolders_sizes


def get_folder_size(folder):
    """
    Get the size of a folder in bytes if there is permission to check it otherwise returns 0

    Args:
        folder (str): Path to the folder.

    Returns:
        int: Size of the folder in bytes.
    """
    if os.name == 'nt':  # Windows
        folder = folder.replace('"', r'\"')  # Escape double quotes
        command = 'dir /s /a /q "{}" | find /i "File(s)"'.format(folder)
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        if output.strip() == '':
            size = 0
        else:
            size = int(output.split()[-2]) / 2**20  # Convert to MB
    else:  # Unix-like systems
        command = 'du -sk "{}" 2>/dev/null || true'.format(folder)
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        if output.strip() == '':
            size = 0
        else:
            size = int(output.split()[0]) / 2**10  # Convert to MB

    return size


def get_largest_subfolders(folders_to_print, subfolders_sizes):
    """
    Get the largest subfolders based on their sizes.

    Args:
        folders_to_print (int): The number of folders to print.
        subfolders_sizes (dict): A dictionary containing subfolder sizes.

    Returns:
        list: A list of tuples containing the largest subfolders and their sizes.
    """
    return heapq.nlargest(folders_to_print, subfolders_sizes.items(), key=lambda item: item[1])


def downloads_file(url, block_size, max_attempts, logger, track_progress):
    """
    Performs a null download of the file in the url.

    File is downloaded by splitting it into blocks, trying (max_attempts) of times to establish
    connection.
    If it doesn't work it returns False and logs an error. If it succeeds returns True
    If track_progress is True then it displays a progress bar while downloading.
    """
    attempt = 1
    while attempt <= max_attempts:
        try:
            response = urllib.request.urlopen(url)
            break
        except (urllib.error.URLError, ConnectionResetError):
            if attempt == max_attempts:
                print_error(f'Failed to establish connection after '
                            f'{max_attempts} attempts', logger)
                return False
            # Wait more every time before retrying
            print_warning(f'Trying to establish connection again after {2 * attempt} seconds')
            time.sleep(2 * attempt)
            attempt += 1

    file_size = int(response.headers['Content-Length'])

    # In the definitive download test we create a progress bar and updated accordingly
    if track_progress:
        progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, ncols=80)

    # Here we download the file into dev/null splitting in it into blocks and breaking when is over
    with open("/dev/null", 'wb') as file:
        while True:
            buffer = response.read(block_size)
            if not buffer:
                break
            file.write(buffer)
            if track_progress:
                progress_bar.update(len(buffer))

    response.close()
    return True

    if track_progress:
        progress_bar.close()


def handle_final_download_test(logs_folder, speed_log_filename, size, download_time,
                               download_speed_mbps, minimum_previous_tests, std_deviations_limit,
                               speed_min_mbps):
    """
    Handles the result of the download used to measure speed.

    This function stores the value in the speed logs, and checks if the speed is below the absolute
    minimum threshold or if it is too slow compared to usual values obtained if there are enough
    previous tests to make a significant comparison.


    Args:
        logs_folder (str): The folder to store the log files.
        speed_log_filename (str): The name of the speed log file.
        size (str): The size of the file downloaded to measure speed.
        download_time (float): The download time in seconds.
        download_speed_mbps (float): The download speed in Mbps.
        minimum_previous_tests (int): The minimum number of previous tests required to compare
            current results with results usually obtained.
        std_deviations_limit (int): The number of standard deviations used for comparison.
            If the current download speed is less than the average speed minus
            'std_deviations_limit' times the standard deviation of the speed, this function returns
            False which implied that check_download_speed will not pass.

        speed_min_mbps (float): The minimum download speed threshold in Mbps.

    Returns:
        bool: True if there is an error, False otherwise.
    """

    speed_log_filename = f'{logs_folder}/{speed_log_filename}'
    log_file_exits = os.path.isfile(speed_log_filename)
    local_time = time.localtime(time.time())

    # If the file doesnt exist yet we create the header and write the results in it
    # if not it appends the results to the current file
    if log_file_exits:
        speed_log = open(speed_log_filename, 'a')
    else:
        speed_log = open(speed_log_filename, 'w')
        speed_log.write('Year  Month  Day  HH:MM  Download_Time[s]  Download_Speed[Mb/s]')

    # Here results of the speed download test are written in the speed log along with a timestamp
    speed_log.write('\n' + time.strftime("%Y     %m   %d  %H:%M", local_time))
    speed_log.write(f'{download_time:18.2f} {download_speed_mbps:21.2f}')
    speed_log.close()

    # Here we check how many download test have been performed previously
    wordcount_command = f'wc -l {speed_log_filename}'
    with os.popen(wordcount_command) as wc_proc:
        lines_in_log = int(wc_proc.read().split()[0])

    # If there are not enough previous test to perform a significant comparison between the current
    # results and prior results, then it doesn't make the comparison and prints a warning message
    enough_previous_tests = True
    if lines_in_log < minimum_previous_tests + 1:
        enough_previous_tests = False
        print_warning(f'There are not enough prior download tests ({lines_in_log - 1} out of a '
                      f'minimum of {minimum_previous_tests}) to compare the current results with '
                      f'the usual value')

    # If there are enough previous test to perform a significant comparison between the current
    # results and prior results it checks whether the current result is less than the average
    # minus a given number of times the standard deviation and if it is sets speed_outlier to True
    speed_outlier = False
    if enough_previous_tests:
        with os.popen(f"awk '{{print $6}}' {speed_log_filename}") as prior_speeds_proc:
            prior_speeds_command_output = prior_speeds_proc.read().split()[1:-1]
        prior_speeds = list(map(float, prior_speeds_command_output))
        avg_speed, speed_std = np.average(prior_speeds), np.std(prior_speeds)
        err_msg = ''

        if download_speed_mbps < (avg_speed - std_deviations_limit * speed_std):
            err_msg += (f' is too low compared to regular values '
                        f'(more than {std_deviations_limit} standard deviations '
                        f'less than average)')
            speed_outlier = True

    speed_below_absmin = False

    # Here it checks if the current result is below the absolute minimum threshold and if it is
    # it sets speed_below_absmin to True. It also adjusts the error message so that it has the
    # information of any of the types of failure possible (too low, or outlier).
    if download_speed_mbps < speed_min_mbps:
        speed_below_absmin = True
        if speed_outlier is True:
            err_msg += (',\nand it is below the absolute minimum cut '
                        f'({speed_min_mbps:.1f} Mb/s)')
        else:
            err_msg += (f' is below the absolute minimum cut '
                        f'({speed_min_mbps:.1f} Mb/s)')

    message_out1 = f'Download Speed: {download_speed_mbps:.2f} Mb/s'

    # If speed_outlier or speed_below_absmin are True then returns False
    if speed_outlier or speed_below_absmin:
        print_error(message_out1 + err_msg)
        return False
    else:
        return True


def get_megas(size):
    """
    Convert a string with bytes info into the number of corresponding mega bytes
    """
    if size[-2:] == 'MB':
        megas = int(size[:-2])
    if size[-2:] == 'GB':
        megas = int(size[:-2]) * 2**10
    return megas


def get_configured_logger(log_object_name, log_file_name):
    """ Configures a logger with RotatingFileHandler and retrieves it."""
    logger = logging.getLogger(log_object_name)
    logger.setLevel(logging.DEBUG)

    # Create a rotating file handler
    handler = logging.handlers.RotatingFileHandler(log_file_name, maxBytes=1024, backupCount=0)
    handler.setLevel(logging.DEBUG)

    # Define the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)
    return logger


def determines_log_filename():
    """
    Determines the log filename based on major system properties.

    This way we can facilitate the comparison between the performance
    of the different test across different machines.
    """
    computer_info = platform.uname()
    machine = re.sub(r'\.|\s', '_', computer_info.machine)
    system = re.sub(r'\.|\s', '_', computer_info.system)
    node = re.sub(r'\.|\s', '_', computer_info.node)
    return '_'.join([machine, system, node]) + '.log'


def check_arguments_validity(arguments):
    """
    Check the validity of input arguments based on their types and specified boundaries.

    Args:
        arguments (dict): A dictionary containing the input arguments and their values.

    Raises:
        TypeError: If an argument's value does not match the allowed types.
        ValueError: If an argument's value is outside the specified minimum or maximum bounds.

    Returns:
        None
    """
    arg_types = {'logs_folder': [str], 'min_gb': [int, float], 'min_percent_disk': [int, float],
                 'folders_to_print': [int], 'max_cpu_usage': [int, float],
                 'website_to_check': [str], 'max_connection_attempts': [int],
                 'file_sizes_to_download': [list], 'block_size': [int], 'sleep_time': [int, float],
                 'speed_log_filename': [str], 'minimum_previous_tests': [int],
                 'std_deviations_limit': [int, float], 'speed_min_mbps': [int, float],
                 'minimum_download_time': [int, float], 'latency_url': [str],
                 'latency_limit_ms': [int, float], 'min_percent_battery': [int, float],
                 'min_remaining_time_mins': [int, float]}

    min_values = {'min_gb': 0, 'min_percent_disk': 0, 'folders_to_print': 0, 'max_cpu_usage': 0,
                  'max_connection_attempts': 1, 'block_size': 1, 'sleep_time': 0,
                  'minimum_previous_tests': 1, 'std_deviations_limit': 0,
                  'speed_min_mbps': 0, 'minimum_download_time': 0,
                  'latency_limit_ms': 0, 'min_percent_battery': 0, 'min_remaining_time_mins': 0}

    max_values = {'min_percent_disk': 100, 'max_cpu_usage': 100, 'max_connection_attempts': 10,
                  'sleep_time': 20, 'min_percent_battery': 100}

    for argument in arguments:
        value = arguments[argument]
        curr_type = type(value)
        allowed_types = arg_types[argument]
        if curr_type not in allowed_types:
            raise TypeError(f'Argument {argument} should be of type {allowed_types}'
                            f' not {curr_type}')
        if argument in min_values:
            if value < min_values[argument]:
                raise ValueError(f'Value {value} of argument {argument} is smaller than allowed'
                                 f' minimum of {min_values[argument]}')
        if argument in max_values:
            if value > max_values[argument]:
                raise ValueError(f'Value {value} of argument {argument} is larger than allowed'
                                 f' maximum of {max_values[argument]}')
