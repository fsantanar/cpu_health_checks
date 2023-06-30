Description
===========

The CPU Health Checks package provides a comprehensive set of CPU health check functionalities. It consists of three modules:

1. `cpu_health.py`: This module contains the core functionality of the package. It includes the `CPUCheck` class, which is responsible for performing the CPU health checks. It also provides a `main` function that serves as a wrapper to create a `CPUCheck` object and execute all the health checks. The `cpu_health` module relies on the `utilities` module for supporting functions.

2. `utilities.py`: This module contains supporting functions that are used by the `cpu_health` module. These functions handle tasks such as reading the configuration file, calculating disk space, checking network connectivity, measuring download speed, and more.

3. `test_checks.py`: This module contains unit tests for the `cpu_health` module. It includes various test cases to ensure the correctness of the CPU health checks.

Preparation
-----------

First make sure that the configuration file config/configuration.yml (with respect to package root folder) main key (default value is "default") has the input parameter values you want to use. Then check that the "config_file" default parameter value corresponds to the location of the configuration file with respect to the folder where you are running the modules. If not You can change this value when calling CPUCheck() or main().

Finally make sure that the logs folder exists and its locations with respect to the folder where you are running the modules is properly defined in the "logs_folder" parameter, either using the value in the configuration file or defining it explicitly when calling CPUCheck() or main().

If you are running the modules from folder src/cpu_health_checks (their default location), the configuration file and the logs folder will correspond to the default values  in the "config_file", and "logs_folder" parameters, so you don't need to worry about those unless you want to change them.

After installing the package you would be able to import the modules using statements like `import cpu_health_checks.cpu_health as cpu_health`, or `import cpu_health_checks.utilities as utilities`.
If you have git cloned the package you would also be able to run the Python modules directly by doing "python path/to/cpu_health_module_folder/cpu_health.py" replacing "path/to/cpu_health_module_folder/" with the actual folder containing the cpu_health.py and utilities.py modules.

General Flow/Usage
------------------

The main ways to run the CPU health checks are the following:

1. Running individual checks: You can create an instance of the CPUCheck class and call specific methods to perform individual CPU health checks. For example:

   .. code-block:: python

      import cpu_health_checks.cpu_health as cpu_health

      # Create a CPUCheck object
      checkobj = cpu_health.CPUCheck()

      # Perform specific health checks
      res1 = checkobj.check_enough_disk_space()
      res2 = checkobj.check_enough_idle_usage()
      res3 = checkobj.check_network_connection()
      # ... add more checks as needed
      # Retrieve the results and take actions based on the returned values
      
   Each check function returns True if the check passed and False otherwise.

   Remember that if you have git cloned the package you can also do this by running the cpu_health.py module from the terminal using python interactive mode and then in the python interpreter create the object doing for example checkobj = CPUCheck().

2. Running all checks at once: you can run all the CPU health checks at once using the main() wrapper function. There are two ways to do this:

   a. Execute the main() function of cpu_health.py using the default parameters defined in the .yml configuration file, and the default values for "config_file", and "config_mode" defined in the CPUCheck() constructor. For example:

      In Python, first import the cpu_health module:

      .. code-block:: python

         import cpu_health_checks.cpu_health as cpu_health

      And then run the main() function with the default input parameters without explicitly defining any parameter at call time:

      .. code-block:: python

         main()

      If you have git cloned the repo you can do this in a single step without needing to use python interactively by just going to the folder containing the Python modules and running the cpu_health.py module using the "auto" option when running the module:

      .. code-block:: shell

         python cpu_health.py auto

   b. Execute the main() function of cpu_health.py using input parameters to override the configuration file. For example:

      In Python, first import the cpu_health module:

      .. code-block:: python

         import cpu_health_checks.cpu_health as cpu_health

      And then call the main function overriding the desired parameters. Remember to make sure that default values for "config_file" and "logs_folder" are appropriate given the folder you are running the module, or otherwise define them explicitly as input parameters of the main() function at call time. For example:

      .. code-block:: python

         result = cpu_health.main(logs_folder='logs/linux/', latency_url='www.example.com')

      When doing this, change "logs_folder" and "latency_url" for the actual input parameters you want to override form the configuration file.
      Here "result" will then be a dictionary with the keys having the names of the checks performed and the values will be the results of each test.

      If you have git cloned the repo you can do the same running cpu_health.py in python interactive mode and then typing "main(logs_folder='logs/linux/', latency_url='www.example.com')" in the python interpreter.


Both methods generate logs in the specified logs folder, providing detailed information about the health check results.

Modules Role
--------------

Each component of the CPU Health Checks package has a specific role:

- `CPUCheck`: This class encapsulates the CPU health checks and provides an interface to configure and execute the checks. It utilizes the supporting functions in the `utilities` module.

- `utilities`: This module contains functions that handle various tasks related to CPU health checks. These functions are called by the `CPUCheck` class to perform specific checks or retrieve information.

- `test_checks`: This module tests the behavior of the product. Some checks will return False, indicating that the check didn't pass, which doesn't necessarily mean there is an error in the code; it is just the expected output of the check. However, `test_checks` checks if the behavior of the product is correct by running multiple unittests where the expected result is known a priori given the input parameters. For example, we test if `CPUCheckObj.check_enough_disk_space()` returns False when the `min_percent_disk` attribute of the `CPUCheckObj` object is 100, because we assume that at least some part of the disk is used. Some of these tests should return True, some should return False, and some should raise exceptions. If everything goes as expected, the general test prints "OK" at the end; otherwise, it indicates which tests failed.

