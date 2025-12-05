"""Inicialización de settings.

Para el caso de deploy en Render se usa directamente ``config.settings.direct``,
por lo que este archivo NO debe importar ``base.py`` ni otras variantes cuando
``DJANGO_SETTINGS_MODULE`` apunta explícitamente a un submódulo (direct,
development, production).

Solo cuando ``DJANGO_SETTINGS_MODULE`` es exactamente ``config.settings`` se
carga la configuración basada en ``base.py`` + entorno.
"""

import os

dj_settings_module = os.getenv('DJANGO_SETTINGS_MODULE', '')

if dj_settings_module in ('', 'config.settings'):
    # Importar configuración según entorno solo para el caso genérico
    from .base import *  # noqa: F401,F403

    environment = os.getenv('DJANGO_ENV', 'development')

    if environment == 'production':
        from .production import *  # noqa: F401,F403
    else:
        from .development import *  # noqa: F401,F403