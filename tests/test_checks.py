#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Felipe Santana Rojas
# Date: 2023-06-07
# Filename: test_checks.py
# License: MIT License
import os
import unittest

import cpu_health_checks.cpu_health as cpu_health


class SystemTestCase(unittest.TestCase):
    def setUp(self):
        # Get the directory path of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the paths relative to the project root directory
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.config_file_path = os.path.join(project_root, 'cpu_health_checks', 'config',
                                             'configuration.yml')
        self.logs_folder_path = os.path.join(project_root, 'cpu_health_checks', 'logs')

        self.cpu_check = cpu_health.CPUCheck(config_file=self.config_file_path,
                                             logs_folder=self.logs_folder_path)

    def test_disk_space_min_percent_hundred(self):
        """
        Test case to check if check_enough_disk_space
        returns False when the min_percent_disk required is set to 100.
        """
        self.cpu_check.min_percent_disk = 100
        result = self.cpu_check.check_enough_disk_space()
        self.assertFalse(result, 'check_enough_disk_space is not False')

    def test_idle_usage_max_cpu_zero_hundred(self):
        """
        Test case to check if check_enough_idle_usage returns True when max_cpu_usage is 100.
        """
        self.cpu_check.max_cpu_usage = 100
        result = self.cpu_check.check_enough_idle_usage()
        self.assertTrue(result, 'check_enough_idle_usage is not True')

    def test_code_execution_minimums(self):
        """
        Test case to check if the code execution completes successfully with minimum parameters.

        The idea of this test is to check that the entire main() execution works with no problems
        when using the minimum values allowed for all the parameters that are restricted to a
        minumum limit. It also confirms that the checks check_enough_disk_space,
        check_enough_idle_usage, and check_fast_latency, provide the expected results given the
        input parameters.

        Raises:
            AssertionError: If the code execution fails with an exception.
        """
        print(" ")
        print(f"speedlog path and filename:"
              f"{self.cpu_check.logs_folder}/{self.cpu_check.speed_log_filename}")
        print(" ")
        try:
            result = cpu_health.main(min_gb=0, min_percent_disk=0, folders_to_print=0,
                                     max_cpu_usage=0, max_connection_attempts=1,
                                     block_size=1, sleep_time=0, minimum_previous_tests=1,
                                     std_deviations_limit=0, speed_min_mbps=0,
                                     minimum_download_time=0, latency_limit_ms=0,
                                     min_percent_battery=0, min_remaining_time_mins=0,
                                     config_file=self.config_file_path,
                                     logs_folder=self.logs_folder_path)
        except Exception as e:
            self.fail(f"Code execution failed with exception: {str(e)}")

        self.assertTrue(result['check_enough_disk_space'], 'check_enough_disk_space is not True')
        self.assertFalse(result['check_enough_idle_usage'], 'check_enough_idle_usage is not False')
        if 'check_fast_latency' in result:
            self.assertFalse(result['check_fast_latency'], 'check_fast_latency is not False')
        if 'check_enough_battery_charge' in result:
            self.assertTrue(result['check_enough_battery_charge'],
                            'check_enough_battery_charge is not True')

    def test_raises_when_no_config(self):
        """
        Test case to check if FileNotFoundError is raised when the config file is not found.

        Raises:
            FileNotFoundError: If the config file is not found.
        """
        with self.assertRaises(FileNotFoundError):
            cpu_health.main(config_file='no_one_can_have_this_file')

    def test_argument_validity(self):
        """
        Test case to check if Error is raised for invalid main() arguments or values.

        Returns:
            None

        Raises:
            TypeError: If an argument is of the wrong type, or is an invalid argument of main().
            ValueError: If an argument has an invalid value.
        """
        with self.assertRaises(TypeError):
            cpu_health.main(config_file=self.config_file_path,
                            logs_folder=self.logs_folder_path, min_gb='2')
        with self.assertRaises(TypeError):
            cpu_health.main(config_file=self.config_file_path,
                            logs_folder=self.logs_folder_path, max_gb=2)
        with self.assertRaises(ValueError):
            cpu_health.main(config_file=self.config_file_path,
                            logs_folder=self.logs_folder_path, min_gb=-1)


if __name__ == '__main__':
    unittest.main()
