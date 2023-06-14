Description
===========

The CPU Health Checks package provides a comprehensive set of CPU health check functionalities. It consists of three modules:

1. `cpu_health.py`: This module contains the core functionality of the package. It includes the `CPUCheck` class, which is responsible for performing the CPU health checks. It also provides a `main` function that serves as a wrapper to create a `CPUCheck` object and execute all the health checks. The `cpu_health` module relies on the `utilities` module for supporting functions.

2. `utilities.py`: This module contains supporting functions that are used by the `cpu_health` module. These functions handle tasks such as reading the configuration file, calculating disk space, checking network connectivity, measuring download speed, and more.

3. `test_checks.py`: This module contains unit tests for the `cpu_health` module. It includes various test cases to ensure the correctness of the CPU health checks.

Preparation
-----------

First we need to make sure that the modules of cpu_health_checks are available for us.
For that we need to either pip install the cpu_health_checks package, or git clone the cpu_health_checks repo. If you clone the repo you can run the modules from the folder containing the cpu_health_checks package, or you can add that folder to your PYTHONPATH (See the `Installing Section <https://cpu-health-checks.readthedocs.io/en/latest/Installing.html>`_. for instructions on how to do that) and run the modules from any folder, which is recommended.

Then make sure that the configuration file exists and has a main key containing all the necessary input parameters. Then check that the config_file and config_mode values are correct either by using the default values in CPUCheck.__init__, or explicitly defining them when calling CPUCheck() or main().

Finally make sure that the logs folder exists and is properly defined in the logs_folder parameter, either in the configuration file or defining it explicitly when calling CPUCheck() or main().

If you have cloned the git repo and are running the modules from the package folder, the provided configuration file and the logs folder will correspond to the default values defined by default in the config_file, and logs_folder parameters, so you don't need to worry about those unless you want to change them.

If you have pip installed the cpu_health_checks package you would be able to import it using statements like `import cpu_health_checks.cpu_health as cpu_health`, `import cpu_health_checks.utilities as utilities`, and `import cpu_health_checks.tests.test_checks as test_checks`. If you have git cloned the package you would also be able to run the main module directly by doing "python path/to/cpu_health_package/cpu_health.py" replacing "path/to/cpu_health_package/" with the actual package where the package is located.

General Flow/Usage
------------------

The general flow of using the CPU Health Checks package is as follows:

1. First Alternative: Run individual checks on CPUCheck object.

   1.1 Create an instance of the `CPUCheck` class using the CPUCheck() constructor and use the input parameters specified by default in the configuration file or by override the one you want during instantiation. For example do checkobj = CPUCheck(min_gb=100) if you want to use a value for min_gb that is different than the one in the configuration file. After instantiation you can also modify any of the input parameters by changing the corresponding attribute of the object (for example checkobj.min_gb=200).

   1.2 Call the desired methods of the `CPUCheck` object to perform specific CPU health checks. These methods include `check_pending_reboot`, `check_enough_disk_space`, `check_enough_idle_usage`, `check_network_connection`, `check_download_speed`, `check_latency`, and `check_battery_charge`.

   1.3 Retrieve the results of the health checks and take appropriate actions based on the returned values.

2. Second Alternative: Run all checks at once by either

   2.1 Run the `cpu_health.py` module in interactive mode (e.g., with ipython or `python -i`) and once in there run `main()` using the desired input parameters to override the configuration file. For example: `main(logs_folder='logs/linux/', latency_url='www.example.com')`. Or...

   2.2 Run the `main` function wrapper with the default values in the configuration file automatically from the command line by adding the word "auto" after indicating the module name. For example, type: `python cpu_health.py auto`.

3. Third Alternative: Import the cpu_health_check modules from other locations.

   3.1 In a module heading or in the python interpreter, you can do `import cpu_health_checks.cpu_health as cpu_health`, `import cpu_health_checks.utilities as utilities`, and `import cpu_health_checks.tests.test_checks as test_checks` to import the main modules of the package and then use them as needed. Adjust the module alias or the import syntax as preferred.

Each component of the CPU Health Checks package has a specific role:

- `CPUCheck`: This class encapsulates the CPU health checks and provides an interface to configure and execute the checks. It utilizes the supporting functions in the `utilities` module.

- `utilities`: This module contains functions that handle various tasks related to CPU health checks. These functions are called by the `CPUCheck` class to perform specific checks or retrieve information.

- `test_checks`: This module tests the behavior of the product. Some checks will return False, indicating that the check didn't pass, which doesn't necessarily mean there is an error in the code; it is just the expected output of the check. However, `test_checks` checks if the behavior of the product is correct by running multiple unittests where the expected result is known a priori given the input parameters. For example, we test if `CPUCheckObj.check_enough_disk_space()` returns False when the `min_percent_disk` attribute of the `CPUCheckObj` object is 100, because we assume that at least some part of the disk is used. Some of these tests should return True, some should return False, and some should raise exceptions. If everything goes as expected, the general test prints "OK" at the end; otherwise, it indicates which tests failed.
