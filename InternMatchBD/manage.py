#!/usr/bin/env python

import os
import sys

def main():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "apps")))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
