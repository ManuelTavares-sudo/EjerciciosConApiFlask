# 🚀 Ejercicios Prácticos de APIs con Flask

**Colección de 8 aplicaciones web completas usando Python Flask y diferentes APIs públicas**

## 🎯 Ejercicios

| # | Proyecto | Backend | Frontend | Descripción | API Key |
|---|----------|---------|----------|-------------|---------|
| 1.1 | 🌍 Clima | [clima_app.py](ejercicio_1_1/clima_app.py) | [clima.html](ejercicio_1_1/templates/clima.html) | Detecta ubicación y muestra clima actual | ✅ Gratis |
| 1.2 | 📍 Lugares | [lugares_app.py](ejercicio_1_2/lugares_app.py) | [lugares.html](ejercicio_1_2/templates/lugares.html) | Encuentra lugares cercanos (restaurantes, hospitales) | ❌ No |
| 2.1 | 🤖 Reddit | [reddit_app.py](ejercicio_2_1/reddit_app.py) | [reddit.html](ejercicio_2_1/templates/reddit.html) | Explora subreddits y busca posts | ❌ No |
| 2.2 | 🐙 GitHub | [github_app.py](ejercicio_2_2/github_app.py) | [github.html](ejercicio_2_2/templates/github.html) | Dashboard con estadísticas de usuarios/repos | ❌ No |
| 3.1 | 💾 CRUD API | [productos_api.py](ejercicio_3_1/productos_api.py) | [productos.html](ejercicio_3_1/templates/productos.html) | API REST completa con SQLite | ❌ No |
| 3.2 | 🔥 Chat | [chat_app.py](ejercicio_3_2/chat_app.py) | [chat.html](ejercicio_3_2/templates/chat.html) | Chat en tiempo real con Firebase | ✅ Google |
| 4.1 | 📚 Libros | [libros_app.py](ejercicio_4_1/libros_app.py) | [libros.html](ejercicio_4_1/templates/libros.html) | Buscador de millones de libros | ❌ No |
| 4.2 | 💰 Divisas | [divisas_app.py](ejercicio_4_2/divisas_app.py) | [divisas.html](ejercicio_4_2/templates/divisas.html) | Conversor de monedas en tiempo real | ✅ Gratis |

---

## 🛠️ Instalación
```bash
# Clonar repositorio
git clone https://github.com/TU-USUARIO/ejercicios-apis-flask.git
cd ejercicios-apis-flask

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install flask requests

# Ejecutar un ejercicio
cd ejercicio_1_2
python lugares_app.py
# Abrir http://127.0.0.1:5000
```

---

## 📚 Documentación de Ejercicios

### 1.1 🌍 Sistema de Clima por Ubicación

**Archivos:**
- 📄 Backend: [`clima_app.py`](ejercicio_1_1/clima_app.py)
- 🎨 Frontend: [`clima.html`](ejercicio_1_1/templates/clima.html)

**¿Qué hace?**
Detecta automáticamente tu ubicación usando tu dirección IP y muestra el clima actual en tiempo real.

**APIs utilizadas:**
- `ipapi.co` - Geolocalización por IP (sin API key)
- `OpenWeatherMap` - Datos meteorológicos (requiere API key gratis)

**Configuración:**
```python
# En clima_app.py, línea 7:
WEATHER_API_KEY = 'TU_API_KEY_AQUI'
```

**Obtener API Key:**
1. Ir a https://openweathermap.org/api
2. Crear cuenta gratuita
3. Copiar API key del dashboard

**Funcionalidades:**
- ✅ Detección automática de ubicación por IP
- ✅ Temperatura actual, sensación térmica, mín/máx
- ✅ Humedad, velocidad del viento, presión atmosférica
- ✅ Icono animado del clima
- ✅ Diseño con cielo nocturno y estrellas animadas

**Ejecutar:**
```bash
cd ejercicio_1_1
python clima_app.py
# http://127.0.0.1:5000
```

