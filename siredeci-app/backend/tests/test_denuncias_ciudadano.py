import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.ciudadanos.models import Ciudadano
from apps.categorias.models import Categoria, AreaResponsable


@pytest.mark.django_db
def test_ciudadano_puede_registrar_denuncia_no_anonima():
    """Un ciudadano activo puede registrar una denuncia no anónima con los datos mínimos."""
    # Preparar datos base: ciudadano y categoría
    ciudadano = Ciudadano.objects.create(
        dni="12345678",
        nombre="Juan",
        apellido="Pérez",
        email="juan@example.com",
        direccion="Calle Falsa 123",
        fecha_emision_dni=timezone.now().date(),
        estado_cuenta="Activo",
    )

    area = AreaResponsable.objects.create(
        nombre="Gestión Ambiental",
        descripcion="Área responsable de temas ambientales",
        esta_activo=True,
    )

    categoria = Categoria.objects.create(
        nombre="Ruido excesivo",
        descripcion="Denuncias por ruido",
        esta_activo=True,
        id_area_responsable=area,
    )

    client = APIClient()

    payload = {
        "titulo": "Ruido en la madrugada",
        "descripcion": "Vecinos hacen ruido todos los días a las 3am.",
        "id_categoria": categoria.id_categoria,
        "id_ciudadano": ciudadano.id_ciudadano,
        "es_anonima": False,
        "prioridad": "Media",
        "ubicacion": {
            "latitud": -12.0464,
            "longitud": -77.0428,
            "direccion": "Av. Siempre Viva 742",
            "referencia": "Cerca al parque",
            "distrito": "Lima",
            "codigo_postal": "15001",
        },
        # evidencias_data es opcional, se omite
    }

    response = client.post("/api/denuncias/", payload, format="json")

    assert response.status_code == 201
    data = response.json()

    assert "mensaje" in data
    assert data["mensaje"]
    assert "denuncia" in data
    denuncia = data["denuncia"]

    # El backend debe devolver un número de seguimiento y código de denuncia
    assert denuncia.get("codigo_denuncia")
    assert denuncia.get("numero_seguimiento")
    assert denuncia.get("titulo") == payload["titulo"]


@pytest.mark.django_db
def test_ciudadano_ve_sus_denuncias_en_mis_denuncias():
    """El endpoint /api/denuncias/mis-denuncias/ devuelve las denuncias del ciudadano indicado."""
    ciudadano = Ciudadano.objects.create(
        dni="87654321",
        nombre="María",
        apellido="López",
        email="maria@example.com",
        direccion="Av. Principal 456",
        fecha_emision_dni=timezone.now().date(),
        estado_cuenta="Activo",
    )

    area = AreaResponsable.objects.create(
        nombre="Limpieza Pública",
        descripcion="Área responsable de residuos sólidos",
        esta_activo=True,
    )

    categoria = Categoria.objects.create(
        nombre="Basura en la calle",
        descripcion="Residuos sólidos",
        esta_activo=True,
        id_area_responsable=area,
    )

    client = APIClient()

    # Crear una denuncia asociada a este ciudadano mediante el endpoint oficial
    payload = {
        "titulo": "Basura acumulada",
        "descripcion": "Hay basura acumulada desde hace varios días.",
        "id_categoria": categoria.id_categoria,
        "id_ciudadano": ciudadano.id_ciudadano,
        "es_anonima": False,
        "prioridad": "Baja",
        "ubicacion": {
            "latitud": -12.05,
            "longitud": -77.03,
            "direccion": "Jr. Limpio 101",
            "referencia": "Frente al mercado",
            "distrito": "Lima",
            "codigo_postal": "15002",
        },
    }

    resp_create = client.post("/api/denuncias/", payload, format="json")
    assert resp_create.status_code == 201

    # Ahora consultar /api/denuncias/mis-denuncias/ usando id_ciudadano como query param
    resp_list = client.get(
        "/api/denuncias/mis-denuncias/",
        {"id_ciudadano": ciudadano.id_ciudadano},
    )

    assert resp_list.status_code == 200
    data = resp_list.json()

    # mis_denuncias devuelve una lista (o resultados paginados); aquí asumimos lista simple
    assert isinstance(data, list) or "results" in data

    if isinstance(data, list):
        assert any(d["titulo"] == payload["titulo"] for d in data)
    else:
        assert any(d["titulo"] == payload["titulo"] for d in data.get("results", []))
