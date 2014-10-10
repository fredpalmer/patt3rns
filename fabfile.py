import os

from fabric import api
from fabric.api import env, local
from fabric import context_managers
from fabric.decorators import task
# noinspection PyProtectedMember
from fabric.operations import _prefix_commands, _prefix_env_vars

PROJECT_DIR = os.path.dirname(__file__)


@task
def clean():
    """
    Cleans the project directory
    """
    with context_managers.lcd(PROJECT_DIR):
        api.local("pwd && find . -name \"*_log\" -type f -exec rm -vf {} \;")
        api.local("pwd && find . -name \"*.pyc\" -type f -exec rm -vf {} \;")
        api.local("pwd && find . -name \"*.pyo\" -type f -exec rm -vf {} \;")
        api.local("pwd && find . -name nohup.out -type f -exec rm -vf {} \;")
        api.local("pwd && find . -name .noseids -type f -exec rm -vf {} \;")
        api.local("pwd && find . -name celerybeat-schedule -type f -exec rm -vf {} \;")
        api.local("pwd && find . -name .DS_Store -type f -exec rm -vf {} \;")


@task
def ssh_agent_run(cmd):
    """
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent. This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), "remote")
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )
