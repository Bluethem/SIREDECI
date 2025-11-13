# Alternativas GRATUITAS a Google Maps

## 🗺️ Opciones 100% Gratuitas para Mapas Interactivos

### 1. **OpenStreetMap + Leaflet.js** ⭐ RECOMENDADO

**Ventajas:**
- ✅ Totalmente GRATIS sin límites de uso
- ✅ No requiere API Key ni tarjeta de crédito
- ✅ Datos de código abierto mantenidos por la comunidad
- ✅ Leaflet.js es liviano (~39KB) y fácil de usar
- ✅ Excelente documentación y comunidad activa
- ✅ Funciona sin restricciones en localhost y producción

**Instalación:**
```bash
npm install leaflet
```

**Implementación básica:**
```javascript
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Inicializar mapa
const map = L.map('map').setView([-12.0464, -77.0428], 13)

// Agregar capa de tiles de OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 19
}).addTo(map)

// Agregar marcador
const marker = L.marker([-12.0464, -77.0428]).addTo(map)
marker.bindPopup('Ubicación de la denuncia').openPopup()

// Hacer el mapa interactivo para seleccionar ubicación
map.on('click', (e) => {
  const { lat, lng } = e.latlng
  marker.setLatLng([lat, lng])
  console.log('Nueva ubicación:', lat, lng)
})
```

**Proveedores de tiles gratuitos:**
- OpenStreetMap Standard
- OpenStreetMap.HOT (Humanitarian)
- CartoDB Positron (minimalista)
- CartoDB Dark Matter (modo oscuro)

---

### 2. **Mapbox GL JS** (Plan gratuito generoso)

**Ventajas:**
- ✅ 50,000 cargas de mapa gratis/mes (sin tarjeta de crédito)
- ✅ Mapas más modernos y personalizables que Google Maps
- ✅ Excelente rendimiento con WebGL
- ✅ Geocoding gratuito incluido
- ✅ Diseño de mapas personalizado

**Instalación:**
```bash
npm install mapbox-gl
```

**Uso:**
```javascript
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

mapboxgl.accessToken = 'TU_ACCESS_TOKEN_GRATIS'

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [-77.0428, -12.0464],
  zoom: 13
})

const marker = new mapboxgl.Marker()
  .setLngLat([-77.0428, -12.0464])
  .addTo(map)
```

