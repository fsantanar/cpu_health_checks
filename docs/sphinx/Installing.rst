Installing
==========

To install the CPU Health Checks package you can either use PyPI (Not Available for the Moment but Will be Available Soon) typing

   .. code-block:: bash

      pip install cpu_health_checks

Installing from Source using Git Clone following these steps:

1. Clone the repository using the following command:

   .. code-block:: bash

      git clone https://github.com/fsantanar/cpu_health_checks.git

   This will create a local copy of the repository on your machine.

   Please note that before this, you will need to have git installed on your computer.
   If you don't have it, please follow the `git installation instructions
   <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_. If you are running a Mac
   computer, you can install the Xcode Command Line Tools, which include git, by typing
   "xcode-select --install" in your terminal.

2. Navigate to the repository directory:

   .. code-block:: bash

      cd cpu_health_checks

3. Install the package:

   .. code-block:: bash

      pip install .

4. Go to the folder with the python modules and test the package running the main() function in the cpu_health module using the "auto" option.

   .. code-block:: bash

      cd src/cpu_health_checks
      python cpu_health.pt auto

