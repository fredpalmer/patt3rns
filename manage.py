#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patt3rns.settings")
    # Add the lib/ directory to the system path
    sys.path.append("lib")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
