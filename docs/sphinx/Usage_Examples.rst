Usage Examples
==============

This section provides examples on how to use the CPU Health Checks package effectively.

Example 1: Run the `main()` Wrapper Function Automatically from Command line
---------------------------------------------------------------------------------------------------------

To run the CPU health checks using the `main()` function in the `cpu_health.py` module, you can execute the following command:

.. code-block:: bash

   python cpu_health.py auto

This will use the configuration parameters defined in the configuration file (`config/configuration.yml`) to create a `CPUCheck` object and perform all the health checks.

Example 2: Using the `main()` Wrapper Function using non-default parameters
--------------------------------------------------------------------------------------------------------

You can run the CPU health checks using the `main()` function using a configuration file and mode
different than the default defined in the CPUCheck constructor
(`default` key in `config/configuration.yml` file). And for any parameter you can also use values 
different than the ones defined in your custom configuration file.

For example if you have your custom configuration file called `custom.yml` in folder `inputs/` with
respect to the folder where you are running the code you need to use config_file=`inputs/custom.yml`.
Now if you want to use the values within the main key `laptop_check` in that file you need to use
the config_mode=`laptop_check` value. Finally if there are some values there that you want to 
override when running a specific check like min_gb=20, and min_percent_battery=50 you can define
those at at call time, as it is shown in the example.

.. code-block:: bash

   python cpu_health.py

.. code-block:: python

   main(config_file='inputs/custom.yml', config_mode='laptop_check', min_gb=20, min_percent_battery=50)

This will use the configuration parameters defined in the configuration file (`config/configuration.yml`) to create a `CPUCheck` object and perform all the health checks.


Example 3: Using the `CPUCheck()` Constructor
-------------------------------------------------------------------------

To run individual CPU health checks with specific input parameters, you can create an instance of the `CPUCheck` class and call the relevant methods. Here's an example:

.. code-block:: python

   import cpu_health_checks.cpu_health as cpu_health
   
   config_file_path = "path/to/configuration.yml"
   logs_folder_path = "path/to/logs"
   
   # Create a CPUCheck object called checkobj
   checkobj = cpu_health.CPUCheck(config_file=config_file_path, logs_folder=logs_folder_path)
   
   # Perform specific health checks
   checkobj.check_enough_disk_space()
   checkobj.check_enough_idle_usage()
   checkobj .check_network_connection()
   # ... add more checks as needed
   
   # Retrieve the results and take actions based on the returned values

There you need to replace "path/to/configuration.yml" for the path and filename of the configuration file, and "path/to/logs"
with the folder to use to store the general and download speed logs. Both folders have to be specified with respect to the
folder where cpu_health is being run.


Example 4: Using the `test_checks.py` Module
------------------------------------------------------------------------

The `test_checks.py` module provides unit tests for the `cpu_health.py` module. You can use it to verify that the code behaves as expected. Here's an example of using the `test_checks.py` module:

.. code-block:: bash

   python -m unittest test_checks.py

This command will execute the unit tests defined in the `test_checks.py` module and report the test results.

