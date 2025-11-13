#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script personalizado para ejecutar migraciones evitando problemas de encoding
"""
import os
import sys

# Forzar UTF-8 antes de cualquier import
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PGCLIENTENCODING'] = 'UTF8'

# Limpiar cualquier variable de entorno de PostgreSQL que pueda causar problemas
for key in list(os.environ.keys()):
    if key.startswith('PG') and key not in ['PGCLIENTENCODING']:
        del os.environ[key]

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Ejecutar el comando que se pase como argumento
    if len(sys.argv) < 2:
        print("Uso: python migrate.py [comando]")
        print("Ejemplos:")
        print("  python migrate.py makemigrations")
        print("  python migrate.py migrate")
        print("  python migrate.py createsuperuser")
        sys.exit(1)
    
    # Construir el comando completo
    command = ['manage.py'] + sys.argv[1:]
    
    print(f"Ejecutando: {' '.join(command)}")
    execute_from_command_line(command)
