#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Forzar UTF-8 para evitar problemas de encoding en Windows
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Fix específico para Python 3.13 con psycopg2
if sys.version_info >= (3, 13):
    import locale
    import warnings
    
    # Suprimir warnings de deprecación
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    
    # Configurar locale antes de que Django/psycopg2 se inicialicen
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, '')
            except:
                pass


def main():
    """Run administrative tasks."""
    # Usar configuración directa por defecto para evitar problemas de encoding
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.direct')
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
