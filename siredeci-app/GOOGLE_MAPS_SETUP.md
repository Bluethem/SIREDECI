# Configuración de Google Maps API

## Pasos para obtener y configurar tu API Key de Google Maps

### 1. Crear un proyecto en Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la facturación (Google Maps requiere una tarjeta de crédito, pero ofrece $200 USD de crédito mensual gratis)

### 2. Habilitar las APIs necesarias

En Google Cloud Console, habilita las siguientes APIs:
- **Maps JavaScript API** (para mostrar mapas interactivos)
- **Places API** (para autocompletar direcciones)
- **Geocoding API** (para convertir coordenadas en direcciones)

### 3. Crear una API Key

1. En el menú lateral, ve a **APIs y servicios > Credenciales**
2. Haz clic en **Crear credenciales > Clave de API**
3. Copia la API Key generada

### 4. Configurar restricciones de seguridad (Recomendado)

Para proteger tu API Key:

1. En la lista de credenciales, haz clic en el nombre de tu API Key
2. En **Restricciones de aplicación**:
   - Selecciona "Referentes HTTP (sitios web)"
   - Agrega los dominios permitidos:
     ```
     http://localhost:5173/*
     http://127.0.0.1:5173/*
     https://tu-dominio.com/*
     ```

3. En **Restricciones de API**:
   - Selecciona "Restringir clave"
   - Marca solo las APIs que habilitaste en el paso 2

### 5. Configurar la API Key en el proyecto

Reemplaza `YOUR_API_KEY` en el archivo `frontend/index.html`:

```html
<!-- Antes -->
<script async defer
  src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initMap">
</script>

<!-- Después (con tu API Key) -->
<script async defer
  src="https://maps.googleapis.com/maps/api/js?key=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&libraries=places&callback=initMap">
</script>
```

### 6. Alternativa: Usar variables de entorno (Recomendado para producción)

Para mayor seguridad, puedes usar variables de entorno:

1. Crea un archivo `.env.local` en la carpeta `frontend`:
   ```
   VITE_GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

2. Modifica el `index.html` o crea un componente wrapper para cargar el script dinámicamente

3. Accede a la variable en tu código:
   ```javascript
   const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
   ```

## Uso en el proyecto

Una vez configurada la API Key, el mapa se cargará automáticamente cuando el usuario llegue al **Paso 3: Ubicación** al registrar una denuncia.

### Funcionalidades disponibles:

- ✅ Mapa interactivo con arrastre
- ✅ Marcador de ubicación
- ✅ Obtención de coordenadas (latitud/longitud)
- ✅ Botón "Usar mi ubicación actual" (requiere permisos del navegador)
- ✅ Campo de dirección editable
- ✅ Campo de referencia adicional

## Costos

Google Maps ofrece **$200 USD de crédito mensual gratis**, que generalmente es suficiente para:
- Aproximadamente 28,000 cargas de mapa por mes
- Más de lo que la mayoría de aplicaciones pequeñas necesitan

Monitorea tu uso en [Google Cloud Console > Facturación](https://console.cloud.google.com/billing).

## Troubleshooting

### Error: "This page can't load Google Maps correctly"
- Verifica que tu API Key sea correcta
- Confirma que las APIs estén habilitadas
- Revisa las restricciones de dominio

### El mapa no se muestra
- Abre la consola del navegador (F12) y busca errores
- Verifica que el script de Google Maps se haya cargado
- Confirma que el elemento `<div id="map">` exista en el DOM

### Error de permisos de geolocalización
- El navegador debe permitir el acceso a la ubicación
- En Chrome: Configuración > Privacidad y seguridad > Configuración de sitios > Ubicación

## Recursos adicionales

- [Documentación oficial de Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
- [Ejemplos de código](https://developers.google.com/maps/documentation/javascript/examples)
- [Precios de Google Maps](https://developers.google.com/maps/pricing-and-plans)
