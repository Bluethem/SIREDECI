import os
import shutil
from pathlib import Path

# Limpiar archivos __pycache__ y .pyc
count = 0
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_dir = os.path.join(root, '__pycache__')
        shutil.rmtree(cache_dir)
        count += 1
        print(f"✓ Eliminado: {cache_dir}")
    
    for file in files:
        if file.endswith('.pyc'):
            pyc_file = os.path.join(root, file)
            os.remove(pyc_file)
            print(f"✓ Eliminado: {pyc_file}")

print(f"\n✓ Limpieza completa. {count} directorios __pycache__ eliminados.")
