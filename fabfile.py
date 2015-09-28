# coding=utf-8
from __future__ import unicode_literals

import getpass
import os

from fabric import api, colors, context_managers
from fabric.api import env, local
# noinspection PyProtectedMember
from fabric.operations import _prefix_commands, _prefix_env_vars

env.colorize_errors = True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patt3rns.settings")
from django.conf import settings  # noqa

# NOTE: for some reason if the settings module is not used outside of the context of a task
#       the settings module will not be initialized correctly
print colors.green("Initialized Django {}.settings for fabric command use...".format(settings.REPO_NAME))


def _is_running(process_name):
    with api.settings(context_managers.hide("warnings", "running", "stdout", "stderr"), warn_only=True):
        response = api.local("ps aux | \grep {} | \grep -v grep".format(os.path.join(os.environ.get("VIRTUAL_ENV"), "bin", process_name)))
        result = not response.return_code
    return result


def clean():
    """
    Cleans the project workspace of any crud left over from testing, switching branches, etc.
    """
    patterns = [
        "*_log",
        "*.pyc",
        "*.pyo",
        "nohup.out",
        ".noseids",
        ".DS_Store",
        "celerybeat-schedule",
    ]
    with context_managers.lcd(settings.BASE_DIR):
        for pattern in patterns:
            command = "find . -name \"{}\" -type f -exec rm -vf {{}} \;".format(pattern)
            api.local(command)


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


def supervisorctl(config_file="supervisord.conf"):
    """
    Starts supervisord if not running and shows the status of the currently running processes
    :param config_file: Optional configuration file to use rather than the default
    """
    def _create_dir(dir_to_check):
        if not os.path.exists(dir_to_check):
            # Create the directory and make sure the permissions are correct
            print(colors.yellow("Creating required directory => {} for supervisor...".format(dir_to_check)))
            api.local("sudo mkdir {}".format(dir_to_check))
            api.local("sudo chown {user}:wheel {dir_to_check}".format(dir_to_check=dir_to_check, user=getpass.getuser()))

    _create_dir("/var/log/{}".format(settings.REPO_NAME))
    _create_dir("/var/run/{}".format(settings.REPO_NAME))

    with context_managers.lcd(settings.BASE_DIR):
        if not _is_running("supervisord"):
            print(colors.yellow("supervisord was not running... starting supervisord..."))
            api.local("supervisord --configuration {}".format(config_file))

        if _is_running("supervisord"):
            print(colors.green("supervisord appears to be running..."))
            supervisorctl_command = "supervisorctl --configuration {}".format(config_file)
            print(colors.white("To run supervisor commands => {}".format(supervisorctl_command)))
            api.local("{} status".format(supervisorctl_command))
            api.local("{} maintail".format(supervisorctl_command))
        else:
            print(colors.red("supervisord does not appear to be running, please try again."))