**Código clave:**
```python
# Obtener ubicación del usuario
ip_response = requests.get('https://ipapi.co/json/')
ubicacion = ip_response.json()

# Consultar clima en OpenWeatherMap
weather_url = 'https://api.openweathermap.org/data/2.5/weather'
params = {
    'lat': ubicacion['latitude'],
    'lon': ubicacion['longitude'],
    'appid': WEATHER_API_KEY,
    'units': 'metric',
    'lang': 'es'
}
clima_response = requests.get(weather_url, params=params)
```

---

### 1.2 📍 Buscador de Lugares Cercanos

**Archivos:**
- 📄 Backend: [`lugares_app.py`](ejercicio_1_2/lugares_app.py)
- 🎨 Frontend: [`lugares.html`](ejercicio_1_2/templates/lugares.html)

**¿Qué hace?**
Encuentra restaurantes, hospitales, farmacias, bancos y más lugares cerca de tu ubicación usando OpenStreetMap.

**API utilizada:**
- `Overpass API` (OpenStreetMap) - **No requiere API key** ✅

**Funcionalidades:**
- ✅ Geolocalización del navegador (pide permiso)
- ✅ 8 tipos de lugares: restaurantes, cafés, hospitales, farmacias, supermercados, gasolineras, bancos, hoteles
- ✅ Radio configurable: 500m, 1km, 2km, 5km
- ✅ Calcula distancia desde tu ubicación
- ✅ Muestra dirección, teléfono, horarios
- ✅ Integración con Google Maps

**Ejecutar:**
```bash
cd ejercicio_1_2
python lugares_app.py
# http://127.0.0.1:5000
```

**Código clave:**
```python
# Query de Overpass API para buscar lugares
overpass_query = f"""
[out:json][timeout:25];
(
  node[amenity=restaurant](around:{radio},{lat},{lon});
  way[amenity=restaurant](around:{radio},{lat},{lon});
);
out center;
"""

# Calcular distancia con fórmula de Haversine
import math
dlat = math.radians(coords['lat'] - lat)
dlon = math.radians(coords['lon'] - lon)
a = math.sin(dlat/2)**2 + math.cos(math.radians(lat)) * math.cos(math.radians(coords['lat'])) * math.sin(dlon/2)**2
distancia = round(6371000 * 2 * math.asin(math.sqrt(a)))
```

---

### 2.1 🤖 Analizador de Reddit

**Archivos:**
- 📄 Backend: [`reddit_app.py`](ejercicio_2_1/reddit_app.py)
- 🎨 Frontend: [`reddit.html`](ejercicio_2_1/templates/reddit.html)

**¿Qué hace?**
Explora cualquier subreddit, filtra posts por popularidad y realiza búsquedas globales en Reddit.

**API utilizada:**
- `Reddit JSON API` - **No requiere API key** ✅

**Funcionalidades:**
- ✅ Navegar por cualquier subreddit (r/python, r/webdev, etc.)
- ✅ Filtros: Hot 🔥, New 🆕, Top ⭐
- ✅ Búsqueda global en Reddit
- ✅ Muestra: título, autor, puntos, comentarios, fecha
- ✅ Lista de subreddits populares preconfigurados
- ✅ Interfaz estilo Reddit

**Ejecutar:**
```bash
cd ejercicio_2_1
python reddit_app.py
# http://127.0.0.1:5000
```

**Subreddits sugeridos:**
- `python` - Programación Python
- `webdev` - Desarrollo web
- `learnprogramming` - Aprender programación
- `javascript` - JavaScript
- `flask` - Flask framework

**Código clave:**
```python
# Obtener posts de un subreddit
url = f'https://www.reddit.com/r/{subreddit}/{filtro}.json'
headers = {'User-Agent': 'Mozilla/5.0 (compatible; FlaskApp/1.0)'}
response = requests.get(url, headers=headers, params={'limit': limit})

data = response.json()
for post in data['data']['children']:
    post_data = post['data']
    # Convertir timestamp a fecha
    fecha = datetime.fromtimestamp(post_data['created_utc'])
```

---

### 2.2 🐙 Dashboard de GitHub

**Archivos:**
- 📄 Backend: [`github_app.py`](ejercicio_2_2/github_app.py)
- 🎨 Frontend: [`github.html`](ejercicio_2_2/templates/github.html)

**¿Qué hace?**
Dashboard completo con estadísticas de usuarios y repositorios de GitHub, incluyendo trending repos.

