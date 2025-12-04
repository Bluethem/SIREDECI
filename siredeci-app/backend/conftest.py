import pytest
from django.contrib.auth import get_user_model
from apps.usuarios.models import Rol, UsuarioRol  # importa estos modelos

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_use_migrations():
    """Desactiva las migraciones en los tests: crea las tablas desde los modelos."""
    return False


@pytest.fixture
def usuario_interno(db):
    """Crea un usuario interno simple para usar en los tests con rol interno."""
    user = User.objects.create_user(
        nombre_usuario="interno_test",
        email="interno@example.com",
        password="pass1234",
        estado_cuenta="Activo",
    )

    # Crear un rol NO ciudadano (distinto de ROL-005)
    rol = Rol.objects.create(
        codigo_rol="ROL-001",
        nombre="Administrador de pruebas",
        descripcion="Rol interno para tests",
        nivel=1,
        es_sistema=True,
        esta_activo=True,
    )

    # Asignar rol al usuario
    UsuarioRol.objects.create(
        id_usuario=user,
        id_rol=rol,
        es_activo=True,
    )

    return user