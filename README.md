![Alt Text](docs/sphinx/_static/CPU_Health_Cheks.jpg)

# CPU Health Checks

CPU Health Checks is a comprehensive software package that allows you to perform various health checks on your CPU across different platforms (Linux, MacOS, Windows). This package provides a set of functionalities to monitor critical aspects of CPU health, including pending reboots, disk space availability, idle CPU usage, network connection status, download speed, latency, and battery charge. By monitoring these factors, you can ensure the optimal performance and stability of your CPU.

## Installation

To install CPU Health Checks, you have two options:

1. Installing from PyPI (Not Available for the Moment but Will be Available Soon): You can install the package using pip by running the following command:

```console
pip install cpu_health_checks
```

2. Installing from Source (Git Clone): Alternatively, you can clone the CPU Health Checks repository from GitHub. This allows you to have access to the source code and modify it as you want. To clone the repository, use the following command:

```shell
git clone https://github.com/fsantanar/cpu_health_checks.git
```
Once you have cloned the repository, navigate to the cpu-health-checks directory.

```shell
cd cpu_health_checks
```

And then install the cloned repo with pip

```shell
pip install .
```

Go to the folder with the python modules and test the package running the main() function in cpu_health module using the "auto" option

```shell
cd src/cpu_health_checks
python cpu_health.py auto
```

Which should perform the CPU health checks on your computer.

Once you have installed the cpu_health_checks package you would be able to import it from any folder using statements like `import cpu_health_checks.cpu_health as cpu_health`, or `import cpu_health_checks.utilities as utilities`. When importing the modules make sure that the "config_file" parameter in the CPUCheck class constructor (by default '../../config/configuration.yml')
Points to the configuration file with respect to the folder where the module is being run, if the default value is not correct use it as input parameter when calling CPUCheck() constructor (e.g. CPUCheck(config_file='config/configuration.yml') or the main() function. Also make sure that the "logs_folder" parameter points to the logs folder with respect to the folder where the module is being run. 
By default this parameter is set to '../../logs/' in the configuration.yml file, but if you need to change it, edit the value in the configuration file, or use it as input parameter when calling the CPUCheck() constructor or the main() function.
If you have git cloned the package you would also be able to run the main module directly by doing "python path/to/cpu_health_module_folder/cpu_health.py" replacing "path/to/cpu_health_module_folder/" with the actual folder containing the cpu_health.py module (which should be in the folder src/cpu_health_checks/ folder within the root folder of the project).

## Usage
The CPU Health Checks package provides a flexible and easy-to-use interface for monitoring your CPU health. Here's an overview of how to use the package and what results you can expect.

### Configuration
CPU Health Checks uses a YAML configuration file (configuration.yml) to specify various input parameters. By default, the configuration file is located in the config directory and uses the default main key. You can customize the configuration file by modifying the parameters according to your requirements.

You can also define multiple main keys in the configuration file to have different sets of parameters for specific use cases. To use a specific main key, you can specify it when calling the CPUCheck() constructor or the main() wrapper function.

### Running CPU Health Checks
There are several ways to run the CPU health checks:

1. Running individual checks: You can create an instance of the CPUCheck class and call specific methods to perform individual CPU health checks. For example:

   ```python
   import cpu_health_checks.cpu_health as cpu_health

   # Create a CPUCheck object
   checkobj = cpu_health.CPUCheck()

   # Perform specific health checks
   checkobj.check_enough_disk_space()
   checkobj.check_enough_idle_usage()
   checkobj.check_network_connection()
   # ... add more checks as needed
   # Retrieve the results and take actions based on the returned values
   ```

   Each check function returns True if the check passed and False otherwise.

2. Running all checks at once: You can run all the CPU health checks at once using the main() wrapper function. There are two ways to do this:

      a. Execute the main() function of cpu_health.py using input parameters to override the configuration file. For example:

      In python first import the cpu_health module
      ```python
      import cpu_health_checks.cpu_health as cpu_health
      ```

      And then call the main function overriding the desired parameters. Remember to make sure that default values for "config_file" and "logs_folder" are appropriate given the folder you are running the module, or otherwise define them explicitly as input parameters of the main() function.

      ```python
      result = cpu_health.main(logs_folder='logs/linux/', latency_url='www.example.com')
      ```

      Changing "logs_folder" and "latency_url" for the actual input parameters you want to override form the configuration file.
      Here "result" will then be a dictionary with the keys having the names of the checks performed and the values will be the results of each test.

      If you have git cloned the repo you can do the same thing going to the src/cpu_health_checks/ folder containing the Python modules, run the cpu_health.py module interactively in python and then use its main() function. For example:

      ```shell
      python -i cpu_health.py auto
      ```

      And then in Python type:
      ```python
      main(logs_folder='logs/linux/', latency_url='www.example.com')
      ```

      b. Execute the main() function of cpu_health.py using the default parameters defined in the .yml configuration file, and the default values for "config_file", and "config_mode" defined in the CPUCheck() constructor. For example:

      In python first import the cpu_health module
      ```python
      import cpu_health_checks.cpu_health as cpu_health
      ```

      And then run the main() function with the default input parameters not defining any parameter explicitly at call time.

      ```python
      main()
      ```

      If you have git cloned the repo you can do this in a single step without needing to use python interactively by just going to the folder containing the Python modules and running the cpu_health.py module using the "auto" option when running the module:

      ```shell
      python cpu_health.py auto
      ```

Both methods generate logs in the specified logs folder, providing detailed information about the health check results.

### Interpreting Results
After running the CPU health checks, you can interpret the results based on the returned values from each check function. If a check passes (returns True), it means that the CPU health is satisfactory for that specific aspect. If a check fails (returns False), it indicates an issue with the CPU health in that particular area.

Based on the results, you can take appropriate actions to resolve any identified issues. For example, if the disk space check fails, you can free up disk space by removing unnecessary files or expanding the storage capacity.

## Contribution
If you would like to contribute to the development of CPU Health Checks, you can follow these steps:

1. Fork the CPU Health Checks repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your changes.
4. Make the necessary changes and additions to the codebase.
5. Test your changes thoroughly.
6. Commit your changes and push them to your forked repository.
7. Submit a pull request on the original CPU Health Checks repository.

Please make sure to follow the coding style and guidelines specified in the repository to ensure consistency and maintainability.

## License
CPU Health Checks is released under the MIT License. See the LICENSE file for more details.

## Read The Docs Documentation

For further documentation please refer to the Read The Docs webpage at [cpu-health-checks.readthedocs.io/](https://cpu-health-checks.readthedocs.io/en/)