**API utilizada:**
- `GitHub REST API` - **No requiere API key** ✅ (uso público limitado)

**Funcionalidades:**
- ✅ Perfil completo del usuario (avatar, bio, ubicación, empresa)
- ✅ Estadísticas: repos públicos, seguidores, stars totales, forks
- ✅ Top 5 lenguajes de programación usados (con barra visual)
- ✅ Repositorios destacados (ordenados por stars)
- ✅ Trending repos de la última semana
- ✅ Filtros por lenguaje de programación

**Ejecutar:**
```bash
cd ejercicio_2_2
python github_app.py
# http://127.0.0.1:5000
```

**Usuarios sugeridos:**
- `torvalds` - Linus Torvalds (creador de Linux)
- `gaearon` - Dan Abramov (React core team)
- `sindresorhus` - Sindre Sorhus
- `tj` - TJ Holowaychuk
- `yyx990803` - Evan You (creador de Vue.js)

**Código clave:**
```python
# Obtener información del usuario
user_response = requests.get(
    f'https://api.github.com/users/{username}',
    headers={'Accept': 'application/vnd.github.v3+json'}
)

# Obtener repositorios
repos_response = requests.get(
    f'https://api.github.com/users/{username}/repos',
    params={'per_page': 100, 'sort': 'updated'}
)

# Calcular estadísticas
total_stars = sum(repo['stargazers_count'] for repo in repos)
total_forks = sum(repo['forks_count'] for repo in repos)

# Contar lenguajes
lenguajes = {}
for repo in repos:
    lang = repo['language']
    if lang:
        lenguajes[lang] = lenguajes.get(lang, 0) + 1
```

---

### 3.1 💾 API REST con SQLite (CRUD Completo)

**Archivos:**
- 📄 Backend: [`productos_api.py`](ejercicio_3_1/productos_api.py)
- 🎨 Frontend: [`productos.html`](ejercicio_3_1/templates/productos.html)

**¿Qué hace?**
API REST completa con operaciones CRUD (Create, Read, Update, Delete) para gestión de productos usando SQLite.

**Tecnología:**
- `SQLite` - Base de datos local - **No requiere configuración** ✅

**Funcionalidades:**
- ✅ **CREATE**: Crear productos nuevos
- ✅ **READ**: Listar todos los productos con filtros
- ✅ **UPDATE**: Actualizar productos existentes
- ✅ **DELETE**: Eliminar productos
- ✅ Búsqueda por nombre/descripción
- ✅ Filtros por categoría
- ✅ Ordenamiento configurable (nombre, precio, stock, fecha)
- ✅ Estadísticas en tiempo real
- ✅ Interfaz de gestión completa con modales
- ✅ Base de datos se crea automáticamente con datos de ejemplo

**Ejecutar:**
```bash
cd ejercicio_3_1
python productos_api.py
# http://127.0.0.1:5000
# La BD se crea automáticamente
```

**Endpoints de la API:**
```bash
# Listar productos
GET /api/productos
GET /api/productos?categoria=Electrónica
GET /api/productos?buscar=laptop&orden=precio&dir=DESC

# Obtener un producto
GET /api/productos/1

# Crear producto
POST /api/productos
Content-Type: application/json
{
  "nombre": "Laptop HP",
  "descripcion": "Laptop 15.6 pulgadas",
  "precio": 15999.99,
  "stock": 10,
  "categoria": "Electrónica"
}

# Actualizar producto
PUT /api/productos/1
Content-Type: application/json
{
  "nombre": "Laptop HP Pavilion",
  "precio": 16999.99,
  "stock": 8
}

# Eliminar producto
DELETE /api/productos/1

# Obtener estadísticas
GET /api/productos/stats

# Listar categorías
GET /api/categorias
```

**Probar con cURL:**
```bash
# Crear
curl -X POST http://127.0.0.1:5000/api/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Mouse Gamer","precio":899.99,"stock":15,"categoria":"Accesorios"}'

# Actualizar
curl -X PUT http://127.0.0.1:5000/api/productos/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Mouse Gamer RGB","precio":999.99,"stock":10}'

# Eliminar
curl -X DELETE http://127.0.0.1:5000/api/productos/1
```

