## Creating a Virtual Environment and Installing Dependencies

All Python work should be done within a virtual environment, to avoid dependency conflicts.
Node.js and Ruby have their own dependency management (i.e., npm shrinkwrap and bundler).
Our Python automation scripts will employ those tools, but we first need to configure Python.

Create the virtual environment. From the working directory of our project (e.g., `{{ readme.working_directory }}`):

    {{ python_version_params.install_path }}\python.exe -m venv {{ python_version_params.virtual_environment_name }}

This will create a directory for the virtual environment (e.g., `{{ readme.working_directory }}\{{ python_version_params.virtual_environment_name }}\`).

Next activate that virtual environment and install our Python dependencies:

    {{ python_version_params.virtual_environment_name }}\Scripts\activate.bat
    pip install -r {{ python_version_params.requirements_name }}

Next use Python's invoke automation to get the rest of our dependencies:

    invoke update_dependencies