**Obtener API Key gratuita:**
1. Regístrate en [mapbox.com](https://account.mapbox.com/auth/signup/)
2. No requiere tarjeta de crédito
3. 50,000 cargas/mes gratis permanentemente

---

### 3. **Maptiler + Leaflet** (Plan gratuito)

**Ventajas:**
- ✅ 100,000 cargas de tiles gratis/mes
- ✅ Mapas personalizables con editor visual
- ✅ Compatible con Leaflet.js
- ✅ Geocoding incluido
- ✅ Mejor calidad visual que OpenStreetMap estándar

**Uso con Leaflet:**
```javascript
import L from 'leaflet'

const map = L.map('map').setView([-12.0464, -77.0428], 13)

L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=TU_API_KEY', {
  attribution: '© MapTiler © OpenStreetMap contributors',
  maxZoom: 20
}).addTo(map)
```

**Registro:** [maptiler.com](https://www.maptiler.com/cloud/)

---

### 4. **HERE Maps** (Plan gratuito)

**Ventajas:**
- ✅ 250,000 transacciones gratis/mes
- ✅ Excelente para geocoding y routing
- ✅ Datos de tráfico incluidos
- ✅ Funciona bien en Perú y Latinoamérica

**Registro:** [developer.here.com](https://developer.here.com/)

---

## 🎯 Recomendación para SIREDECI

### Opción 1: OpenStreetMap + Leaflet (SIN API KEY)

**Mejor para:** Proyectos que quieren evitar cualquier dependencia externa o límites.

**Pros:**
- No necesitas registrarte ni API key
- Funciona inmediatamente
- Sin restricciones de uso
- Ideal para desarrollo y producción

**Contras:**
- Menos funciones avanzadas que Google Maps
- Diseño más básico (pero personalizable)

---

### Opción 2: Mapbox GL (CON API KEY GRATIS)

**Mejor para:** Proyectos que quieren mapas modernos y bonitos.

**Pros:**
- Mapas más atractivos visualmente
- Rendimiento superior con WebGL
- 50,000 cargas/mes es suficiente para proyectos medianos
- Geocoding incluido

**Contras:**
- Requiere registro y API key
- Límite mensual (aunque generoso)

---

## 💻 Implementación Recomendada para SIREDECI

### Usar Leaflet + OpenStreetMap (100% Gratis, Sin API Key)

**Paso 1: Instalar Leaflet**
```bash
cd frontend
npm install leaflet
```

**Paso 2: Actualizar `RegistrarDenuncia.vue`**

Reemplazar la función `initMap()` con:

```javascript
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix para los iconos de Leaflet en Vite
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow
})

const initMap = () => {
  const mapElement = document.getElementById('map')
  if (!mapElement || map) return
  
  // Crear mapa centrado en Lima, Perú
  map = L.map('map').setView(
    [parseFloat(form.value.ubicacion.latitud), parseFloat(form.value.ubicacion.longitud)], 
    15
  )
  
  // Agregar tiles de OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)
  
  // Agregar marcador arrastrable
  marker = L.marker(
    [parseFloat(form.value.ubicacion.latitud), parseFloat(form.value.ubicacion.longitud)],
    { draggable: true }
  ).addTo(map)
  
  // Actualizar coordenadas cuando se mueve el marcador
  marker.on('dragend', (e) => {
    const position = marker.getLatLng()
    form.value.ubicacion.latitud = position.lat.toFixed(6)
    form.value.ubicacion.longitud = position.lng.toFixed(6)
  })
  
  // Permitir hacer clic en el mapa para mover el marcador
  map.on('click', (e) => {
    marker.setLatLng(e.latlng)
    form.value.ubicacion.latitud = e.latlng.lat.toFixed(6)
    form.value.ubicacion.longitud = e.latlng.lng.toFixed(6)
  })
}
```

**Paso 3: Agregar estilos CSS en el componente**

```css
<style scoped>
/* Importar estilos de Leaflet */
@import 'leaflet/dist/leaflet.css';

.material-symbols-outlined {
  font-variation-settings:
  'FILL' 0,
  'wght' 400,
  'GRAD' 0,
  'opsz' 24
}

/* Asegurar que el mapa tenga altura */
#map {
  height: 100%;
  width: 100%;
  z-index: 0;
}
</style>
```

---

## 📊 Comparación de Costos

| Servicio | Cargas Gratis/Mes | Requiere Tarjeta | API Key |
|----------|-------------------|------------------|---------|
| **OpenStreetMap + Leaflet** | ∞ Ilimitado | ❌ No | ❌ No |
| **Mapbox** | 50,000 | ❌ No | ✅ Sí |
| **Maptiler** | 100,000 | ❌ No | ✅ Sí |
| **HERE Maps** | 250,000 | ✅ Sí | ✅ Sí |
| **Google Maps** | 28,000* | ✅ Sí | ✅ Sí |

*Google Maps requiere tarjeta de crédito incluso para el plan gratuito.

---

## 🚀 Ventajas de OpenStreetMap para tu proyecto

1. **Cero configuración:** No necesitas crear cuenta ni obtener API keys
2. **Sin límites:** Nunca te quedarás sin créditos
3. **Open Source:** Datos abiertos, sin restricciones legales
4. **Buena cobertura en Perú:** OpenStreetMap tiene excelente cobertura en ciudades peruanas
5. **Privacidad:** No envías datos de tus usuarios a terceros
6. **Desarrollo local:** Funciona perfectamente en localhost sin restricciones

---

## 📚 Recursos Adicionales

### Leaflet.js
- [Documentación oficial](https://leafletjs.com/)
- [Tutoriales interactivos](https://leafletjs.com/examples.html)
- [Plugins útiles](https://leafletjs.com/plugins.html)

### OpenStreetMap
- [Wiki oficial](https://wiki.openstreetmap.org/)
- [Proveedores de tiles](https://wiki.openstreetmap.org/wiki/Tile_servers)
- [Nominatim (Geocoding gratuito)](https://nominatim.openstreetmap.org/)

### Geocoding Gratuito (Para convertir direcciones en coordenadas)
- **Nominatim:** Geocoding gratuito de OpenStreetMap
- **Photon:** Alternativa rápida y moderna
- Ambos son 100% gratuitos y sin límites razonables

---

## ⚡ Siguiente Paso Recomendado

Implementar **Leaflet + OpenStreetMap** porque:
- ✅ Es la opción más simple y sin complicaciones
- ✅ No requiere registro ni API keys
- ✅ Funciona inmediatamente
- ✅ Sin costos ocultos ni límites
- ✅ Perfecto para tu proyecto universitario

**¿Quieres que implemente Leaflet en tu proyecto ahora?** 🚀