**Código clave:**
```python
# Crear tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        stock INTEGER DEFAULT 0,
        categoria TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# CREATE
cursor.execute('''
    INSERT INTO productos (nombre, descripcion, precio, stock, categoria)
    VALUES (?, ?, ?, ?, ?)
''', (nombre, descripcion, precio, stock, categoria))

# READ
cursor.execute('SELECT * FROM productos WHERE categoria = ?', (categoria,))
productos = [dict(row) for row in cursor.fetchall()]

# UPDATE
cursor.execute('''
    UPDATE productos 
    SET nombre=?, precio=?, stock=?, fecha_actualizacion=CURRENT_TIMESTAMP
    WHERE id=?
''', (nombre, precio, stock, id))

# DELETE
cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
```

---

### 3.2 🔥 Chat en Tiempo Real con Firebase

**Archivos:**
- 📄 Backend: [`chat_app.py`](ejercicio_3_2/chat_app.py)
- 🎨 Frontend: [`chat.html`](ejercicio_3_2/templates/chat.html)

**¿Qué hace?**
Chat multi-usuario en tiempo real con sincronización automática usando Firebase Realtime Database.

**API utilizada:**
- `Firebase Realtime Database` - Requiere cuenta Google ✅

**Funcionalidades:**
- ✅ Mensajería en tiempo real (sincronización automática)
- ✅ Múltiples usuarios simultáneos
- ✅ 10 avatares personalizables (emojis)
- ✅ 6 colores de burbuja personalizables
- ✅ Indicador de usuarios online
- ✅ Actualización automática cada 2.5 segundos
- ✅ Historial de mensajes persistente

**Configuración (paso a paso):**

1. **Crear proyecto Firebase:**
   - Ir a https://console.firebase.google.com
   - Click "Agregar proyecto"
   - Nombre: "chat-flask" (o el que quieras)
   - Desactivar Google Analytics (opcional)
   - Crear proyecto

2. **Configurar Realtime Database:**
   - Menú izquierdo → Compilación → Realtime Database
   - "Crear base de datos"
   - Ubicación: `us-central1`
   - Modo: **"Comenzar en modo de prueba"** (importante)
   - Copiar URL (ej: `https://chat-flask-xxxxx-default-rtdb.firebaseio.com`)

3. **Obtener credenciales:**
   - Configuración proyecto (⚙️) → Cuentas de servicio
   - "Generar nueva clave privada"
   - Descargar archivo JSON

4. **Configurar app:**
```bash
   # Guardar archivo descargado como:
   ejercicio_3_2/firebase-credentials.json
   
   # Editar chat_app.py línea 14:
   FIREBASE_DB_URL = 'https://TU-PROYECTO-default-rtdb.firebaseio.com'
   
   # Instalar dependencia:
   pip install firebase-admin
```

**Ejecutar:**
```bash
cd ejercicio_3_2
python chat_app.py
# http://127.0.0.1:5000
```

**Código clave:**
```python
# Inicializar Firebase
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tu-proyecto.firebaseio.com'
})

# Enviar mensaje
ref = db.reference('mensajes')
nuevo_mensaje = ref.push({
    'usuario': 'Juan',
    'texto': 'Hola mundo',
    'avatar': '😀',
    'color': '#6366f1',
    'timestamp': datetime.now().isoformat()
})

# Leer mensajes
mensajes = ref.order_by_child('timestamp').limit_to_last(50).get()

# Usuario online
ref = db.reference(f'presencia/{usuario}')
ref.set({
    'online': True,
    'ultima_actividad': datetime.now().isoformat()
})
```

**Estructura de datos en Firebase:**
```json
{
  "mensajes": {
    "-NabcDEF123": {
      "usuario": "Juan",
      "texto": "Hola mundo",
      "avatar": "😀",
      "color": "#6366f1",
      "timestamp": "2026-02-17T12:30:00Z"
    }
  },
  "presencia": {
    "Juan": {
      "online": true,
      "ultima_actividad": "2026-02-17T12:30:00Z"
    }
  }
}
```

---

### 4.1 📚 Buscador de Libros

