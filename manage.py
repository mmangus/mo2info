#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import json
import os
import subprocess
import sys


def main():
    """Run administrative tasks."""
    eb_env = json.loads(
        subprocess.run(
            "/opt/elasticbeanstalk/bin/get-config environment"
        ).stdout
    )
    for key, value in eb_env.items():
        os.environ.setdefault(key, value)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
