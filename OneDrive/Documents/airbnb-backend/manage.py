#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from django.core.management import execute_from_command_line


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

        # Run conversion and loading script using subprocess
        import subprocess
        try:
            subprocess.run(
                'docker-compose build web',
                check=True, shell=True, text=True)
            subprocess.run(
                'docker-compose up -d web',
                check=True, shell=True, text=True)
            result = subprocess.run(
                'docker-compose exec web bash convert_and_load.sh input.sql postgres_user postgres_db postgres_password',
                check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print('Error running conversion script:', e.stderr)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

