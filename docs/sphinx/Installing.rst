Installing
==========

To install the CPU Health Checks package, follow these steps:

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

3. Install the package dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

4. Add the folder containing the package to your PYTHONPATH environmental variable in your shell 
   configuration file.

   Depending on your shell (which you can check with "echo $SHELL"), you can use:

   - For Bash:

     .. code-block:: bash

        export PYTHONPATH="/path/to/folder:$PYTHONPATH"

   - For Fish:

     .. code-block:: fish

        set -gx PYTHONPATH "/path/to/folder" $PYTHONPATH

   - For PowerShell:

     .. code-block:: powershell

        $env:PYTHONPATH = "/path/to/folder;$env:PYTHONPATH"

   Replace ``/path/to/folder`` with the folder where the "cpu_health_checks" package is located
   (i.e., its parent folder).

   This will install all the required dependencies for the CPU Health Checks package. Following these
   4 simple steps, the package will now be ready for use.
