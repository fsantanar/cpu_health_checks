![Alt Text](docs/sphinx/_static/CPU_Health_Cheks.jpg)

# CPU Health Checks

CPU Health Checks is a comprehensive software package that allows you to perform various health checks on your CPU across different platforms (Linux, MacOS, Windows). This package provides a set of functionalities to monitor critical aspects of CPU health, including pending reboots, disk space availability, idle CPU usage, network connection status, download speed, latency, and battery charge. By monitoring these factors, you can ensure the optimal performance and stability of your CPU.

## Installation

To install CPU Health Checks, you need to clone the CPU Health Checks repository from GitHub and pip install from there. This allows you to clearly see the components of the package and if you like edit them as you want. To clone the repository, use the following command:

```shell
git clone https://github.com/fsantanar/cpu_health_checks.git
```
Once you have cloned the repository, navigate to the cpu-health-checks directory.

```shell
cd cpu_health_checks
```

Then install the cloned repo with pip doing 

```shell
pip install .
```

Note: If you want to install in developer mode and modify the modules locally without needing to pip install each time add the "-e" option after "pip install".

Finally, go to the folder with the python modules and test the package running the main() function in the cpu_health module from the console using the "auto" option

```shell
cd src/cpu_health_checks
python cpu_health.py auto
```

Which should perform the CPU health checks on your computer.

Once you have installed the cpu_health_checks package you would be able to import it from any folder using statements like `import cpu_health_checks.cpu_health as cpu_health`, or `import cpu_health_checks.utilities as utilities`, and then you can run the functions in these modules for example doing cpu_health.main(). Alternatively, you can run cpu_health.py from the command line using interactive mode (either with ipython or python -i) and then in the python interpreter use the module functions, for example typing main(). 

Even though you can run these modules from any folder, when running from a folder different than the modules location you have to make sure that the "config_file" parameter in the CPUCheck class constructor (by default '../../config/configuration.yml') points to the configuration file relative to the folder where the module is being run, if the default value is not correct use "config_file" as input parameter when calling CPUCheck() constructor (e.g. CPUCheck(config_file='config/configuration.yml') if you are running from package root folder) or the main() function to define the correct value. Also make sure that the "logs_folder" parameter points to the logs folder relative to the folder where the module is being run. By default this parameter is set to '../../logs/' in the configuration.yml file, but if you need to change it, edit the value in the configuration file, or use "logs_folder" as input parameter when calling the CPUCheck() constructor or the main() function to define the correct value (e.g. CPUCheck(logs_folder='cpu_health_checks/logs/') if you are running from parent folder of the package root).

## Updating

If you want to update the package to a newer version you need to go to the root folder of the package, checkout to your local main branch, then pull the remote main branch, and install again with pip install. Below are the specific commands

```shell
cd cpu_health_checks
git checkout main
git pull origin main
pip install .
```

## Usage
The CPU Health Checks package provides a flexible and easy-to-use interface for monitoring your CPU health. Here's an overview of how to use the package and what results you can expect.

### Configuration
CPU Health Checks uses a YAML configuration file (configuration.yml) to specify various input parameters. By default, the configuration file is located in the config directory and uses the default main key. You can customize the configuration file by modifying the parameters according to your requirements.

You can also define multiple main keys in the configuration file to have different sets of parameters for specific use cases. To use a specific main key, you can specify it when calling the CPUCheck() constructor or the main() wrapper function using the "config_mode" parameter.

### Running CPU Health Checks
The main ways to run the CPU health checks are the following:

1. Running individual checks: You can create an instance of the CPUCheck class and call specific methods to perform individual CPU health checks. For example:

   ```python
   import cpu_health_checks.cpu_health as cpu_health

   # Create a CPUCheck object
   checkobj = cpu_health.CPUCheck()

   # Perform specific health checks
   res1 = checkobj.check_enough_disk_space()
   res2 = checkobj.check_enough_idle_usage()
   res3 = checkobj.check_network_connection()
   # ... add more checks as needed
   # Retrieve the results and take actions based on the returned values
   ```

   Each check function returns True if the check passed and False otherwise.

   You can also do this by running the cpu_health.py module from the terminal using python interactive mode and then in the python interpreter create the object doing for example checkobj = CPUCheck().

