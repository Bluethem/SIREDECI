import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_usuario_notificaciones_lista_vacia_por_defecto(usuario_interno):
    """El usuario interno autenticado puede acceder al endpoint y,
    si no tiene notificaciones, obtiene una lista vacía.
    """
    client = APIClient()
    client.force_authenticate(user=usuario_interno)

    response = client.get("/api/notificaciones/usuario/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "results" in data
    assert data["results"] == []


@pytest.mark.django_db
def test_usuario_config_notificaciones_get_y_put(usuario_interno):
    """El usuario interno puede obtener y actualizar su configuración de notificaciones."""
    client = APIClient()
    client.force_authenticate(user=usuario_interno)

    # GET inicial: debería crear configuración por defecto
    resp_get = client.get("/api/notificaciones/usuario/config/")
    assert resp_get.status_code == 200
    data_get = resp_get.json()
    assert "recibir_email" in data_get

    # PUT para actualizar algunos campos
    payload = {
        "recibir_email": False,
        "recibir_sms": True,
        "frecuencia_resumen": "Semanal",
    }
    resp_put = client.put("/api/notificaciones/usuario/config/", payload, format="json")
    assert resp_put.status_code == 200
    data_put = resp_put.json()

    assert data_put["recibir_email"] is False
    assert data_put["recibir_sms"] is True
    assert data_put["frecuencia_resumen"] == "Semanal"
