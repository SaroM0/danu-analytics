# Proyecto Django: Danu

Este es un proyecto Django enfocado en la visualización de datos y el análisis de ubicaciones usando mapas interactivos y gráficos. Contiene una aplicación principal llamada `danu` y una subaplicación llamada `analytics` que gestiona las vistas y la lógica de análisis.

## Estructura del Proyecto

- **danu/**
  - `settings.py`: Configuración principal de Django.
  - `urls.py`: Enrutamiento principal que incluye las URLs de la aplicación `analytics`.
  - `wsgi.py` y `asgi.py`: Archivos de configuración para despliegues en servidores compatibles con WSGI/ASGI.
  - `db.sqlite3`: Base de datos SQLite predeterminada.

- **analytics/**: Aplicación que gestiona las vistas para la visualización de datos.
  - `views.py`: Contiene la lógica para procesar los datos y renderizar vistas.
  - `models.py`: (Vacío) Puede usarse en el futuro para definir modelos de Django.
  - `templates/analytics/`: Carpeta que contiene los templates HTML para las diferentes visualizaciones (`home`, `chatbot`, `map`, `predictions`, `products`, `stores`).

- **data/**: Carpeta que contiene archivos CSV con datos para análisis y visualización.

- **static/**: Contiene archivos estáticos, como `styles.css` para los estilos del frontend.

## Dependencias

Este proyecto depende de las siguientes bibliotecas:
- **Django 4.2.16**: Framework principal para construir aplicaciones web.
- **Pandas**: Para la manipulación y análisis de datos.
- **Folium**: Para la creación de mapas interactivos.
- **Plotly**: Para gráficos interactivos.

> Para instalar todas las dependencias, asegúrate de tener `pip` y Python instalados y ejecuta los siguientes comandos en tu entorno virtual.

```bash
pip install django==4.2.16 pandas folium plotly
```

## Instalación y Configuración
1. **Clona el repositorio**:
   ```bash
   git clone <URL-del-repositorio>
   cd danu
   ```
2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configura la Base de Datos**: Ejecuta las migraciones de Django para preparar la base de datos:
   ```bash
   python manage.py migrate
   ```
4. **Carga los datos:**: Los datos en formato CSV deben estar en la carpeta `data/` para su análisis.
5. **Ejecuta el servidor**: Inicia el servidor local de Django:
    ```bash
   python manage.py runserver
   ```
    Accede a la aplicación en `http://127.0.0.1:8000/`.

## Uso de la Aplicación

La aplicación ofrece varias vistas para la visualización de datos:

- **Home** (`/`): Página de inicio con enlaces a otras visualizaciones.
- **Chatbot** (`/chatbot`): (Especifique la funcionalidad).
- **Mapa** (`/map`): Visualización de datos en un mapa interactivo.
- **Predicciones** (`/predictions`): (Especifique la funcionalidad).
- **Productos y Tiendas** (`/products` y `/stores`): Información sobre productos y ubicaciones.

