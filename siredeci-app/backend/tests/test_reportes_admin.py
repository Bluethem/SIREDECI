import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_admin_indicators_list_estructura_basica(usuario_interno):
    """Un usuario interno autenticado puede acceder al listado de indicadores.

    Verificamos que responde 200 y devuelve un diccionario con 'results' (lista).
    No asumimos que existan indicadores de ejemplo, solo la estructura.
    """
    client = APIClient()
    client.force_authenticate(user=usuario_interno)

    response = client.get("/api/reportes/indicators/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert "results" in data
    assert isinstance(data["results"], list)


@pytest.mark.django_db
def test_admin_ranking_desempeno_estructura_basica(usuario_interno):
    """Un usuario interno autenticado puede acceder al ranking de desempeño.

    Verificamos código 200 y estructura con 'count', 'results'.
    """
    client = APIClient()
    client.force_authenticate(user=usuario_interno)

    response = client.get("/api/reportes/desempeno/ranking/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert "count" in data
    assert "results" in data
    assert isinstance(data["results"], list)


@pytest.mark.django_db
def test_admin_dashboard_summary_estructura_basica(usuario_interno):
    """El resumen del dashboard admin responde con las claves esperadas.

    Endpoint: /api/reportes/dashboard/summary/
    """
    client = APIClient()
    client.force_authenticate(user=usuario_interno)

    response = client.get("/api/reportes/dashboard/summary/")

    assert response.status_code == 200
    data = response.json()

    # Estructura básica según views.dashboard_summary
    for key in [
        "total_denuncias",
        "avg_tiempo_atencion_horas",
        "tasa_resolucion",
        "avg_satisfaccion",
        "hoy",
        "estados",
    ]:
        assert key in data

    assert isinstance(data["hoy"], dict)
    assert isinstance(data["estados"], dict)
