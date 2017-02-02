- Python {{ python.version }}

  [{{ python_version_params.installer_url }}]({{ python_version_params.installer_url }})

  When installing Python:

  - Choose 'Customize Installation'
  - On 'Optional Features':

    Check 'pip' and 'for all users (requires elevation)'.

    Uncheck 'Documentation', 'tcl/tk and IDLE', 'Python test suite', 'py launcher'.

  - On 'Advanced Options':

    Uncheck all options.

    Set the installation path to `{{ python_version_params.install_path }}`.
