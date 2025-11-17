"""
Script para migrar de psycopg2 a psycopg3 (compatible con Python 3.13)
"""
import subprocess
import sys

print("=" * 70)
print("MIGRACIÓN A PSYCOPG3 PARA PYTHON 3.13")
print("=" * 70)

print(f"\n📍 Versión de Python detectada: {sys.version}")

if sys.version_info < (3, 13):
    print("\n⚠️  Tu versión de Python es menor a 3.13")
    print("   No necesitas psycopg3, psycopg2 debería funcionar.")
    print("\n   Si tienes problemas, ejecuta:")
    print("   pip install psycopg2-binary==2.9.9 --force-reinstall")
    sys.exit(0)

print("\n✅ Python 3.13 detectado - Se requiere psycopg3")

# Paso 1: Desinstalar psycopg2
print("\n📦 Paso 1: Desinstalando psycopg2...")
try:
    subprocess.run([
        sys.executable, "-m", "pip", "uninstall", "-y",
        "psycopg2", "psycopg2-binary"
    ], check=False)
    print("   ✓ psycopg2 desinstalado")
except Exception as e:
    print(f"   ℹ️  {e}")

# Paso 2: Instalar psycopg3
print("\n📦 Paso 2: Instalando psycopg3...")
try:
    result = subprocess.run([
        sys.executable, "-m", "pip", "install",
        "psycopg[binary]>=3.1.18"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("   ✓ psycopg3 instalado correctamente")
    else:
        print(f"   ✗ Error: {result.stderr}")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Error al instalar psycopg3: {e}")
    sys.exit(1)

# Paso 3: Verificar instalación
print("\n🔍 Paso 3: Verificando instalación...")
try:
    import psycopg
    print(f"   ✓ psycopg3 versión: {psycopg.__version__}")
except ImportError:
    print("   ✗ Error: No se pudo importar psycopg3")
    sys.exit(1)

# Paso 4: Probar conexión
print("\n🔌 Paso 4: Probando conexión a PostgreSQL...")
try:
    from decouple import config
    
    conn_params = {
        'dbname': config('DB_NAME'),
        'user': config('DB_USER'),
        'password': config('DB_PASSWORD'),
        'host': config('DB_HOST'),
        'port': config('DB_PORT', default='5432'),
    }
    
    print("   Conectando con:")
    for key, value in conn_params.items():
        if key == 'password':
            print(f"   - {key}: {'*' * len(value)}")
        else:
            print(f"   - {key}: {value}")
    
    # Construir DSN
    dsn = f"dbname={conn_params['dbname']} user={conn_params['user']} password={conn_params['password']} host={conn_params['host']} port={conn_params['port']}"
    
    conn = psycopg.connect(dsn)
    print("\n   ✓ CONEXIÓN EXITOSA con psycopg3!")
    
    # Probar una query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"   ✓ PostgreSQL versión: {version[:50]}...")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n   ✗ Error en conexión: {e}")
    print("\n   Verifica que PostgreSQL esté corriendo y las credenciales sean correctas")

print("\n" + "=" * 70)
print("MIGRACIÓN COMPLETADA")
print("=" * 70)

print("\n✅ Próximos pasos:")
print("1. Ejecuta: python manage.py check")
print("2. Si todo está OK, ejecuta: python manage.py runserver")
print("\nNOTA: Django usará automáticamente psycopg3 en lugar de psycopg2")