2. Running all checks at once: You can run all the CPU health checks at once using the main() wrapper function. There are two ways to do this:

      a. Execute the main() function of cpu_health.py using the default parameters defined in the .yml configuration file, and the default values for "config_file", and "config_mode" defined in the CPUCheck() constructor. For example:

      In python first import the cpu_health module
      ```python
      import cpu_health_checks.cpu_health as cpu_health
      ```

      And then run the main() function with the default input parameters not defining any parameter explicitly at call time.

      ```python
      main()
      ```

      You can also do this in a single step without needing to use python interactively by just going to the folder containing the Python modules and running the cpu_health.py module using the "auto" option when running the module:

      ```shell
      python cpu_health.py auto
      ```

      b. Execute the main() function of cpu_health.py using input parameters to override the configuration file. For example:

      In python first import the cpu_health module
      ```python
      import cpu_health_checks.cpu_health as cpu_health
      ```

      And then call the main function overriding the desired parameters. Remember to make sure that default values for "config_file" and "logs_folder" are appropriate given the folder you are running the module, or otherwise define them explicitly as input parameters of the main() function at call time. For example:

      ```python
      result = cpu_health.main(logs_folder='logs/linux/', latency_url='www.example.com')
      ```

      When doing this, change "logs_folder" and "latency_url" for the actual input parameters you want to override form the configuration file.
      Here "result" will then be a dictionary with the keys having the names of the checks performed and the values will be the results of each test.

      You can also do the same running cpu_health.py in python interactive mode and then typing "main(logs_folder='logs/linux/', latency_url='www.example.com')" in the python interpreter.


Both methods generate logs in the specified logs folder and print messages on screen with the results of the checks, providing detailed information about the cpu health check results.

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

## Coding Standards

We take pride in following industry best practices and maintaining high coding standards. Here are some key aspects that showcase the robustness and reliability of our package:

### 1. Code Modularity
Our package is designed with a modular approach, allowing each functionality to be encapsulated specific purpose functions/method within separate modules. This enhances maintainability and code readability, making it easy for developers to understand and contribute to the project.

### 2. Exception Handling & Raising
We adhere to proper exception handling throughout the codebase. This ensures graceful error handling, providing informative error messages for debugging and troubleshooting.

### 3. Unit Testing
The package includes comprehensive unit tests that validate the correctness of each module's functionality. Continuous integration with GitHub Actions ensures that tests are automatically run on Linux, macOS, and Windows platforms, ensuring cross-platform compatibility.

### 4. Platform Compatibility
Our package is designed to work seamlessly on all major platforms, including Linux, macOS, and Windows. This allows users to run our code on their preferred operating system without any hassle.

### 5. Logging of Results
We maintain detailed logs of our package's execution, allowing users to track and review the results of CPU health checks effortlessly. The logging mechanism is configurable, providing flexibility in managing log levels and output destinations.

### 6. Easy and Flexible to Use
We strive to offer a user-friendly experience for our package. Users can execute CPU health checks from the terminal, use default input parameters, pass parameters during function calls, or configure settings through a user-friendly config file.

### 7. Continuous Integration with GitHub Actions
Our development workflow includes a GitHub Actions workflow that automatically checks linting and runs unit tests on all three major platforms. This ensures that every pull request is thoroughly validated before merging into the main branch.

### 8. Protected Branch Rule
To maintain code integrity and quality, we enforce a branch protection rule that requires pull requests and owner authorization to merge changes into the main branch. This guarantees that only well-reviewed and approved code makes it to the main branch.

### 9. Comprehensive Documentation
We believe that good documentation is essential for a successful project. Our code is well-documented with clear and concise docstrings, providing insights into each module's functionality. We generate documentation locally using Sphinx, and it's also available online through Read the Docs, making it easy for users and developers to understand and utilize our package effectively.

### 10. Easy Installation with Pip
We ensure a smooth installation process through the setup.py file, allowing users to install our package effortlessly using Pip.

We are committed to maintaining these coding standards and continuously improving our package to provide the best possible experience for our users and contributors.

