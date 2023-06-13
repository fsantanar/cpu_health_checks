Configuration File
==================

The CPU Health Checks package uses a YAML configuration file to specify various input parameters.
By default, the configuration file is searched at `config/configuration.yml` and the `default` main
Key in it is used.

You can change the default config file and mode when calling the main() wrapper function or the 
CPUCheck constructor in the cpu_health.py module by specifying the configuration file relative path 
with the `config_file` parameter, and the main key to use with the `config_mode` parameter. 

For example if you want to run all the tests based on the content of the "my_laptop" main key, from 
the configuration file "myconfig.yml" at folder "configs/mac/" you can type: 
main(config_file='configs/mac/myconfig.yml', config_mode='my_laptop').

Then, by default the parameters from the configuration file/mode set will be used as input, but the 
user can override any parameter defined in the configuration by specifying it when instantiating the `CPUCheck` object or when using the main() wrapper.

Example Configuration File
--------------------------

The following is an example of a configuration file (`configuration.yml`) used by the CPU Health Checks package, and is the one provided as starting point by the package:

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


You can modify any of these parameters according to your requirements.
The commented line on top of each group of parameters indicates the function in which the parameters
are used.

You can also define multiple main keys in the configuration file (other than `default`) and quickly
switch between which one is used by setting the `config_mode` parameter when calling the CPUCheck()
constructor or the main() wrapper function.

