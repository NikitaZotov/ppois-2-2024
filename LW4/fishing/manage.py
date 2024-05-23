#!/usr/bin/env python
import os
import sys
import threading
from main.console_interface import console_interface


def start_console_interface():
    print("Starting console interface")
    threading.Thread(target=console_interface, daemon=True).start()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishing.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    start_console_interface()
    execute_from_command_line(sys.argv)