**Archivos:**
- 📄 Backend: [`libros_app.py`](ejercicio_4_1/libros_app.py)
- 🎨 Frontend: [`libros.html`](ejercicio_4_1/templates/libros.html)

**¿Qué hace?**
Buscador de millones de libros con información completa, vista previa y enlaces de compra.

**API utilizada:**
- `Google Books API` - **No requiere API key** ✅

**Funcionalidades:**
- ✅ Búsqueda por título, autor o tema
- ✅ Filtros por categoría (19 categorías disponibles)
- ✅ Filtros por idioma (Español, Inglés, Todos)
- ✅ Resultados configurables (12, 20 o 40 libros)
- ✅ Modal con información detallada del libro
- ✅ Vista previa en Google Books
- ✅ Enlaces de compra
- ✅ Rating con estrellas
- ✅ Tags populares preconfigurados
- ✅ Diseño editorial elegante

**Ejecutar:**
```bash
cd ejercicio_4_1
python libros_app.py
# http://127.0.0.1:5000
```

**Búsquedas sugeridas:**
- "inteligencia artificial"
- "programacion python"
- "historia de méxico"
- "desarrollo personal"
- "ciencia ficción"

**Código clave:**
```python
# Buscar libros
params = {
    'q': query,
    'maxResults': 20,
    'printType': 'books',
    'langRestrict': 'es'
}
response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)

data = response.json()
for item in data['items']:
    info = item['volumeInfo']
    libro = {
        'id': item['id'],
        'titulo': info.get('title'),
        'autores': info.get('authors', []),
        'descripcion': info.get('description'),
        'imagen': info.get('imageLinks', {}).get('thumbnail'),
        'rating': info.get('averageRating'),
        'paginas': info.get('pageCount'),
        'preview_link': info.get('previewLink')
    }

# Obtener detalles de un libro
response = requests.get(f'https://www.googleapis.com/books/v1/volumes/{book_id}')
```

---

### 4.2 💰 Conversor de Divisas

**Archivos:**
- 📄 Backend: [`divisas_app.py`](ejercicio_4_2/divisas_app.py)
- 🎨 Frontend: [`divisas.html`](ejercicio_4_2/templates/divisas.html)

**¿Qué hace?**
Conversor de monedas en tiempo real con tasas actualizadas y tabla de conversiones.

**API utilizada:**
- `ExchangeRate-API` - Requiere API key gratis ✅

**Funcionalidades:**
- ✅ Conversión entre 16+ monedas principales
- ✅ Tasas de cambio en tiempo real
- ✅ Botón de intercambio rápido (swap)
- ✅ Tabla de tasas desde USD
- ✅ Cálculo de tasa inversa
- ✅ Diseño dark mode minimalista
- ✅ Banderas de países

**Monedas soportadas:**
- 🇺🇸 USD (Dólar Estadounidense)
- 🇪🇺 EUR (Euro)
- 🇬🇧 GBP (Libra Esterlina)
- 🇯🇵 JPY (Yen Japonés)
- 🇲🇽 MXN (Peso Mexicano)
- 🇨🇦 CAD (Dólar Canadiense)
- 🇦🇺 AUD (Dólar Australiano)
- 🇨🇭 CHF (Franco Suizo)
- 🇨🇳 CNY (Yuan Chino)
- 🇧🇷 BRL (Real Brasileño)
- 🇦🇷 ARS (Peso Argentino)
- 🇨🇴 COP (Peso Colombiano)
- 🇨🇱 CLP (Peso Chileno)
- 🇮🇳 INR (Rupia India)
- 🇰🇷 KRW (Won Coreano)
- 🇸🇬 SGD (Dólar de Singapur)

**Configuración:**
```python
# 1. Ir a: https://www.exchangerate-api.com
# 2. Crear cuenta gratuita (1,500 requests/mes)
# 3. Copiar API key
# 4. En divisas_app.py línea 7:
API_KEY = 'TU_API_KEY_AQUI'
```

**Ejecutar:**
```bash
cd ejercicio_4_2
python divisas_app.py
# http://127.0.0.1:5000
```

