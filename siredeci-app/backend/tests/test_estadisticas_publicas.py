import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_public_estadisticas_denuncias_resumen_estructura_basica():
    """El endpoint de resumen público devuelve las claves esperadas.

    No asumimos que existan datos en la BD, solo verificamos la estructura del payload.
    """
    client = APIClient()

    response = client.get("/api/public/reportes/estadisticas/denuncias-resumen/")

    assert response.status_code == 200
    data = response.json()

    assert "stats" in data
    assert "categorias" in data
    assert "estados" in data
    assert "distritos" in data

    stats = data["stats"]
    assert "total" in stats
    assert "resueltas" in stats
    assert "en_proceso" in stats
    assert "tiempo_promedio_horas" in stats


@pytest.mark.django_db
def test_public_tendencias_geograficas_respuesta_valida():
    """El endpoint de tendencias geográficas públicas responde 200 y devuelve una lista.

    No se valida el contenido exacto, solo que la respuesta tenga formato esperado.
    """
    client = APIClient()

    response = client.get("/api/public/reportes/tendencias-geograficas/")

    assert response.status_code == 200
    data = response.json()

    # views.public_tendencias_geograficas devuelve {'results': [...]}
    assert isinstance(data, dict)
    assert "results" in data
    assert isinstance(data["results"], list)


@pytest.mark.django_db
def test_public_ranking_areas_respuesta_valida():
    """El endpoint de ranking de áreas públicas responde 200 y devuelve una lista.

    Solo verificamos estructura básica, no datos concretos.
    """
    client = APIClient()

    response = client.get("/api/public/reportes/ranking-areas/")

    assert response.status_code == 200
    data = response.json()

    # views.public_ranking_areas devuelve {'results': [...]}
    assert isinstance(data, dict)
    assert "results" in data
    assert isinstance(data["results"], list)
