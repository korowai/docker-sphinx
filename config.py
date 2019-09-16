import itertools

__version__ = '0.2.1'

def xrepr(arg):
    if isinstance(arg, str):
        return "'%s'" % arg
    else:
        return repr(arg)

def generated_warning(py, os):
    return """\
#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################
"""

def sphinx_params(py, os):
    """Configuration parameters for sphinx with their default values"""

    params = {
        'SPHINX_UID': 1000,
        'SPHINX_GID': 1000,
        'SPHINX_VERSION': '2.2.0',
        'SPHINX_AUTOBUILD_VERSION': '0.7.1',
        'SPHINX_RTD_THEME_VERSION': '0.4.3',
        'SPHINX_BREATHE_VERSION' : '4.13.1',
        'SPHINX_AUTOBUILD_HOST': '0.0.0.0',
        'SPHINX_AUTOBUILD_PORT': 8000,
        'SPHINX_AUTOBUILD_FLAGS': '',
        'SPHINX_BUILD_FLAGS': '',
        'SPHINX_SOURCE_DIR': 'docs/sphinx',
        'SPHINX_BUILD_DIR': 'docs/build/html'
    }

    py_major = py.split('.')[0]
    if py_major == '2':
        params['SPHINX_VERSION'] = '1.8.5'
        params['SPHINX_RTD_THEME_VERSION'] = '0.4.2'
        params['SPHINX_BREATHE_VERSION'] = '4.13.0'

    return params


def sphinx_env_defaults_str(py, os):
    items = sphinx_params(py, os).items()
    return '\n'.join(("DEFAULT_%s=%s" % (k, xrepr(v)) for k, v in items))


def sphinx_env_settings_str(py, os):
    params = list(sphinx_params(py, os))
    return '\n'.join(('%s=${%s-$DEFAULT_%s}' % (k, k, k) for k in params))


def docker_sphinx_args_str(py, os):
    items = sphinx_params(py, os).items()
    return '\n'.join(('ARG %s=%s' % (k, xrepr(v)) for k, v in items))


def docker_sphinx_env_str(py, os):
    params = list(sphinx_params(py, os))
    return 'ENV ' + ' \\\n    '.join(('%s=$%s' % (k, k) for k in params))


def context_id(py, os, sep):
    return sep.join((py, os))


def context_dir(py, os, sep='/'):
    return context_id(py, os, sep)


def context_tag(py, os, sep='-'):
    return context_id(py, os, sep)


def context_files(py, os):
    return {'Dockerfile.in': 'Dockerfile',
            'bin/autobuild.in': 'bin/autobuild',
            'bin/build.in': 'bin/build',
            'bin/sphinx-defaults.in': 'bin/sphinx-defaults',
            'bin/sphinx-entrypoint.in': 'bin/sphinx-entrypoint',
            'bin/sphinx-env.in': 'bin/sphinx-env',
            'hooks/build.in': 'hooks/build'}


def context_subst(py, os):
    return dict({'GENERATED_WARNING': generated_warning(py, os),
                 'SPHINX_ENV_DEFAULTS': sphinx_env_defaults_str(py, os),
                 'SPHINX_ENV_SETTINGS': sphinx_env_settings_str(py, os),
                 'DOCKER_FROM_TAG': context_tag(py, os),
                 'DOCKER_SPHINX_ARGS': docker_sphinx_args_str(py, os),
                 'DOCKER_SPHINX_ENV': docker_sphinx_env_str(py, os),
                 'VERSION': __version__}, **sphinx_params(py, os))


def context(py, os):
    return {'dir': context_dir(py, os),
            'files': context_files(py, os),
            'subst': context_subst(py, os)}


pys = ['2.7', '3.5', '3.6', '3.7']
oses = ['alpine']
contexts = [context(py, os) for (py, os) in itertools.product(pys, oses)]
del pys
del oses
