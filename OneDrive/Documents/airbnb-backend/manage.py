#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbnb.settings')
    try:
        # If a virtualenv was created with virtualenv (provides activate_this.py), try to activate it.
        venv_activate = Path(__file__).resolve().parent / \
            'venv' / 'Scripts' / 'activate_this.py'
        if venv_activate.exists():
            with open(venv_activate, 'r') as f:
                exec(compile(f.read(), str(venv_activate), 'exec'),
                     {'__file__': str(venv_activate)})

        # type: ignore[reportMissingModuleSource]
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
