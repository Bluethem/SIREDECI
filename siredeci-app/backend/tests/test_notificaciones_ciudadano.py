import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_ciudadano_notificaciones_lista_vacia_por_defecto():
    """Un ciudadano puede consultar sus notificaciones internas y,
    si no tiene ninguna, obtiene una lista vacía.
    """
    client = APIClient()

    usuario = User.objects.create(
        nombre_usuario="ciudadano_test",
        email="ciudadano@example.com",
    )

    response = client.get("/api/ciudadanos/notificaciones/", {"id_usuario": usuario.id_usuario})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "results" in data
    assert data["results"] == []


@pytest.mark.django_db
def test_ciudadano_config_notificaciones_get_y_put():
    """Un ciudadano puede obtener y actualizar su configuración de notificaciones."""
    client = APIClient()

    usuario = User.objects.create(
        nombre_usuario="ciudadano_conf",
        email="conf@example.com",
    )

    # GET inicial: debe crear configuración con valores por defecto
    resp_get = client.get("/api/ciudadanos/notificaciones/config/", {"id_usuario": usuario.id_usuario})
    assert resp_get.status_code == 200
    data_get = resp_get.json()
    assert "recibir_email" in data_get

    # PUT para actualizar preferencias
    payload = {
        "recibir_email": False,
        "recibir_push": False,
        "frecuencia_resumen": "Ninguno",
    }
    resp_put = client.put(
        f"/api/ciudadanos/notificaciones/config/?id_usuario={usuario.id_usuario}",
        payload,
        format="json",
    )
    assert resp_put.status_code == 200
    data_put = resp_put.json()

    assert data_put["recibir_email"] is False
    assert data_put["recibir_push"] is False
    assert data_put["frecuencia_resumen"] == "Ninguno"
