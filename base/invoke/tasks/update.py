import invoke
import re
import sys
import yaml


VERBOSE = False


@invoke.task
def verbose():
    global VERBOSE

    VERBOSE = True


def check_result(result, description):
    if result.failed:
        print('========================================')
        print('Failed to {}'.format(description))
        print('')
        print('========================================')
        print('STDOUT:')
        print('========================================')
        print(result.stdout)
        print('========================================')
        print('STDERR:')
        print('========================================')
        print(result.stderr)
        print('========================================')
        raise Exception('Failed to {}'.format(description))


@invoke.task
def update_base():
    invoke.run('git pull https://github.com/fogies/web-jekyll-base.git master', encoding=sys.stdout.encoding)
    invoke.run('git pull https://github.com/fogies/invoke-base.git master', encoding=sys.stdout.encoding)


@invoke.task
def update_dependencies():
    # Parameters to keep everything silent
    params_silent = {
        'encoding': sys.stdout.encoding,
        'hide': 'both' if VERBOSE is False else None,
        'warn': True
    }

    # Parse our compile config
    with open('_base_config.yml') as f:
        compile_config_yaml = yaml.safe_load(f)

    # Python dependencies
    if compile_config_yaml['config']['python']['required']:
        print('Checking Python dependencies')

        # Ensure we have a current version of pip, as needed by pip-tools
        pip_version_desired = compile_config_yaml['config']['python']['pip_version']
        result = invoke.run('pip --disable-pip-version-check show pip', **params_silent)
        check_result(result, 'check pip version')

        pip_version_current = re.search('^Version: ([\d\.]+)', result.stdout, re.MULTILINE).group(1)
        if pip_version_current != pip_version_desired:
            result = invoke.run(
                'python -m pip install --upgrade pip=={}'.format(
                    pip_version_desired
                ),
                **params_silent
            )
            check_result(result, 'update pip version')

        # Ensures we have pip-tools, which will be in our requirements file
        # pip-sync also does not respect options in the requirements file,
        # so installing the entire file ensures pip-sync only needs to delete
        result = invoke.run('pip --disable-pip-version-check install -r requirements3.txt', **params_silent)
        check_result(result, 'install pip requirements')
        # Ensure we have exactly our dependencies
        result = invoke.run('pip-sync requirements3.txt', **params_silent)
        check_result(result, 'sync pip requirements')

    if compile_config_yaml['config']['node']['required']:
        # The npm install command sometimes outputs characters that cause Unicode
        # errors on Windows, so we set the encoding parameter on our commands
        print('Checking Node.js dependencies')
        result = invoke.run('npm install', **params_silent)
        check_result(result, 'install Node.js dependencies')

    if compile_config_yaml['config']['ruby']['required']:
        # Ruby dependencies
        print('Checking Ruby dependencies')

        # Check we have the correct Bundler version
        bundler_version_desired = compile_config_yaml['config']['ruby']['bundler_version']

        result = invoke.run('gem list -i bundler -v {}'.format(bundler_version_desired), **params_silent)
        # expected to fail if the desired version is not installed
        if result.failed:
            result = invoke.run('gem install bundler -v {}'.format(bundler_version_desired), **params_silent)
            check_result(result, 'install bundler')

        # And only the correct Bundler version
        invoke.run('gem uninstall bundler -v "!={}"'.format(bundler_version_desired), **params_silent)
        # expected to fail if no other versions of bundler are installed

        # Check we have our Ruby dependencies
        result = invoke.run('bundle check', **params_silent)
        # expected to fail if we are missing dependencies
        if result.failed:
            result = invoke.run('bundle install', **params_silent)
            check_result(result, 'bundle install')
