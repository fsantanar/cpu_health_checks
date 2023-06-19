#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Felipe Santana Rojas
# Date: 2023-06-07
# Filename: utilities.py
# License: MIT License
import datetime
import inspect
import os
import re
import shutil
import socket
import sys
import time

import psutil

import cpu_health_checks.utilities as utilities


class CPUCheck:
    """
    A class for performing CPU-related checks and tests.

    Methods:
        check_no_pending_reboot(): Returns boolean indicating if the PC has no pending reboots.\n
        check_enough_disk_space(): Returns boolean indicating if there is enough disk space.\n
        check_enough_idle_usage(): Returns boolean indicating if the CPU has enough idle usage.\n
        check_network_available(): Returns boolean indicating if network is available.\n
        check_good_download_speed(): Returns boolean indicating if the download speed is above a
        threshold and is not a low outlier.\n
        check_fast_latency(): Returns boolean indicating if latency is fast.\n
        check_enough_battery_charge(): Returns boolean indicating if there is enough
        battery charge left.\n

    """

    def __init__(self, config_file='../../config/configuration.yml', config_mode='default',
                 logs_folder=None, min_gb=None, min_percent_disk=None, folders_to_print=None,
                 max_cpu_usage=None, website_to_check=None, max_connection_attempts=None,
                 file_sizes_to_download=None, block_size=None, sleep_time=None,
                 speed_log_filename=None, minimum_previous_tests=None, std_deviations_limit=None,
                 speed_min_mbps=None, minimum_download_time=None, latency_url=None,
                 latency_limit_ms=None, min_percent_battery=None, min_remaining_time_mins=None):
        """
        **CPUCheck object __init__ constructor:**

        This method creates the CPUCheck object using multiple input parameters that can be defined
        explicitly when calling the constructor or if not taken from the 'config_mode' key of the
        'config_file' configuration file, but every parameter from the method signature has to be
        defined in at least one of the two.

        The method checks that all the input parameters have the proper type and if it corresponds
        it also check if the value is within the corresponding min and max limits.
        It also starts a logger to store the results of the check methods.

        Args:
            config_file (str): Path to the configuration file.
            Default: 'config/configuration.yml'.\n
            config_mode (str): Configuration mode to use. Default: 'default'.\n
            logs_folder (str): Path to the folder where logs are stored. The general log filename
            is based on major system properties to facilitate comparison of results across
            platforms/computers.\n
            min_gb (float): Minimum required free disk space in GB.\n
            min_percent_disk (float): Minimum required free disk space as a percentage.\n
            folders_to_print (int): Number of largest subfolders to print.\n
            max_cpu_usage (float): Maximum allowed CPU usage percentage.\n
            website_to_check (str): Website URL to check network connectivity.\n
            max_connection_attempts (int): Number of times to attempt connection
            before giving up.\n
            file_sizes_to_download (list): List of file sizes to download for testing.
            The full list of sizes from which you can choose is:
            1MB, 10MB, 100MB, 1GB, 10GB, 50GB, 100GB, and 1000GB.
            Although very large files are not recommended due to large download times.\n
            block_size (int): Block size for downloading files.\n
            sleep_time (float): Sleep time between download requests used to avoid overloading the
            server.\n
            speed_log_filename (str): Name of the download speed log file.\n
            minimum_previous_tests (int): Minimum number of previous download tests to perform
            comparison between current and previous values obtained.\n
            std_deviations_limit (float): Standard deviations limit
            for comparing download speeds.\n
            check_good_download_speed will not pass if the current download speed is less than
            the average speed minus 'std_deviations_limit' times the standard deviation of the
            speed.\n
            speed_min_mbps (float): Minimum required download speed in Mbps.\n
            minimum_download_time (float): Minimum required download time in seconds.
            In check_good_download_speed, files are downloaded from smaller to larger to ensure
            that a file is large enough for accurate speed measurement but not too large to
            take too long. If the download time of a file is more than 'minimum_download_time',
            the final file used to measure the download speed will be the next file in terms of
            size, which is usually 10 times bigger.\n
            latency_url (str): URL to be used for latency check.\n
            latency_limit_ms (float): High limit in milliseconds for the latency check to pass.\n
            min_percent_battery (float): Minimum battery charge as a percentage.\n
            min_remaining_time_mins (float): Minimum remaining battery charge in minutes.\n


        Example configuration file ('config/configuration.yml'):

        .. code-block:: yaml

            'default':
              # General
              logs_folder: 'logs/'

              # check_enough_disk_space
              min_gb: 2
              min_percent_disk: 10
              folders_to_print: 3

              # check_enough_idle_usage
              max_cpu_usage: 75

              # check_network_available
              website_to_check: 'www.google.com'

              # check_good_download_speed
              max_connection_attempts: 5
              file_sizes_to_download: ['1MB', '10MB', '100MB', '1GB', '10GB']
              block_size: 8192
              sleep_time: 1
              speed_log_filename: 'download_speed_register.txt'
              minimum_previous_tests: 3
              std_deviations_limit: 2
              speed_min_mbps: 1
              minimum_download_time: 3

              # check_fast_latency
              latency_url: 'www.google.com'
              latency_limit_ms: 100

              # check_enough_battery_charge
              min_percent_battery: 10
              min_remaining_time_mins: 15
        """

        init_params = inspect.signature(self.__init__).parameters
        locals_copy = locals()
        init_values = {k: locals_copy[k] for k in init_params if locals_copy[k] is not None}
        # Here get the input values to be used to instantiate the CPUCheck object
        input_values = utilities.get_input_params(init_params, init_values,
                                                  config_file, config_mode)
        # Here we check that the arguments have the proper type and are within accepted limits
        utilities.check_arguments_validity(input_values)

        for key, val in input_values.items():
            setattr(self, key, val)  # Put all the values in the dictionary as object attributes

        # Checks if the log folder exists
        if not os.path.exists(self.logs_folder):
            raise FileNotFoundError(f'Log folder {self.logs_folder} was not found. '
                                    f'Please create it and make sure the logs_folder parameter\n'
                                    f'is properly defined in the configuration file or when'
                                    f' calling main() or CPUCheck()')
        # Determines the log filename based on important system properties
        log_filename = utilities.determines_log_filename()
        log_folder_and_name = os.path.join(self.logs_folder, log_filename)
        # sets logger attribute as the logger configured in the utilities method
        self.logger = utilities.get_configured_logger('my_logger', log_folder_and_name)
        self.logger.info('Input Paramters Used for CPUCheck Object:')
        self.logger.info(input_values)

    def check_no_pending_reboot(self):
        """Returns True if the computer has no pending reboots and False if it has"""
        result = not(os.path.exists('/run/reboot-required'))
        utilities.print_and_log_result(result, 'No Pending Reboots', 'Pending Reboot(s) Found',
                                       self.logger)
        return result

    def check_enough_disk_space(self):
        """
        Checks if there is enough disk space available.

        Checks the disk space available, and if the disk space is above the minimum limit
        and the fraction of free space is above the minimum required then it returns True

        If there is no enough space it gives you a hint on how to free space indicating
        the largest home subfolders.
        """
        du = shutil.disk_usage('/')
        percent_free = 100 * du.free / du.total
        gigabytes_free = du.free / 2**30
        # Here we calculate the size of home
        home = os.path.expanduser("~")
        home_usage = utilities.get_folder_size(home)

        main_message = (f'{gigabytes_free:.1f} Gb free ({percent_free:.2f}%) out of a total '
                        f'of {du.total/2**30:.1f} Gb. Home folder is {home_usage:.2f} Gb')
        enough_gb_avail = gigabytes_free >= self.min_gb
        enough_frac_avail = percent_free >= self.min_percent_disk
        result = enough_gb_avail and enough_frac_avail

        if not(result):
            utilities.print_error('Disk too close to full', self.logger)

            # Here we calculate the largest subfolders to print as indicator on how to clear space
            subfolders_sizes = utilities.get_home_subfolder_info()
            largest_subfolders = utilities.get_largest_subfolders(self.folders_to_print,
                                                                  subfolders_sizes)
            utilities.print_error('To give a hint on where to clear space, the largest home'
                                  ' subfolders are:')
            for subfolder in largest_subfolders:
                utilities.print_error(f'    {subfolder[0]} is {subfolder[1]:.2f} Gb')

        utilities.print_and_log_result(result, main_message, main_message, self.logger)

        return result

    def check_enough_idle_usage(self):
        """Returns True if the CPU has enough idle usage."""
        cpu_usage = psutil.cpu_percent(1)
        if cpu_usage == 0:
            cpu_usage = 0.01  # Just to avoid edge problems in tests
        main_message = f'CPU usage is {cpu_usage:.2f}%'
        result = cpu_usage <= self.max_cpu_usage
        utilities.print_and_log_result(result, main_message, main_message, self.logger)
        return result

    def check_network_available(self):
        """Return True if it suceeds to resolve the given URL, and False otherwise."""
        result = False
        try:
            socket.gethostbyname(self.website_to_check)
            message_passed = 'There is internet connection'
            message_failed = ''
            result = True
        except socket.gaierror:
            message_failed = 'Failed to resolve URL.'
        except socket.timeout:
            message_failed = 'Connection timed out.'
        except Exception:
            message_failed = 'Network check failed due to an unknown error.'
        utilities.print_and_log_result(result, message_passed, message_failed, self.logger)
        return result

    def check_good_download_speed(self):
        """
        Perform download speed tests and return the result.

        The download speed test is performed by downloading files of different sizes from a
        predefined URL. The download speed is calculated and compared against specified
        thresholds to determine if the test passes or fails. If the file is sucessfuly
        downloaded, the download speed is above the minimum limit, and the speed is not
        a low outlier compared to previous results, the method returns True, if not it
        results False.

        Returns:
            bool: True if the download speed test suceeds, False otherwise.

        Raises:
            AssertionError: If the logs folder is not a directory.

        """

        assert os.path.isdir(self.logs_folder), \
            f'To run this test you have to create folder {self.logs_folder} first with ' \
            f'mkdir {self.logs_folder} on repo\'s main folder'

        sizes = self.file_sizes_to_download
        # Last test is the one actually used for meassuring the download speed
        is_last_test = False

        message1 = 'Testing Download Speed: '
        message2a = 'Running preliminary quick tests'
        print(message1 + message2a, end='\r', flush=True)

        # We download files of increasing size until we reach one that downloads in enough
        # time for the test to be accurate
        for ind_size in range(len(sizes)):
            size = sizes[ind_size]
            url = 'http://speedtest.tele2.net/' + size + '.zip'
            start_time = time.time()

            # This function does a null download, splitting the file into blocks, performing
            # multiple attempts, and displaying a progress bar if it is the definitive test
            successful_download = utilities.downloads_file(url, self.block_size,
                                                           self.max_connection_attempts,
                                                           self.logger, is_last_test)
            end_time = time.time()
            if not(successful_download):  # If failed to download the file set the check as failed
                return False
            download_time = end_time - start_time
            megas = utilities.get_megas(size)
            download_speed_mbps = megas / download_time
            time.sleep(self.sleep_time)  # To avoid overloading the server

            # If it is the download used to measure the speed the function below logs the results,
            # checks if the speed is above the minimum, and if we can, compare it to prior results
            if is_last_test or download_time > 10 * self.minimum_download_time:
                main_message = (f'Downloaded at an average speed of {download_speed_mbps:.3f}'
                                f'Mb/s: {download_time:.2f} secs for a {megas:.1f} Mb file')
                result = utilities.handle_final_download_test(self.logs_folder,
                                                              self.speed_log_filename, size,
                                                              download_time, download_speed_mbps,
                                                              self.minimum_previous_tests,
                                                              self.std_deviations_limit,
                                                              self.speed_min_mbps)
                utilities.print_and_log_result(result, main_message, main_message, self.logger)
                return result

            # If the download time of a given file is large enough then use the next in size
            # as the definitive download to measure the speed
            if download_time > self.minimum_download_time:
                is_last_test = True
                message2b = (f'Running final download test on {sizes[ind_size+1]}'
                             f' size file (automatically discarded)')
                time.sleep(1.5)  # So that the user can see the message change
                print(message1 + message2b)

    def check_fast_latency(self):
        """
        Checks if the latency is fast measuring the average value to the given host.

        It also prints a quality flag associated to the latency value according to
        genelrally acceted benchmarks
        """

        url = self.latency_url  # URL to be used to measure average latency
        message_error = None  # This message will exist if there is any type of error
        # This limits are then used to associate a quality flag to the latency value
        quality_limits = {0: 'Excellent', 20: 'Good', 100: 'Fair', 200: 'Poor', 500: 'Very Poor'}

        # In this block we measure the average latency and catch any potential errors
        try:
            ping_output = utilities.run_command('ping -c 4 ' + url).stdout
            latency_values = re.findall(r'time=(\d+\.\d+)', ping_output)
            average_latency = sum(float(latency) for latency in latency_values)\
                / len(latency_values)
            if any(float(latency) <= 0 for latency in latency_values):
                message_error = 'Invalid (negative) latency values found.'

        except ZeroDivisionError:
            message_error = f'Failed to ping host {url}'
        except Exception as e:
            message_error = 'Latency check failed due to an unknown error:' + str(e)

        # If there was an error it prints it and returns False for the test
        if message_error is not None:
            utilities.print_error(message_error)
            return False

        # If the test didnt find any error checks if the latency was faster than the limit
        # assigns the quality flag and prints and logs the results
        result = average_latency < self.latency_limit_ms
        main_message = f"Latency to {url} was {average_latency:.2f} ms"
        latency_quality = quality_limits[max([key for key in quality_limits.keys() if key < 0.1])]
        main_message += (f" which is '{latency_quality}' "
                         f"according to generally accepted benchmarks")
        utilities.print_and_log_result(result, main_message, main_message, self.logger)

        return result

    def check_enough_battery_charge(self):
        """
        Checks battery level, plugging, and time remaining.

        Returns True if the battery has enough charge and the remaining time is not too low.
        If not, returns False and checks if the battery is plugged, if it is it recommends to
        check battery health, if it is not, it recommends to plug it.
        """

        battery_info = psutil.sensors_battery()
        percent_remaining = battery_info.percent
        time_remaining = battery_info.secsleft
        time_remaining_formatted = datetime.timedelta(seconds=time_remaining)
        plugged = battery_info.power_plugged
        # Initially we only check if the charge fraction is larger than the limit
        result = (percent_remaining >= self.min_percent_battery)

        if plugged:
            main_message = (f'The battery is plugged and has {percent_remaining}% of charge')

        else:
            main_message = (f'The battery is not plugged, has {percent_remaining}% of charge,'
                            f' and the remaining time is {time_remaining_formatted}')

            result = result and (time_remaining >= self.min_remaining_time_mins * 60)

        if not(result) and plugged:
            utilities.print_error(f'Even though the battery is plugged, the charge level of'
                                  f' {percent_remaining}% is low, so consider running check\n'
                                  f'again in a few minutes, and if this persist the battery '
                                  f'health might be compromised')
        if not(result) and not(plugged):
            utilities.print_error(f'The charge level of {percent_remaining}% is low, so please'
                                  f' consider charging your battery')

        utilities.print_and_log_result(result, main_message, main_message, self.logger)
        return result


