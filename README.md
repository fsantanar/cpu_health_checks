
# CPU Health Checks

CPU Health Checks is a comprehensive software package that allows you to perform various health checks on your CPU across different platforms (Linux, MacOS, Windows). This package provides a set of functionalities to monitor critical aspects of CPU health, including pending reboots, disk space availability, idle CPU usage, network connection status, download speed, latency, and battery charge. By monitoring these factors, you can ensure the optimal performance and stability of your CPU.

## Installation

To install CPU Health Checks, you have two options:

1. Using pip: You can install the package using pip by running the following command:

```console
pip install cpu_health_checks
```

2. Cloning the repository: Alternatively, you can clone the CPU Health Checks repository from GitHub. This allows you to have access to the source code and run the modules directly. To clone the repository, use the following command:

```shell
git clone https://github.com/fsantanar/cpu-health-checks.git
```
Once you have cloned the repository, navigate to the cpu-health-checks directory.

Note: If you choose this option, make sure to add the cpu-health-checks directory to your PYTHONPATH environment variable to be able to run the modules from any folder.

If you have pip installed the cpu_health_checks package you would be able to import it using statements like `import cpu_health_checks.cpu_health as cpu_health`, `import cpu_health_checks.utilities as utilities`, and `import cpu_health_checks.tests.test_checks as test_checks. If you have git cloned the package you would also be able to run the main module directly by doing "python path/to/cpu_health_package/cpu_health.py" replacing "path/to/cpu_health_package/" with the actual package where the package is located.

## Usage
The CPU Health Checks package provides a flexible and easy-to-use interface for monitoring your CPU health. Here's an overview of how to use the package and what results you can expect.

### Configuration
CPU Health Checks uses a YAML configuration file (configuration.yml) to specify various input parameters. By default, the configuration file is located in the config directory and uses the default main key. You can customize the configuration file by modifying the parameters according to your requirements.

You can also define multiple main keys in the configuration file to have different sets of parameters for specific use cases. To use a specific main key, you can specify it when calling the CPUCheck() constructor or the main() wrapper function.

### Running CPU Health Checks
There are several ways to run the CPU health checks:

1 Running individual checks: You can create an instance of the CPUCheck class and call specific methods to perform individual CPU health checks. For example:

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

2 Running all checks at once: You can run all the CPU health checks at once using the main() wrapper function. There are two ways to do this:

a. Run the cpu_health.py module in interactive mode (e.g., with ipython or python -i) and then run main() using the desired input parameters to override the configuration file. For example:

In the shell type
```console
python -i cpu_health.py
```

And then in python type:
```python
main(logs_folder='logs/linux/', latency_url='www.example.com')
```

b. Run the cpu_health.py module from the command line using the auto keyword. This will automatically use the default configuration parameters defined in the configuration file to create a CPUCheck object and perform all the health checks. For example:

```console
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
