import os
import sys
import yaml
import urlparse

from fabric.api import cd, sudo, env
from fabric.context_managers import shell_env, prefix
from fabric.contrib.files import exists

DEPLOY_FILE = os.environ.get('DEPLOY_FILE', '.deploy.yml')
DEPLOY_USER = os.environ.get('DEPLOY_USER', 'jmbo')

recipe = yaml.load(open(DEPLOY_FILE, 'r'))

# vary shallow validations
expected_keys = ['repository', 'hosts']

if not set(expected_keys).issubset(set(recipe.keys())):
    raise Exception('Invalid config, check the %s' % (DEPLOY_FILE,))
    sys.exit(1)

# which hosts to connect to
env.hosts = recipe['hosts']

# which repository to clone
repository_url = urlparse.urlparse(recipe['repository'])
repository_name = repository_url.path.split('/')[-1]
folder_name = repository_name.rsplit('.', 1)[0]

# path to where apps are hosted
env.path = os.path.join('/', 'var', 'praekelt', folder_name)

# which environment variables to set when stuff is run
environment = recipe.get('env', {})

# which processes to have supervisord start
processes = recipe.get('processes', {})

# actions
post_clone = recipe.get('post_clone', [])
post_pull = recipe.get('post_pull', [])


def clone():
    if not exists(env.path):
        sudo('git clone %s %s' % (repository_url.geturl(), env.path),
             user=DEPLOY_USER)
    with cd(env.path):
        sudo('virtualenv ve', user=DEPLOY_USER)
        with prefix('. ve/bin/activate'):
            for command in post_clone:
                with shell_env(**environment):
                    sudo(command, user=DEPLOY_USER)


def pull():
    with cd(env.path):
        with prefix('. ve/bin/activate'):
            for command in post_pull:
                with shell_env(**environment):
                    sudo(command, user=DEPLOY_USER)