def main(**kwargs):
    """
    The main function to execute the cpu checks based on the provided configuration.

    It starts by instantiating a CPUCheck object which by default (no kwargs provided
    at call time) is done taking all the input parameters from the 'default' main key
    of the configuration file config/configuration.yml. Then, if any kwarg is provided
    when calling the function, that parameter overrides the value in the configuration file.

    Then it runs a series of cpu health checks, which return True if the test pass and False
    otherwise. Finally it prints and logs the results indicating how many checks passed/failed.

    The list of checks to run is:
    [check_no_pending_reboot, check_enough_disk_space, check_enough_idle_usage,
    check_network_available, check_good_download_speed, and check_enough_battery_charge].
    But if check_network_available fails (returns False), check_good_download_speed and
    check_fast_latency are not run and it is set automatically to failed.
    Also the test check_enough_battery_charge is automatically skipped if there is no
    battery information available (which probably means the code is beign run on a desktop).


    Args:
        kwargs: Series of optional kwargs to be used for instantiating the CPUCheck object.
            These parameters have to be part of the CPUCheck.__init__ signature
            (see help CPUCheck.__init__ for more information), and they override the value
            present in the configuration file.

    Returns:
        dict: Dictionary whose keys are the name of the checks performed and the values
            correspond to the result of each test

    Raises:
        TypeError: If any kwargs are not part of the parameters used
            to instantiate the CPUCheck object.

    Examples:
        # Example 1: Running main without any kwargs\n
        >>> results = main()
        >>> result
        {'check_no_pending_reboot': True, 'check_enough_disk_space': True, ...}

        # Example 2: Running main with specific (and extreme) kwargs\n
        >>> results = main(min_percent_disk=100, max_cpu_usage=100)
        >>> result
        {..., 'check_enough_disk_space': False, 'check_enough_idle_usage': True, ...}

    """

    # First we check that all the kwargs are part of the
    # parameters used to instantiate the CPUCheck object
    cpucheck_pars = inspect.signature(CPUCheck.__init__).parameters
    for par in kwargs:
        if par not in cpucheck_pars:
            raise TypeError(f'Sorry, parameter {par} is not part of the parameters used'
                            f' to instantiate the CPUCheck object')
    # Create the CPUCheck object to perform the tests
    checkobj = CPUCheck(**kwargs)
    checkobj.logger.info("Starting main function")

    fails = 0
    checks = [checkobj.check_no_pending_reboot, checkobj.check_enough_disk_space,
              checkobj.check_enough_idle_usage, checkobj.check_network_available,
              checkobj.check_good_download_speed, checkobj.check_fast_latency,
              checkobj.check_enough_battery_charge]

    # In the following while block it runs the checks defined as CPUCheck methods in order
    # if one or more fail gives an error message and indicates which checks failed.
    # If the check_network_available check fails then check_good_download_speed and
    # check_fast_latency are automatically set to failed.
    # If there is no battery info the battery check is skipped but not set to failed.
    all_passed = True
    ind_check = 0
    results = {}
    while ind_check in range(len(checks)):
        check = checks[ind_check]
        checkobj.logger.info(f"Running {check.__name__}")
        if check == checkobj.check_enough_battery_charge and psutil.sensors_battery() is None:
            checkobj.logger.info('check_battery was skipped because there is no battery info')
            ind_check += 1
            continue
        result = check()
        results[check.__name__] = result
        if not(result):
            utilities.print_error(f"{check.__name__} didn't passed")
            checkobj.logger.error(f"{check.__name__} didn't passed")
            all_passed = False

            fails += 1
            if check == checkobj.check_network_available:
                fails += 2
                utilities.print_error('Since there is no network check_good_download_speed '
                                      'and check_fast_latency were automatically set to Failed')
                ind_check += 2
        ind_check += 1

    print(' ')
    print('#' * 28)
    print('###  ', end='')

    if all_passed:
        utilities.print_message('All checks passed', new_line=False)
    else:
        utilities.print_error(f'{fails:02} check(s) failed', new_line=False)

    print('  ###')
    print('#' * 28)
    checkobj.logger.info("Finished main function")
    return results


# If the user specific the 'auto' argument when running
# Then automatically run main() with no extra arguments
main_args = sys.argv
if main_args[-1] == 'auto':
    main()