**Código clave:**
```python
# Convertir entre monedas
url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{de}/{a}/{monto}'
response = requests.get(url)
data = response.json()

resultado = {
    'monto_convertido': data['conversion_result'],
    'tasa_conversion': data['conversion_rate'],
    'ultima_actualizacion': data['time_last_update_utc']
}

# Obtener todas las tasas
url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
response = requests.get(url)
tasas = response.json()['conversion_rates']
```

---

## 🔧 Tecnologías Utilizadas

### Backend
- **Python 3.7+** - Lenguaje de programación
- **Flask 3.0+** - Framework web minimalista
- **Requests** - Cliente HTTP para APIs
- **SQLite** - Base de datos SQL embebida
- **Firebase Admin SDK** - Integración con Firebase

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Estilos modernos (cada app con diseño único)
- **JavaScript (Vanilla)** - Sin frameworks, puro JS
- **Fetch API** - Peticiones HTTP asíncronas

### APIs Externas
- OpenWeatherMap API
- Overpass API (OpenStreetMap)
- Reddit JSON API
- GitHub REST API v3
- Google Books API
- ExchangeRate-API
- Firebase Realtime Database
- ipapi (geolocalización)

---

## 📁 Estructura del Proyecto
```
ejercicios-apis-flask/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── ejercicio_1_1/              # 🌍 Clima
│   ├── clima_app.py            # Backend Flask
│   └── templates/
│       └── clima.html          # Frontend
│
├── ejercicio_1_2/              # 📍 Lugares
│   ├── lugares_app.py
│   └── templates/
│       └── lugares.html
│
├── ejercicio_2_1/              # 🤖 Reddit
│   ├── reddit_app.py
│   └── templates/
│       └── reddit.html
│
├── ejercicio_2_2/              # 🐙 GitHub
│   ├── github_app.py
│   └── templates/
│       └── github.html
│
├── ejercicio_3_1/              # 💾 CRUD API
│   ├── productos_api.py
│   ├── productos.db            # Se crea automáticamente
│   └── templates/
│       └── productos.html
│
├── ejercicio_3_2/              # 🔥 Chat
│   ├── chat_app.py
│   ├── firebase-credentials.json  # Debes crearlo
│   └── templates/
│       └── chat.html
│
├── ejercicio_4_1/              # 📚 Libros
│   ├── libros_app.py
│   └── templates/
│       └── libros.html
│
└── ejercicio_4_2/              # 💰 Divisas
    ├── divisas_app.py
    └── templates/
        └── divisas.html
```

---

## 🚀 Cómo Empezar

### Recomendación de Orden

**Nivel Principiante** (sin API keys):
1. **ejercicio_1_2** - Lugares cercanos
2. **ejercicio_2_1** - Reddit
3. **ejercicio_4_1** - Libros

**Nivel Intermedio**:
4. **ejercicio_2_2** - GitHub
5. **ejercicio_3_1** - CRUD API
6. **ejercicio_1_1** - Clima (requiere API key)
7. **ejercicio_4_2** - Divisas (requiere API key)

**Nivel Avanzado**:
8. **ejercicio_3_2** - Chat Firebase (configuración compleja)

### Ejecutar Cualquier Ejercicio
```bash
# Navegar al ejercicio
cd ejercicio_X_X

# Ejecutar
python nombre_app.py

# Abrir navegador
http://127.0.0.1:5000

# Detener (Ctrl+C)
```

---

## 🎨 Características de Diseño

Cada ejercicio tiene un **diseño UI único** y profesional:

- **Ejercicio 1.1:** Tema nocturno con gradientes azules y estrellas animadas
- **Ejercicio 1.2:** Diseño limpio estilo Material Design
- **Ejercicio 2.1:** Interfaz inspirada en Reddit con tema claro
- **Ejercicio 2.2:** Dashboard oscuro estilo GitHub
- **Ejercicio 3.1:** Admin panel moderno con modales y toast notifications
- **Ejercicio 3.2:** Chat burbujas con avatares coloridos
- **Ejercicio 4.1:** Biblioteca elegante estilo editorial
- **Ejercicio 4.2:** Conversor minimalista dark mode con efectos de luz

---


## 👤 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

---




<div align="center">

**⭐ Si este proyecto te ayudó, considera darle una estrella ⭐**

**Hecho con ❤️ y Python**

</div>
