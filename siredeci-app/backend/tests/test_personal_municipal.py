import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.categorias.models import AreaResponsable, Categoria
from apps.denuncias.models import Denuncia, Ubicacion
from apps.personal.models import PersonalMunicipal, Asignacion

User = get_user_model()


@pytest.mark.django_db
def test_mis_denuncias_personal_devuelve_denuncias_asignadas(usuario_interno):
    """El endpoint /api/municipal/mis-denuncias/ devuelve las denuncias activas
    asignadas al personal municipal vinculado al usuario interno.
    """
    # Crear área y categoría
    area = AreaResponsable.objects.create(
        nombre="Área de Pruebas",
        descripcion="Área para tests de personal municipal",
        email="area@test.com",
        telefono="999999999",
        capacidad_maxima=10,
        esta_activo=True,
    )

    categoria = Categoria.objects.create(
        nombre="Ruido zona centro",
        descripcion="Pruebas de categoría",
        esta_activo=True,
        id_area_responsable=area,
    )

    # Crear personal municipal asociado al usuario_interno
    personal = PersonalMunicipal.objects.create(
        dni="11112222",
        nombre="Ana",
        apellido="Pruebas",
        email="ana.pruebas@example.com",
        cargo="Operador",
        fecha_ingreso=timezone.now().date(),
        estado_laboral="Activo",
        id_area_responsable=area,
        id_usuario=usuario_interno,
    )

    # Crear una denuncia de esa área
    ubicacion = Ubicacion.objects.create(
        latitud=-12.05,
        longitud=-77.04,
        direccion="Calle Test 123",
        referencia="Frente a la plaza",
        distrito="Lima",
        codigo_postal="15001",
    )

    denuncia = Denuncia.objects.create(
        titulo="Bulla en la plaza",
        descripcion="Descripción de prueba",
        id_categoria=categoria,
        id_ubicacion=ubicacion,
        es_anonima=True,
        prioridad="Media",
        numero_seguimiento="SEG-TEST-001",
        requiere_validacion=False,
    )

    # Crear una asignación activa de esa denuncia al personal
    Asignacion.objects.create(
        motivo_asignacion="Test asignación",
        id_denuncia=denuncia,
        id_personal_asignado=personal,
        id_personal_asignador=personal,
    )

    client = APIClient()
    client.force_authenticate(user=usuario_interno)

    response = client.get("/api/municipal/mis-denuncias/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert any(d["codigo_denuncia"] == denuncia.codigo_denuncia for d in data)


@pytest.mark.django_db
def test_pendientes_asignar_area_devuelve_denuncias_sin_asignacion(usuario_interno):
    """El endpoint /api/municipal/pendientes-asignar/ lista las denuncias de las
    categorías del área del personal que no tienen asignación activa.
    """
    area = AreaResponsable.objects.create(
        nombre="Área Pendientes",
        descripcion="Área para tests de pendientes",
        email="area2@test.com",
        telefono="888888888",
        capacidad_maxima=5,
        esta_activo=True,
    )

    categoria = Categoria.objects.create(
        nombre="Basura",
        descripcion="Basura en la vía pública",
        esta_activo=True,
        id_area_responsable=area,
    )

    personal = PersonalMunicipal.objects.create(
        dni="33334444",
        nombre="Luis",
        apellido="Pendientes",
        email="luis.pendientes@example.com",
        cargo="Jefe de área",
        fecha_ingreso=timezone.now().date(),
        estado_laboral="Activo",
        id_area_responsable=area,
        id_usuario=usuario_interno,
    )

    ubicacion = Ubicacion.objects.create(
        latitud=-12.06,
        longitud=-77.03,
        direccion="Av. Principal 789",
        referencia="Cerca al puente",
        distrito="Lima",
        codigo_postal="15002",
    )

    denuncia = Denuncia.objects.create(
        titulo="Basura acumulada",
        descripcion="Hay basura desde hace varios días",
        id_categoria=categoria,
        id_ubicacion=ubicacion,
        es_anonima=True,
        prioridad="Alta",
        numero_seguimiento="SEG-TEST-002",
        requiere_validacion=False,
    )

    client = APIClient()
    client.force_authenticate(user=usuario_interno)

    response = client.get("/api/municipal/pendientes-asignar/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert any(d["codigo_denuncia"] == denuncia.codigo_denuncia for d in data)


@pytest.mark.django_db
def test_mis_denuncias_personal_403_sin_personal_activo(usuario_interno):
    """Si el usuario interno no tiene registro de PersonalMunicipal activo,
    el endpoint devuelve 403 con mensaje adecuado.
    """
    client = APIClient()
    client.force_authenticate(user=usuario_interno)

    response = client.get("/api/municipal/mis-denuncias/")

    assert response.status_code == 403
    data = response.json()
    assert data.get("error") == "Personal no válido"
