import itertools

__version__ = '0.5.1'

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
        'KRW_CODE': '/code',
        'SPHINX_VERSION': '6.1.3',
        'SPHINX_AUTOBUILD_VERSION': '2021.3.14',
        'SPHINX_RTD_THEME_VERSION': '1.2.0rc3',
        'SPHINX_BREATHE_VERSION' : 'master',
        'SPHINX_AUTOBUILD_HOST': '0.0.0.0',
        'SPHINX_AUTOBUILD_PORT': 8000,
        'SPHINX_AUTOBUILD_FLAGS': '',
        'SPHINX_BUILD_FLAGS': '',
        'SPHINX_SOURCE_DIR': 'docs/sphinx',
        'SPHINX_BUILD_DIR': 'docs/build/html'
    }
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


def context_tags(py, os):
    return [context_tag(py, os)] + tag_aliases(py, os)

def tag_aliases(py, os):
    aliases = []
    if (py, os) == matrix[-1]:
        aliases.append('latest')
    return aliases

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


# each tuple in matrix is:
#
# ( python-version, os )
#
matrix = [
    ('3.8', 'alpine'),
    ('3.9', 'alpine'),
    ('3.10', 'alpine'),
    ('3.11', 'alpine'),
]

contexts = [context(py, os) for (py, os) in matrix]
