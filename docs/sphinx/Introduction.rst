Introduction
============

Overview
--------

The CPU Health Checks package is designed to perform various CPU health checks on any platform (Linux, MacOS, Windows). It provides a set of functionalities to monitor pending reboots, disk space availability, idle CPU usage, network connection status, download speed, latency, and battery charge. The package consists of three modules: `cpu_health.py`, `utilities.py`, and `test_checks.py`.

Goals
-----

The main goals of the CPU Health Checks package are:

- Perform comprehensive CPU health checks across different platforms.
- Provide an easy-to-use interface to monitor critical aspects of CPU health.
- Allow flexibility by enabling users to override default configuration parameters.
- Facilitate automation by providing a main function that performs all the health checks.
- Storing results on log files to check for trends in time and possible performance outliers.

Results
-------

Each check function returns True if the check passed (for example if there is enough disk space),
and False otherwise. Calling the main() wrapper function in cpu_health.py returns a dictionary
Where the keys are the name of the checks performed and the values are the result of the 
corresponding test.

All the general information and timestamps are written into a general log file, and 
another log file dedicated only to monitor the internet download speed.

Finally the functions print colored messages on screen to clearly highlight when the checks passed,
when they didn't (providing extra information on why the didn't), and when the usage, file content,
or input parameters raised an exception that prevented the check to be performed.

